"""
Flask Web Application for ISE Switch Session Management.

This Flask web application provides a user interface to:
1. Collect access-session information from Cisco switches
2. View failed/unauthorized authentication sessions
3. Update endpoint group assignments in Cisco ISE
4. Manage individual MAC address endpoint groups

Routes:
    /: Main page with options to check switch or search by MAC
    /check-result: Display access-session results from a switch
    /mac/<mac>: Display and update ISE group for a specific MAC address
    /update/<mac>: Process ISE group update for a MAC address
    /endpoint: Search for endpoint by MAC address
"""

from typing import Dict
from flask import Flask, render_template, request, flash
import check_access_sessions
import ise_api

# Initialize Flask application
app = Flask(__name__, static_url_path="/static")


@app.route("/", methods=["GET", "POST"])
def main():
    """
    Render the main page of the application.

    This is the landing page that provides two main options:
    1. Enter a switch IP address to collect session information
    2. Enter a MAC address to search for endpoint in ISE

    Returns:
        str: Rendered HTML template for the main page.
    """
    return render_template("main.html")


@app.route("/check-result", methods=["POST"])
def check():
    """
    Collect and display access-session information from a Cisco switch.

    This route receives a switch IP address from the form, connects to the switch,
    collects all access-session information, and displays details about any
    failed or unauthorized sessions.

    Form Parameters:
        ip_address (str): IP address of the Cisco switch to query.

    Returns:
        str: Rendered HTML template displaying session results in a table format.

    Example:
        POST /check-result
        Form data: ip_address=192.168.1.1
    """
    ip_address = request.form.get("ip_address")
    dict_result = check_access_sessions.main(ip_address)
    return render_template("check-result.html", dict_result=dict_result)


@app.route("/mac/<mac>", methods=["GET", "POST"])
def search_ise(mac: str):
    """
    Display ISE endpoint information and available groups for a MAC address.

    This route retrieves the current endpoint group assignment for a given MAC address
    and displays all available ISE endpoint groups for potential reassignment.

    Args:
        mac (str): MAC address to search for in ISE.

    Returns:
        str: Rendered HTML template showing current group and available groups.

    Example:
        GET /mac/AA:BB:CC:DD:EE:FF
    """
    endpoint_group_name = "Unknown"
    ise_groups = ise_api.get_group_id()
    endpoint_group_id = ise_api.get_endpoint_group_id(mac)

    # Find the current group name from the group ID
    for group_id, group_name in ise_groups.items():
        if group_id == endpoint_group_id:
            endpoint_group_name = group_name
            break

    return render_template(
        "update-mac.html",
        mac=mac,
        endpoint_group_id=endpoint_group_name,
        ise_groups=ise_groups,
    )


@app.route("/update/<mac>", methods=["POST"])
def update_ise(mac: str):
    """
    Update the ISE endpoint group assignment for a MAC address.

    This route processes the form submission to update an endpoint's group
    assignment in Cisco ISE.

    Args:
        mac (str): MAC address of the endpoint to update.

    Form Parameters:
        ise_group_id (str): The ID of the new ISE endpoint group to assign.

    Returns:
        str: Rendered HTML template showing the update result (success/failure).

    Example:
        POST /update/AA:BB:CC:DD:EE:FF
        Form data: ise_group_id=aa13bb40-8bff-11e6-996c-525400b48521
    """
    ise_group_id = request.form.get("ise_group_id")
    result = ise_api.update_endpoint_group(mac, ise_group_id)
    update_result = result.status_code == 200

    return render_template("update-result.html", result=update_result)


@app.route("/endpoint", methods=["POST"])
def search_endpoint():
    """
    Search for an endpoint in ISE by MAC address.

    This route handles MAC address search requests, validates the MAC address format,
    normalizes it, and retrieves the endpoint's current group assignment from ISE.

    Form Parameters:
        mac (str): MAC address to search for (can be in any common format).

    Returns:
        str: Rendered HTML template showing endpoint information and available groups,
            or an error message if the MAC address format is invalid.

    Example:
        POST /endpoint
        Form data: mac=AA:BB:CC:DD:EE:FF
    """
    mac_check = True
    mac = request.form.get("mac")
    endpoint_group_name = "Unknown"

    # Normalize MAC address to ISE format (XXXX.XXXX.XXXX)
    normalized_mac = ise_api.mac_normalization(mac, ".")

    if normalized_mac == "Error":
        mac_check = False
        return render_template("update-mac.html", mac_check=mac_check, mac=mac)

    # Get all ISE groups and find current assignment
    ise_groups = ise_api.get_group_id()
    endpoint_group_id = ise_api.get_endpoint_group_id(mac)

    for group_id, group_name in ise_groups.items():
        if group_id == endpoint_group_id:
            endpoint_group_name = group_name
            break

    return render_template(
        "update-mac.html",
        mac_check=mac_check,
        mac=mac,
        endpoint_group_id=endpoint_group_name,
        ise_groups=ise_groups,
    )


if __name__ == "__main__":
    # Run the Flask development server
    # For production, use a WSGI server like Gunicorn or uWSGI
    app.run(debug=True, host="0.0.0.0", port=5000)
