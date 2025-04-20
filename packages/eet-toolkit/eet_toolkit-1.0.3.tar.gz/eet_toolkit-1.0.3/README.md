# EET Toolkit - Email Enumeration Toolkit

A comprehensive toolkit for email operations including sending, reading, and managing emails with both GUI interfaces.

## Features

- **Email Sending**: Send emails with custom templates, attachments, and headers
- **Email Reading**: Connect to IMAP/POP3 servers to read emails and download attachments
- **User-friendly GUI**: Graphical interface for all operations

## Installation

```bash
# Install from PyPI
pip install eet-toolkit
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

## System Requirements

### Linux Dependencies
When running on Linux, you may need to install additional XCB libraries for the Qt GUI to work properly:

#### For Debian/Ubuntu/Mint:
```bash
sudo apt install libxcb-cursor0 libxcb-xinerama0 libxcb-randr0
sudo apt install libxcb-xtest0 libxcb-shape0 libxcb-xkb1 libxkbcommon-x11-0
```

#### For Fedora/RHEL:
```bash
sudo dnf install libxcb libxcb-cursor libxkbcommon-x11
```

If you encounter "Could not load the Qt platform plugin xcb" errors, installing these packages should resolve the issue. 