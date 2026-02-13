# Security Policy

## Supported Versions

Currently supported versions of this project:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest| :x:                |

## Reporting a Vulnerability

We take the security of ISE Switch Session Manager seriously. If you discover a security vulnerability, please follow these guidelines:

### How to Report

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by:

1. **Email**: Send details to the project maintainer
2. **GitHub Security Advisory**: Use GitHub's security advisory feature (preferred)
   - Go to the repository's "Security" tab
   - Click "Report a vulnerability"
   - Fill in the details

### What to Include

When reporting a vulnerability, please include:

- **Description**: A clear description of the vulnerability
- **Impact**: Potential impact of the vulnerability
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Proof of Concept**: If possible, provide a PoC (without causing harm)
- **Suggested Fix**: If you have ideas on how to fix it

### Response Timeline

- **Initial Response**: Within 48 hours of receiving your report
- **Status Update**: Within 7 days with our assessment
- **Fix Timeline**: Depends on severity and complexity

### Disclosure Policy

- We ask that you do not publicly disclose the vulnerability until we've had a chance to address it
- Once a fix is available, we will:
  1. Release a security patch
  2. Credit you for the discovery (if you wish)
  3. Publish a security advisory

## Security Best Practices

### For Users

When deploying this application:

1. **Credentials**:
   - Never commit credentials to version control
   - Use strong, unique passwords
   - Rotate credentials regularly
   - Use environment variables for all sensitive data

2. **Network Security**:
   - Deploy in a secure, isolated network segment
   - Use firewalls to restrict access
   - Enable TLS/HTTPS for all communications
   - Consider VPN access for remote management

3. **Application Security**:
   - Run with minimal required permissions
   - Use a production WSGI server (not Flask development server)
   - Implement rate limiting
   - Add authentication/authorization to the web interface
   - Keep dependencies updated

4. **ISE Security**:
   - Create dedicated ISE admin accounts with minimal permissions
   - Use certificate-based authentication when possible
   - Enable and monitor ISE audit logs
   - Validate SSL certificates in production

5. **Switch Security**:
   - Use dedicated service accounts
   - Implement SSH key-based authentication
   - Enable and monitor switch logging
   - Restrict SSH access by source IP

### For Developers

When contributing:

1. **Input Validation**:
   - Validate all user inputs
   - Sanitize data before use
   - Use parameterized queries (if applicable)

2. **Dependencies**:
   - Keep dependencies updated
   - Review security advisories
   - Use tools like `pip-audit` or `safety`

3. **Code Review**:
   - Review code for security issues
   - Look for injection vulnerabilities
   - Check for insecure defaults

4. **Secrets**:
   - Never commit secrets, API keys, or passwords
   - Use `.env` for local development
   - Review commits before pushing

## Known Security Considerations

### Current Limitations

1. **SSL Verification**:
   - The application currently disables SSL certificate verification for ISE API calls
   - **Recommendation**: Implement proper certificate validation in production

2. **Web Authentication**:
   - No built-in authentication for the web interface
   - **Recommendation**: Add Flask-Login or similar for production deployments

3. **API Rate Limiting**:
   - No rate limiting on API calls
   - **Recommendation**: Implement rate limiting for production

4. **Session Management**:
   - Uses filesystem-based sessions
   - **Recommendation**: Consider Redis or database-backed sessions for production

5. **Input Validation**:
   - Limited input validation on some routes
   - **Recommendation**: Implement comprehensive input validation

## Security Checklist for Production

Before deploying to production:

- [ ] Environment variables configured for all credentials
- [ ] SSL/TLS enabled for all connections
- [ ] Certificate validation enabled
- [ ] Web application authentication implemented
- [ ] Rate limiting configured
- [ ] Logging and monitoring in place
- [ ] Network segmentation implemented
- [ ] Firewall rules configured
- [ ] Regular security updates scheduled
- [ ] Incident response plan documented

## Dependencies Security

We regularly monitor our dependencies for security vulnerabilities. To check for vulnerabilities:

```bash
# Using pip-audit
pip install pip-audit
pip-audit

# Using safety
pip install safety
safety check
```

## Updates and Patches

Security updates will be:
- Released as soon as possible
- Documented in release notes
- Announced through GitHub releases
- Tagged with severity level

## Contact

For security-related questions or concerns:
- Review this security policy
- Check the README for general information
- Open a security advisory for vulnerabilities
- Contact the maintainer for other security questions

---

Thank you for helping keep ISE Switch Session Manager secure!
