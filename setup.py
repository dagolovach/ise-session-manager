#!/usr/bin/env python3
"""
Setup script for ISE Switch Session Manager.

This script helps with initial setup and configuration of the application.
"""

import os
import sys
import subprocess
import secrets


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python version: {sys.version.split()[0]}")


def create_env_file():
    """Create .env file from .env.example if it doesn't exist."""
    if os.path.exists(".env"):
        response = input(".env file already exists. Overwrite? (y/N): ")
        if response.lower() != "y":
            print("Skipping .env file creation.")
            return

    if not os.path.exists(".env.example"):
        print("Error: .env.example not found!")
        return

    # Generate a random secret key
    secret_key = secrets.token_hex(32)

    # Read template
    with open(".env.example", "r") as f:
        content = f.read()

    # Replace placeholder with generated secret key
    content = content.replace(
        "your_secret_key_here",
        secret_key
    )

    # Write to .env
    with open(".env", "w") as f:
        f.write(content)

    print("✓ Created .env file from .env.example")
    print("  Please edit .env and add your credentials!")


def check_virtualenv():
    """Check if running in a virtual environment."""
    in_venv = (
        hasattr(sys, "real_prefix")
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
    )

    if not in_venv:
        print("\n⚠️  Warning: Not running in a virtual environment!")
        print("   It's recommended to use a virtual environment.")
        print("   Create one with: python3 -m venv venv")
        print("   Activate with: source venv/bin/activate")
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != "y":
            sys.exit(0)
    else:
        print("✓ Running in virtual environment")


def install_dependencies():
    """Install required Python packages."""
    print("\nInstalling dependencies from requirements.txt...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies")
        sys.exit(1)


def create_directories():
    """Create necessary directories if they don't exist."""
    directories = ["static", "templates", "flask_session"]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory exists: {directory}")


def display_next_steps():
    """Display next steps for the user."""
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("\n1. Edit the .env file with your credentials:")
    print("   - SWITCH_USERNAME, SWITCH_PASSWORD, SWITCH_SECRET")
    print("   - ISE_USERNAME, ISE_PASSWORD, ISE_BASE_URL")
    print("\n2. Ensure your Cisco ISE has ERS API enabled:")
    print("   Administration > System > Settings > ERS Settings")
    print("\n3. Run the application:")
    print("   python application.py")
    print("   or")
    print("   export FLASK_APP=application.py && flask run")
    print("\n4. Access the web interface:")
    print("   http://127.0.0.1:5000/")
    print("\n" + "=" * 60)


def main():
    """Main setup function."""
    print("=" * 60)
    print("ISE Switch Session Manager - Setup")
    print("=" * 60)
    print()

    # Check Python version
    check_python_version()

    # Check if in virtual environment
    check_virtualenv()

    # Create directories
    print("\nCreating necessary directories...")
    create_directories()

    # Create .env file
    print("\nSetting up environment configuration...")
    create_env_file()

    # Install dependencies
    response = input("\nInstall Python dependencies? (Y/n): ")
    if response.lower() != "n":
        install_dependencies()
    else:
        print("Skipping dependency installation.")

    # Display next steps
    display_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during setup: {e}")
        sys.exit(1)
