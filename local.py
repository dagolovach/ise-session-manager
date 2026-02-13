"""
Configuration file for storing credentials.

This module loads credentials from environment variables for better security.
For local development, create a .env file based on .env.example.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Cisco Switch credentials
switch_credentials = {
    "username": os.getenv("SWITCH_USERNAME", "admin"),
    "password": os.getenv("SWITCH_PASSWORD", ""),
    "secret": os.getenv("SWITCH_SECRET", ""),
}

# Cisco ISE credentials
ise_credentials = {
    "username": os.getenv("ISE_USERNAME", "admin"),
    "password": os.getenv("ISE_PASSWORD", ""),
    "base_url": os.getenv("ISE_BASE_URL", "https://localhost:9060/ers/config/"),
}


def validate_credentials():
    """
    Validate that all required credentials are configured.

    Raises:
        ValueError: If any required credential is missing.
    """
    required_switch = ["username", "password", "secret"]
    required_ise = ["username", "password", "base_url"]

    for key in required_switch:
        if not switch_credentials.get(key):
            raise ValueError(f"Missing required switch credential: {key}")

    for key in required_ise:
        if not ise_credentials.get(key):
            raise ValueError(f"Missing required ISE credential: {key}")
