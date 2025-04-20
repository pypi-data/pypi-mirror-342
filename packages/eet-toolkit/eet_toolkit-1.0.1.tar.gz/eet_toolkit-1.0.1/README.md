# EET Toolkit - Email Enumeration Toolkit

A comprehensive toolkit for email operations including sending, reading, and managing emails with both GUI and CLI interfaces.

## Features

- **Email Sending**: Send emails with custom templates, attachments, and headers
- **Email Reading**: Connect to IMAP/POP3 servers to read emails and download attachments
- **User-friendly GUI**: Graphical interface for all operations
- **Command-line Interface**: Automate email tasks through CLI commands

## Installation

```bash
# Install from PyPI
pip install eet-toolkit

# Or install from source
git clone https://github.com/script1337/eet-toolkit.git
cd eet-toolkit
pip install -e .
```

## Usage

### GUI Mode

Launch the graphical interface:

```bash
eet
```

## Configuration

For sending emails, create a json configuration file:

```json
[
  {
    "username": "your_email@example.com",
    "password": "your_password",
    "server": "smtp.example.com",
    "port": 587,
    "display_name": "Your Name",
    "from_email": "your_email@example.com",
    "reply_to": "your_reply_to@example.com",
    "auth_type": "password"
  },
  {
    "username": "oauth2_email@gmail.com",
    "server": "smtp.gmail.com",
    "port": 587,
    "display_name": "OAuth2 User",
    "from_email": "oauth2_email@gmail.com",
    "reply_to": "oauth2_email@gmail.com",
    "auth_type": "oauth2",
    "oauth2": {
      "access_token": "new_sample_access_token_123",
      "refresh_token": "new_sample_refresh_token_456",
      "client_id": "your_client_id_updated",
      "client_secret": "your_client_secret_updated",
      "type": "gmail",
      "expires_at": "2025-12-31T23:59:59Z"
    }
  }
]
```

## License

MIT License

## Author

Script1337

- Telegram: @script1337
- GitHub: https://github.com/script1337 