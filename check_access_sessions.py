#!/usr/bin/env python3
"""
Cisco Switch Access Session Collector.

This module provides functionality to collect and analyze access-session information
from Cisco switches. It identifies failed or unauthorized sessions and gathers detailed
information about each endpoint including MAC address, IP address, authentication method,
and vendor information.

Classes:
    Device: Represents a network device and provides methods to collect session information.

Functions:
    try_to_connect_ssh: Establish an SSH connection to a Cisco device.
    main: Main entry point for collecting access session information.
"""

import re
import time
import pprint
from typing import Dict, List, Optional
import paramiko
import netmiko
import requests
from local import switch_credentials


def try_to_connect_ssh(current_ip_address: str) -> Optional[netmiko.ConnectHandler]:
    """
    Attempt to establish an SSH connection to a Cisco device.

    Args:
        current_ip_address (str): IP address of the Cisco switch to connect to.

    Returns:
        Optional[netmiko.ConnectHandler]: Connected device handler in enable mode,
            or None if connection fails.

    Raises:
        None: Exceptions are caught and printed, returns None on failure.

    Example:
        >>> connection = try_to_connect_ssh('192.168.1.1')
        >>> if connection:
        ...     print("Connected successfully")
    """
    try:
        connection = netmiko.ConnectHandler(
            device_type="cisco_ios_ssh",
            ip=current_ip_address,
            username=switch_credentials["username"],
            password=switch_credentials["password"],
            secret=switch_credentials["secret"],
        )
        connection.enable()
        return connection
    except paramiko.AuthenticationException:
        print(f"Authentication failed for {current_ip_address}")
        return None
    except netmiko.NetmikoTimeoutException:
        print(f"Connection timeout for {current_ip_address}")
        return None
    except netmiko.NetmikoAuthenticationException:
        print(f"Authentication failed for {current_ip_address}")
        return None
    except Exception as e:
        print(f"Connection failed for {current_ip_address}: {str(e)}")
        return None


class Device:
    """
    Represents a Cisco network device for collecting access session information.

    This class provides methods to connect to a Cisco switch, collect active authentication
    sessions, and gather detailed information about failed or unauthorized sessions.

    Attributes:
        current_ip_address (str): IP address of the device.
        connection (netmiko.ConnectHandler): SSH connection handler.
        session_count (List[str]): List containing the total session count.
        mac_addresses (List[str]): List of MAC addresses with active sessions.
        dict_result (Dict): Dictionary containing session details for failed/unauthorized sessions.

    Example:
        >>> device = Device('192.168.1.1')
        >>> device.init_connection_ssh()
        >>> device.collect_active_sessions()
        >>> device.collect_active_sessions_details()
        >>> results = device.get_result()
        >>> device.close_connection()
    """

    def __init__(self, current_ip_address: str):
        """
        Initialize a Device instance.

        Args:
            current_ip_address (str): IP address of the Cisco switch.
        """
        self.current_ip_address = current_ip_address
        self.dict_result: Dict = {}
        self.connection: Optional[netmiko.ConnectHandler] = None
        self.session_count: List[str] = []
        self.mac_addresses: List[str] = []

    def init_connection_ssh(self) -> None:
        """
        Initialize SSH connection to the device.

        Establishes an SSH connection and enters enable mode.

        Raises:
            ConnectionError: If the connection cannot be established.
        """
        self.connection = try_to_connect_ssh(self.current_ip_address)
        if not self.connection:
            raise ConnectionError(
                f"Failed to connect to device at {self.current_ip_address}"
            )

    def close_connection(self) -> None:
        """
        Close the SSH connection to the device.

        This method should be called when finished collecting information
        to properly clean up the connection.
        """
        if self.connection:
            self.connection.disconnect()

    def collect_active_sessions(self) -> None:
        """
        Collect all active MAC addresses from access-sessions on the switch.

        This method executes 'show access-session' and extracts:
        - Total session count
        - All MAC addresses with active authentication sessions

        The results are stored in instance attributes:
        - self.session_count: List with total session count
        - self.mac_addresses: List of MAC addresses in format XXXX.XXXX.XXXX

        Raises:
            AttributeError: If connection is not initialized.
        """
        if not self.connection:
            raise AttributeError("Connection not initialized. Call init_connection_ssh first.")

        self.connection.send_command("term len 0")
        active_sessions = self.connection.send_command("show access-session")
        self.session_count = re.findall(r"Session count = (\d+)\n", active_sessions)
        self.mac_addresses = re.findall(
            r"[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}", active_sessions
        )

    def collect_active_sessions_details(self) -> None:
        """
        Collect detailed information for sessions with failures or unauthorized status.

        For each active session, this method checks if there are any FAIL or Unauthorized
        indicators. If found, it collects comprehensive session details including:
        - Interface
        - MAC address
        - IP address (if available)
        - Username
        - Authentication method (MAB/DOT1X)
        - Vendor information (for MAB sessions)

        The results are stored in self.dict_result with MAC address as keys.

        Note:
            This method includes a 1-second delay when querying vendor information
            to respect the rate limits of the MAC vendor API.

        Raises:
            AttributeError: If connection is not initialized or sessions not collected.

        Example result:
            {
                '0050.5699.1234': {
                    'interface': 'GigabitEthernet1/0/1',
                    'ip_address': '192.168.1.100',
                    'mac_address': '0050.5699.1234',
                    'method': 'mab',
                    'status': 'Authz Failed',
                    'user_name': '00-50-56-99-12-34',
                    'vendor': 'VMware, Inc.'
                }
            }
        """
        if not self.connection:
            raise AttributeError("Connection not initialized. Call init_connection_ssh first.")

        dict_result = {}

        for each in self.mac_addresses:
            session_details = self.connection.send_command(
                f"show access-session mac {each} details"
            )

            # Check if session has failures or unauthorized status
            if "FAIL" in session_details or "Unauthorized" in session_details:
                mac_address = re.findall(
                    r"[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}",
                    session_details,
                )
                ip_address = re.findall(
                    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", session_details
                )
                method = re.findall(r"(\w{3,5})\s+Authc\s.*", session_details)
                status = re.findall(r"Status:  (.*)", session_details)

                dict_session_details = {}
                dict_session_details["status"] = status[0] if status else "Unknown"
                interface_match = re.findall(r"Interface: (.*)", session_details)
                dict_session_details["interface"] = (
                    interface_match[0] if interface_match else "Unknown"
                )
                dict_session_details["mac_address"] = mac_address[0] if mac_address else each

                # Handle IP address (may not always be present)
                if ip_address:
                    dict_session_details["ip_address"] = ip_address[0]
                else:
                    dict_session_details["ip_address"] = "unknown"

                username_match = re.findall(r"User-Name:\s+(.*)", session_details)
                dict_session_details["user_name"] = (
                    username_match[0] if username_match else "Unknown"
                )
                dict_session_details["method"] = method[0] if method else "Unknown"

                # For MAB sessions, query vendor information
                if method and method[0].lower() == "mab":
                    try:
                        url = f"https://api.macvendors.com/{mac_address[0]}"
                        response = requests.get(url, timeout=5)
                        if response.status_code == 200:
                            dict_session_details["vendor"] = response.text
                        else:
                            dict_session_details["vendor"] = "Unknown"
                        # Rate limiting - API allows 1 request per second
                        time.sleep(1)
                    except requests.exceptions.RequestException:
                        dict_session_details["vendor"] = "Unknown"

                self.dict_result[each] = dict_session_details

    def get_result(self) -> Dict:
        """
        Get the collected session details.

        Returns:
            Dict: Dictionary containing details of failed/unauthorized sessions.
                Keys are MAC addresses, values are dictionaries with session details.
        """
        return self.dict_result


def main(current_ip_address: str) -> Dict:
    """
    Main function to collect access session information from a Cisco switch.

    This function orchestrates the entire process of:
    1. Connecting to the switch
    2. Collecting active sessions
    3. Gathering detailed information for failed/unauthorized sessions
    4. Saving results to a JSON file
    5. Closing the connection

    Args:
        current_ip_address (str): IP address of the Cisco switch.

    Returns:
        Dict: Dictionary containing session details for failed/unauthorized sessions.
            Format: {mac_address: {session_details}}

    Example:
        >>> results = main('192.168.1.1')
        >>> for mac, details in results.items():
        ...     print(f"MAC: {mac}, Status: {details['status']}")
    """
    start_time = time.time()

    device = Device(current_ip_address)
    device.init_connection_ssh()
    device.collect_active_sessions()
    device.collect_active_sessions_details()
    dict_result = device.get_result()
    device.close_connection()

    # Save results to file
    with open("static/result.json", "w", encoding="utf-8") as f:
        pprint.PrettyPrinter(stream=f).pprint(dict_result)

    elapsed_time = time.time() - start_time
    print(f"Completed in {elapsed_time:.2f} seconds")

    return dict_result


if __name__ == "__main__":
    # Example usage - replace with actual switch IP
    # For production use, consider using command-line arguments
    import sys

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: python check_access_sessions.py <switch_ip_address>")
        print("Example: python check_access_sessions.py 192.168.1.1")
