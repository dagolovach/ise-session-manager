"""
Cisco ISE API Integration Module.

This module provides functions to interact with Cisco Identity Services Engine (ISE)
External RESTful Services (ERS) API for endpoint and endpoint group management.

Functions:
    get_group_id: Retrieve all endpoint group IDs and names from ISE.
    get_endpoint_group_id: Get the endpoint group ID for a specific MAC address.
    update_endpoint_group: Update the endpoint group assignment for a MAC address.
    mac_normalization: Normalize MAC address to a specific format.
"""

import re
from typing import Dict, Optional
import requests
from requests.auth import HTTPBasicAuth
from local import ise_credentials

# Disable InsecureRequestWarning due to self-signed certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# API request headers
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# ISE credentials
USER = ise_credentials["username"]
PASSWORD = ise_credentials["password"]
BASE_URL = ise_credentials["base_url"]


def get_group_id() -> Dict[str, str]:
    """
    Retrieve all endpoint group IDs from Cisco ISE.

    This function queries the ISE ERS API to get all configured endpoint groups,
    handling pagination automatically to retrieve all available groups.

    Returns:
        Dict[str, str]: A dictionary mapping group IDs to group names.
            Example: {'aa0e8b20-8bff-11e6-996c-525400b48521': 'Blacklist'}

    Raises:
        requests.exceptions.RequestException: If the API request fails.

    Example:
        >>> groups = get_group_id()
        >>> print(groups)
        {'aa0e8b20-8bff-11e6-996c-525400b48521': 'Blacklist',
         'aa13bb40-8bff-11e6-996c-525400b48521': 'GuestEndpoints'}
    """
    url = BASE_URL + "endpointgroup"
    payload = {}
    ise_groups = {}

    while True:
        response = requests.request(
            "GET",
            url,
            auth=HTTPBasicAuth(USER, PASSWORD),
            headers=HEADERS,
            data=payload,
            verify=False,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        for each in data["SearchResult"]["resources"]:
            ise_groups[each["id"]] = each["name"]

        # Check if there are more pages
        if data["SearchResult"]["nextPage"]["href"]:
            url = data["SearchResult"]["nextPage"]["href"]
            continue
        else:
            break

    return ise_groups


def get_endpoint_group_id(mac: str) -> Optional[str]:
    """
    Get the endpoint group ID for a specific MAC address.

    Args:
        mac (str): MAC address of the endpoint. Can be in any common format
            (e.g., 'AA:BB:CC:DD:EE:FF', 'AABB.CCDD.EEFF', 'aabbccddeeff').

    Returns:
        Optional[str]: The endpoint group ID if found, None if endpoint doesn't exist.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
        KeyError: If the response doesn't contain expected data.

    Example:
        >>> group_id = get_endpoint_group_id('AA:BB:CC:DD:EE:FF')
        >>> print(group_id)
        'aa0e8b20-8bff-11e6-996c-525400b48521'
    """
    url = BASE_URL + "endpoint/name/" + mac
    payload = {}

    try:
        response = requests.request(
            "GET",
            url,
            auth=HTTPBasicAuth(USER, PASSWORD),
            headers=HEADERS,
            data=payload,
            verify=False,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        endpoint_group_id = data["ERSEndPoint"]["groupId"]
        return endpoint_group_id
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return None
        raise


def update_endpoint_group(mac: str, ise_group_id: str) -> requests.Response:
    """
    Update the endpoint group assignment in ISE for a specific MAC address.

    This function first retrieves the endpoint ID, then updates its group assignment
    with static group assignment enabled.

    Args:
        mac (str): MAC address of the endpoint to update.
        ise_group_id (str): The ID of the new ISE endpoint group to assign.

    Returns:
        requests.Response: The HTTP response object from the PUT request.
            Status code 200 indicates success.

    Raises:
        requests.exceptions.RequestException: If the API request fails.

    Example:
        >>> response = update_endpoint_group('AA:BB:CC:DD:EE:FF',
        ...                                  'aa13bb40-8bff-11e6-996c-525400b48521')
        >>> print(response.status_code)
        200
    """
    # First, get the endpoint ID
    url = BASE_URL + "endpoint/name/" + mac
    payload = {}

    response = requests.request(
        "GET",
        url,
        auth=HTTPBasicAuth(USER, PASSWORD),
        headers=HEADERS,
        data=payload,
        verify=False,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    endpoint_id = data["ERSEndPoint"]["id"]

    # Update the endpoint group
    url = BASE_URL + "endpoint/" + endpoint_id
    payload = {
        "ERSEndPoint": {
            "groupId": ise_group_id,
            "staticGroupAssignment": "true"
        }
    }

    response = requests.request(
        "PUT",
        url,
        auth=HTTPBasicAuth(USER, PASSWORD),
        headers=HEADERS,
        json=payload,
        verify=False,
        timeout=30,
    )
    return response


def mac_normalization(current_mac_address: str, symbol: str = ".") -> str:
    """
    Normalize a MAC address to a specific format.

    This function strips all non-alphanumeric characters from a MAC address
    and reformats it with the specified separator symbol, splitting it into
    groups of 4 characters (e.g., 'AABB.CCDD.EEFF').

    Args:
        current_mac_address (str): MAC address in any format
            (e.g., 'AA:BB:CC:DD:EE:FF', 'AABB-CCDD-EEFF').
        symbol (str, optional): Separator symbol to use. Defaults to '.'.

    Returns:
        str: Normalized MAC address in format 'XXXX.XXXX.XXXX' (or with custom symbol),
            or 'Error' if the MAC address is invalid.

    Example:
        >>> mac_normalization('AA:BB:CC:DD:EE:FF', '.')
        'AABB.CCDD.EEFF'
        >>> mac_normalization('aa-bb-cc-dd-ee-ff', ':')
        'AABB:CCDD:EEFF'
        >>> mac_normalization('invalid', '.')
        'Error'
    """
    # Remove all non-alphanumeric characters
    current_mac_address = re.sub(r"\W+", "", current_mac_address)

    # Check if we have exactly 12 hex characters
    if len(current_mac_address) == 12:
        return symbol.join(
            [
                current_mac_address[i : i + 4]
                for i in range(0, len(current_mac_address), 4)
            ]
        )

    return "Error"
