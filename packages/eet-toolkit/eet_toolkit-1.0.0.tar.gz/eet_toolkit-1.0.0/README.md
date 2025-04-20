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
eet-gui
```

### CLI Mode

Send emails using command line:

```bash
eet-send --config path/to/config.yaml
```

Read emails using command line:

```bash
eet-read --server imap.example.com --username user@example.com --password yourpassword
```

## Configuration

For sending emails, create a YAML configuration file:

```yaml
smtp:
  server: smtp.example.com
  port: 587
  username: user@example.com
  password: yourpassword
  use_tls: true

email:
  from: "Sender <sender@example.com>"
  to: ["recipient1@example.com", "recipient2@example.com"]
  subject: "Important Message"
  body: "This is the email body."
  html_body: "<html><body><h1>Hello</h1><p>This is HTML content</p></body></html>"
  attachments:
    - path/to/attachment1.pdf
    - path/to/attachment2.docx
```

## License

MIT License

## Author

Script1337

- Telegram: @script1337
- GitHub: https://github.com/script1337 