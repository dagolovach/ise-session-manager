# ISE Switch Session Manager

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/dagolovach/webapp-ise-switch-sessions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Flask web application for managing Cisco ISE (Identity Services Engine) endpoint groups and analyzing access-session information from Cisco switches. This tool helps network administrators quickly identify authentication failures and manage endpoint group assignments.

## Features

- **Access Session Analysis**: Connect to Cisco switches and collect detailed information about failed or unauthorized authentication sessions
- **MAC Address Vendor Lookup**: Automatically identify device vendors for MAB (MAC Authentication Bypass) sessions
- **ISE Endpoint Management**: View and update endpoint group assignments in Cisco ISE
- **User-Friendly Web Interface**: Simple Flask-based UI for easy interaction
- **Secure Configuration**: Environment variable support for credential management

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Security Notes](#security-notes)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Prerequisites

- **Python**: 3.8 or higher
- **Cisco ISE**: Access to Cisco ISE with ERS API enabled
- **Cisco Switch**: IOS switch with SSH access and 802.1X/MAB configured
- **Network Access**: Connectivity to both the Cisco switch and ISE server

### Cisco ISE Requirements

1. Enable External RESTful Services (ERS) in ISE:
   - Navigate to **Administration** > **System** > **Settings** > **ERS Settings**
   - Enable **Enable ERS for Read/Write**

2. Create an ISE admin user with ERS permissions:
   - **Administration** > **System** > **Admin Access** > **Administrators** > **Admin Users**
   - Assign appropriate permissions for endpoint and endpoint group management

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/dagolovach/webapp-ise-switch-sessions.git
cd webapp-ise-switch-sessions
```

### 2. Create a Virtual Environment

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Set Up Environment Variables

Create a `.env` file in the project root directory based on the provided `.env.example`:

```bash
cp .env.example .env
```

### 2. Configure Credentials

Edit the `.env` file with your credentials:

```ini
# Cisco Switch Credentials
SWITCH_USERNAME=your_switch_username
SWITCH_PASSWORD=your_switch_password
SWITCH_SECRET=your_enable_password

# Cisco ISE Credentials
ISE_USERNAME=your_ise_username
ISE_PASSWORD=your_ise_password
ISE_BASE_URL=https://your-ise-server:9060/ers/config/

# Flask Configuration (optional)
FLASK_SECRET_KEY=your_random_secret_key_here
FLASK_ENV=development
```

**Security Note**: Never commit the `.env` file to version control. It's already included in `.gitignore`.

## Usage

### Running the Application

**Development Mode:**

```bash
export FLASK_APP=application.py
flask run
```

Or simply:

```bash
python application.py
```

The application will be available at `http://127.0.0.1:5000/`

**Production Mode:**

For production deployments, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 application:app
```

### Workflow Examples

#### 1. Analyze Switch Access Sessions

1. Navigate to the main page
2. Enter the IP address of your Cisco switch
3. Click "Check Sessions"
4. View the table of failed/unauthorized sessions with details:
   - Interface
   - MAC address
   - IP address
   - Username
   - Authentication method (MAB/DOT1X)
   - Device vendor (for MAB)
   - Session status

#### 2. Update Endpoint Group in ISE

1. From the session results, click on a MAC address
2. View the current endpoint group assignment
3. Select a new endpoint group from the dropdown
4. Click "Update Group"
5. Receive confirmation of the update

#### 3. Search by MAC Address

1. On the main page, enter a MAC address in any format:
   - `AA:BB:CC:DD:EE:FF`
   - `AABB.CCDD.EEFF`
   - `AA-BB-CC-DD-EE-FF`
2. Click "Search Endpoint"
3. View current group and update if needed

## Project Structure

```
webapp-ise-switch-sessions/
├── application.py              # Flask web application and routes
├── check_access_sessions.py    # Switch session collection logic
├── ise_api.py                  # ISE API integration
├── local.py                    # Configuration and credential loading
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
├── templates/                 # HTML templates
│   ├── main.html
│   ├── check-result.html
│   ├── update-mac.html
│   └── update-result.html
├── static/                    # Static files (CSS, JS, results)
│   └── result.json
└── flask_session/            # Server-side session storage

```

## API Reference

### Module: `ise_api.py`

#### `get_group_id() -> Dict[str, str]`
Retrieves all endpoint groups from ISE.

**Returns**: Dictionary mapping group IDs to group names

#### `get_endpoint_group_id(mac: str) -> Optional[str]`
Gets the endpoint group ID for a specific MAC address.

**Parameters**:
- `mac`: MAC address in any common format

**Returns**: Group ID string or None if not found

#### `update_endpoint_group(mac: str, ise_group_id: str) -> requests.Response`
Updates the endpoint group assignment for a MAC address.

**Parameters**:
- `mac`: MAC address to update
- `ise_group_id`: New endpoint group ID

**Returns**: HTTP response object

#### `mac_normalization(current_mac_address: str, symbol: str = ".") -> str`
Normalizes MAC address to a specific format.

**Parameters**:
- `current_mac_address`: MAC in any format
- `symbol`: Separator to use (default: ".")

**Returns**: Normalized MAC or "Error"

### Module: `check_access_sessions.py`

#### `class Device`
Represents a Cisco switch for session collection.

**Methods**:
- `init_connection_ssh()`: Establish SSH connection
- `collect_active_sessions()`: Collect all active sessions
- `collect_active_sessions_details()`: Get details for failed sessions
- `close_connection()`: Close SSH connection
- `get_result()`: Return collected session data

#### `main(current_ip_address: str) -> Dict`
Main function to orchestrate session collection.

**Parameters**:
- `current_ip_address`: Switch IP address

**Returns**: Dictionary of failed/unauthorized sessions

## Security Notes

⚠️ **Important Security Considerations**:

1. **Credentials**: Never hardcode credentials. Always use environment variables or a secure secrets management system.

2. **HTTPS**: This application connects to ISE using HTTPS but disables certificate verification (`verify=False`). For production:
   - Use valid SSL certificates
   - Enable certificate verification
   - Consider using a certificate bundle

3. **Network Access**: Run this application in a secure, controlled environment with restricted access to network devices.

4. **Authentication**: The current version doesn't include user authentication for the web interface. Consider adding:
   - Flask-Login for user authentication
   - RBAC (Role-Based Access Control)
   - HTTPS for the Flask application

5. **Input Validation**: While MAC address validation is implemented, always sanitize user inputs.

6. **Production Deployment**:
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Set `FLASK_ENV=production`
   - Use a reverse proxy (Nginx, Apache)
   - Implement rate limiting

## Development

### Code Quality

The codebase follows Python best practices:
- Comprehensive docstrings for all functions and classes
- Type hints for better code clarity
- PEP 8 style guidelines
- Modular design for maintainability

### Testing

To test the connection to a switch:

```bash
python check_access_sessions.py <switch_ip_address>
```

## Troubleshooting

### Common Issues

**SSH Connection Failures**:
- Verify network connectivity: `ping <switch_ip>`
- Confirm SSH is enabled on the switch: `show ip ssh`
- Check credentials in `.env` file

**ISE API Errors**:
- Ensure ERS is enabled in ISE
- Verify ISE credentials and permissions
- Check ISE URL format (should include port 9060)

**Certificate Warnings**:
- Expected for self-signed certificates
- Consider implementing proper certificate validation for production

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Related Resources

- **Blog Post**: [WebApp ISE Python Flask](https://dmitrygolovach.com/webapp-ise-python-flask/)
- **Demo Video**: [YouTube - How it Works](https://youtu.be/xbWCEKQG22c)
- **Related Project**: [Python and ISE Monitor Mode](https://dmitrygolovach.com/python-and-ise-monitor-mode/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

**Dmitry Golovach**

- Website: [dmitrygolovach.com](https://dmitrygolovach.com)
- Twitter: [@dagolovach](https://twitter.com/dagolovach)
- LinkedIn: [dmitrygolovach](https://www.linkedin.com/in/dmitrygolovach/)
- GitHub: [@dagolovach](https://github.com/dagolovach)

---

**Built with** 💙 **by** [Dmitry Golovach](https://dmitrygolovach.com)

*If you find this tool useful, please consider giving it a ⭐ on GitHub!*
