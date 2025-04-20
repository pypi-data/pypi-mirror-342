#!/usr/bin/env python3
import smtplib
import ssl
import argparse
import os
import sys
import time
import random
import json
import datetime
import string
import uuid
import re
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate, make_msgid
from email import encoders
from pathlib import Path
try:
    import socks  # PySocks
except ImportError:
    # Try alternate import
    from PySocks import socks
import socket
import base64
import logging
import hashlib
import email.utils
import imaplib
import poplib
import email
from email.header import decode_header
from email import policy
import quopri

# Add imports for OAuth2 support
import requests
try:
    # For OAuth2 SMTP authentication (both Gmail and Outlook)
    import base64
    HAS_OAUTH2_SUPPORT = True
except ImportError:
    HAS_OAUTH2_SUPPORT = False

VERSION = "1.0.0"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('mailer.log')
    ]
)
logger = logging.getLogger('redmailer')

# Known mail server signatures for impersonation
MAIL_SERVER_SIGNATURES = {
    "outlook": {
        "X-Mailer": "Microsoft Outlook 16.0",
        "X-MS-Has-Attach": "yes",
        "X-MS-TNEF-Correlator": "",
        "x-originating-ip": "[40.94.25.100]",
        "X-Microsoft-Antispam-Mailbox-Delivery": "ucf:0;jmr:0;auth:0;dest:I;ENG:(910001)(944506458)(944626604)(920097)(930097)",
        "X-Microsoft-Antispam-Message-Info": "{random_hash}"
    },
    "gmail": {
        "X-Google-DKIM-Signature": "v=1; a=rsa-sha256; c=relaxed/relaxed; d=1e100.net; s=20161025; h=x-gm-message-state:sender:from:to:subject:thread-topic:thread-index; bh={random_hash}",
        "X-Gm-Message-State": "{random_hash}",
        "X-Google-Smtp-Source": "{random_string}",
        "X-Received": "by 2002:a05:6102:15b3:b0:413:5dcc:2bef with SMTP id {random_string}"
    },
    "yahoo": {
        "X-YMail-OSG": "{random_hash}",
        "X-Mailer": "YahooMailWebService/0.8.1013.11",
        "X-Yahoo-SMTP": "{random_string}@yahoo.com"
    },
    "office365": {
        "X-MS-Exchange-Organization-AuthSource": "DM6PR03MB5196.namprd03.prod.outlook.com",
        "X-MS-Exchange-Organization-AuthAs": "Internal",
        "X-MS-Exchange-Organization-AuthMechanism": "04",
        "X-MS-Exchange-Organization-Network-Message-Id": "{random_uuid}",
        "X-MS-Office365-Filtering-Correlation-Id": "{random_uuid}"
    },
    "protonmail": {
        "X-Pm-Origin": "internal",
        "X-Pm-Content-Encryption": "end-to-end",
        "X-Pm-Spamscore": "0"
    },
    "zoho": {
        "X-ZohoMail": "1",
        "X-Mailer": "Zoho Mail",
        "X-ZohoMail-Sender": "{random_string}"
    }
}

# Common subject prefixes for randomization
SUBJECT_PREFIXES = [
    "Re: ", "Fwd: ", "RE: ", "FW: ", "FWD: ", "", "ATTN: ",
    "Important: ", "Urgent: ", "Follow-up: ", "Update: "
]

# Common subject suffixes for randomization
SUBJECT_SUFFIXES = [
    "", " (Updated)", " - Please Review", " - Action Required",
    " (New)", " [Confidential]", " - Confirmation", " (!)"
]

# HTML comment patterns for insertion
HTML_COMMENTS = [
    "<!-- -->",
    "<!-- {random_string} -->",
    "<!-- Generated on {date} -->",
    "<!-- ID: {random_id} -->",
    "<!-- User: {email} -->",
    "<!-- Version: {random_version} -->"
]

# Advanced random data generators for placeholders
def random_order_id(format_str="ORD-{year}{month}{day}-{random}"):
    """Generate a random order ID using the specified format"""
    now = datetime.datetime.now()
    placeholders = {
        'year': now.strftime('%Y'),
        'month': now.strftime('%m'),
        'day': now.strftime('%d'),
        'hour': now.strftime('%H'),
        'minute': now.strftime('%M'),
        'second': now.strftime('%S'),
        'random': random_string(6).upper(),
        'digits': str(random_with_N_digits(6))
    }
    
    # Replace all placeholders in the format string
    result = format_str
    for key, value in placeholders.items():
        result = result.replace('{' + key + '}', value)
    
    return result

def random_tracking_id(format_str="TRK{digits}-{random}"):
    """Generate a random tracking ID using the specified format"""
    placeholders = {
        'digits': str(random_with_N_digits(8)),
        'random': random_string(4).upper(),
        'hex': random_hash(8),
        'uuid': str(uuid.uuid4()).replace('-', '')[:12]
    }
    
    # Replace all placeholders in the format string
    result = format_str
    for key, value in placeholders.items():
        result = result.replace('{' + key + '}', value)
    
    return result

def random_invoice_number(format_str="INV-{year}{month}-{digits}"):
    """Generate a random invoice number using the specified format"""
    now = datetime.datetime.now()
    placeholders = {
        'year': now.strftime('%Y'),
        'month': now.strftime('%m'),
        'day': now.strftime('%d'),
        'digits': str(random_with_N_digits(6)),
        'random': random_string(4).upper()
    }
    
    # Replace all placeholders in the format string
    result = format_str
    for key, value in placeholders.items():
        result = result.replace('{' + key + '}', value)
    
    return result

def random_timestamp(format_str="%Y-%m-%d %H:%M:%S", delta_days=0, delta_hours=0):
    """Generate a random timestamp with the specified format and offset"""
    base_time = datetime.datetime.now() + datetime.timedelta(days=delta_days, hours=delta_hours)
    return base_time.strftime(format_str)

def random_ip_address():
    """Generate a random IP address"""
    octets = [str(random.randint(1, 254)) for _ in range(4)]
    return ".".join(octets)

def random_user_agent():
    """Generate a random user agent string"""
    chrome_versions = ["70.0.3538.110", "74.0.3729.131", "79.0.3945.88", "83.0.4103.116", "87.0.4280.88", "91.0.4472.124"]
    firefox_versions = ["65.0", "68.0", "73.0", "78.0", "84.0", "89.0"]
    os_strings = [
        "Windows NT 10.0; Win64; x64",
        "Windows NT 6.1; Win64; x64",
        "Macintosh; Intel Mac OS X 10_15_7",
        "Macintosh; Intel Mac OS X 10_14_6",
        "X11; Linux x86_64"
    ]
    
    browser_type = random.choice(["chrome", "firefox"])
    
    if browser_type == "chrome":
        version = random.choice(chrome_versions)
        os_string = random.choice(os_strings)
        return f"Mozilla/5.0 ({os_string}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
    else:
        version = random.choice(firefox_versions)
        os_string = random.choice(os_strings)
        return f"Mozilla/5.0 ({os_string}; rv:{version}) Gecko/20100101 Firefox/{version}"

def random_credit_card_masked():
    """Generate a random masked credit card number"""
    card_types = ["VISA", "MASTERCARD", "AMEX", "DISCOVER"]
    card_type = random.choice(card_types)
    
    if card_type == "AMEX":
        return f"XXXX-XXXXXX-X{random_with_N_digits(4)}"
    else:
        return f"XXXX-XXXX-XXXX-{random_with_N_digits(4)}"

def random_phone_number(format_str="+1 ({area}) {prefix}-{line}"):
    """Generate a random phone number using the specified format"""
    area_code = str(random.randint(201, 999))
    prefix = str(random.randint(200, 999))
    line = str(random.randint(1000, 9999))
    
    placeholders = {
        'area': area_code,
        'prefix': prefix,
        'line': line
    }
    
    # Replace all placeholders in the format string
    result = format_str
    for key, value in placeholders.items():
        result = result.replace('{' + key + '}', value)
    
    return result

def random_name():
    """Generate a random full name"""
    first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
                  "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"]
    
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
                 "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White"]
    
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_company_name():
    """Generate a random company name"""
    adjectives = ["Global", "Advanced", "Strategic", "Innovative", "Dynamic", "Premier", "Elite", "Reliable", "Professional", "United"]
    nouns = ["Solutions", "Systems", "Technologies", "Enterprises", "Industries", "Services", "Associates", "Consulting", "Group", "Corporation"]
    
    if random.random() > 0.7:
        # Sometimes use a simpler "[Adjective] [Noun]" pattern
        return f"{random.choice(adjectives)} {random.choice(nouns)}"
    else:
        # Otherwise use a more complex format with initials
        init1 = random.choice(string.ascii_uppercase)
        init2 = random.choice(string.ascii_uppercase)
        return f"{init1}{init2} {random.choice(nouns)}"

def random_with_N_digits(n):
    """Generate a random number with N digits"""
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)

def random_string(length=8):
    """Generate a random string of specified length"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def random_hash(length=32):
    """Generate a random hash-like string"""
    data = str(random.random()) + str(time.time())
    hash_obj = hashlib.md5(data.encode())
    return hash_obj.hexdigest()[:length]

def random_uuid():
    """Generate a random UUID string"""
    return str(uuid.uuid4())

def random_version():
    """Generate a random version number"""
    major = random.randint(1, 5)
    minor = random.randint(0, 10)
    patch = random.randint(0, 99)
    return f"{major}.{minor}.{patch}"

# Constants for placeholder types
PLACEHOLDER_PATTERNS = {
    # Basic placeholders
    "{{email}}": "target_email",
    "{{email_address}}": "target_email",
    "{{date}}": lambda: datetime.datetime.now().strftime("%Y-%m-%d"),
    "{{time}}": lambda: datetime.datetime.now().strftime("%H:%M:%S"),
    "{{datetime}}": lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "{{random}}": lambda: str(random_with_N_digits(6)),
    "{{random_string}}": lambda: random_string(8),
    "{{random_id}}": lambda: random_hash(16),
    "{{uuid}}": lambda: random_uuid(),
    
    # Advanced placeholders
    "{{order_id}}": lambda: random_order_id(),
    "{{tracking_id}}": lambda: random_tracking_id(),
    "{{invoice_number}}": lambda: random_invoice_number(),
    "{{timestamp}}": lambda: random_timestamp(),
    "{{timestamp_tomorrow}}": lambda: random_timestamp(delta_days=1),
    "{{timestamp_yesterday}}": lambda: random_timestamp(delta_days=-1),
    "{{ip_address}}": lambda: random_ip_address(),
    "{{user_agent}}": lambda: random_user_agent(),
    "{{credit_card}}": lambda: random_credit_card_masked(),
    "{{phone}}": lambda: random_phone_number(),
    "{{name}}": lambda: random_name(),
    "{{company}}": lambda: random_company_name(),
    
    # Date and time components
    "{{year}}": lambda: datetime.datetime.now().strftime("%Y"),
    "{{month}}": lambda: datetime.datetime.now().strftime("%m"),
    "{{day}}": lambda: datetime.datetime.now().strftime("%d"),
    "{{hour}}": lambda: datetime.datetime.now().strftime("%H"),
    "{{minute}}": lambda: datetime.datetime.now().strftime("%M"),
    "{{second}}": lambda: datetime.datetime.now().strftime("%S"),
    
    # Customizable placeholders with parameters - these will be handled separately
    # Examples:
    # {{random_string:12}} - Random string with length 12
    # {{random_digits:4}} - Random number with 4 digits
    # {{timestamp:%Y-%m-%-d}} - Timestamp with custom format
}

# Add to the PLACEHOLDER_PATTERNS dictionary
PLACEHOLDER_PATTERNS.update({
    "{{prefix}}": lambda: random.choice(SUBJECT_PREFIXES),
    "{{suffix}}": lambda: random.choice(SUBJECT_SUFFIXES),
    "{{random_comment}}": lambda: f"<!-- {random_string(12)} -->",
    "{{random_attributes}}": lambda: f'data-id="{random_hash(8)}" data-t="{int(time.time())}"',
    "{{random_class}}": lambda: f"c-{random_string(4)}",
    "{{invisible_content}}": lambda: f'<span style="display:none">{random_string(random.randint(5, 20))}</span>',
    "{{random_marker}}": lambda: f"[ID:{random_hash(8)}]",
    "{{random_line}}": lambda: random_string(random.randint(10, 30)),
    "{{random_space}}": lambda: ' ' * random.randint(1, 5)
})

def load_accounts(accounts_file):
    """Load email accounts from a JSON file"""
    try:
        with open(accounts_file, 'r') as f:
            accounts = json.load(f)
        
        # Validate required fields and normalize account data
        for i, account in enumerate(accounts):
            # Check if required fields are present
            required_fields = ["username", "server", "port"]
            for field in required_fields:
                if field not in account:
                    logger.error(f"Account {i+1} is missing required field: {field}")
                    sys.exit(1)
            
            # Determine authentication type (password or oauth2)
            if "auth_type" in account and account["auth_type"].lower() == "oauth2":
                # OAuth2 authentication
                account["auth_type"] = "oauth2"
                
                # Check if OAuth2 section exists
                if "oauth2" not in account:
                    logger.error(f"Account {i+1} has auth_type 'oauth2' but is missing oauth2 configuration")
                    sys.exit(1)
                
                oauth2_config = account["oauth2"]
                
                # Check required OAuth2 fields
                oauth2_required = ["type"]
                for field in oauth2_required:
                    if field not in oauth2_config:
                        logger.error(f"Account {i+1}'s oauth2 config is missing required field: {field}")
                        sys.exit(1)
                
                # Check if we have either access_token or refresh_token with client credentials
                if "access_token" not in oauth2_config and ("refresh_token" not in oauth2_config or 
                                                          "client_id" not in oauth2_config or 
                                                          "client_secret" not in oauth2_config):
                    logger.error(f"Account {i+1}'s oauth2 config must have either access_token or refresh_token with client credentials")
                    sys.exit(1)
            else:
                # Default to password authentication
                account["auth_type"] = "password"
                
                # Check if password is present for password auth
                if "password" not in account:
                    logger.error(f"Account {i+1} uses password authentication but is missing password field")
                    sys.exit(1)
        
        logger.info(f"Loaded {len(accounts)} email accounts")
        return accounts
    except Exception as e:
        logger.error(f"Failed to load accounts file: {e}")
        sys.exit(1)

def load_targets(targets_file):
    """Load target email addresses from a file"""
    try:
        with open(targets_file, 'r') as f:
            targets = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        logger.info(f"Loaded {len(targets)} target email addresses")
        return targets
    except Exception as e:
        logger.error(f"Failed to load targets file: {e}")
        sys.exit(1)

def load_template(template_file):
    """Load email template from a file"""
    try:
        with open(template_file, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        logger.error(f"Failed to load template file: {e}")
        sys.exit(1)

def setup_proxy(proxy_type, proxy_host, proxy_port, proxy_username=None, proxy_password=None):
    """Set up a proxy for connections"""
    if proxy_type.lower() == "socks4":
        socks_type = socks.SOCKS4
    elif proxy_type.lower() == "socks5":
        socks_type = socks.SOCKS5
    elif proxy_type.lower() == "http":
        socks_type = socks.HTTP
    else:
        logger.error(f"Unsupported proxy type: {proxy_type}")
        sys.exit(1)
    
    # Create a socket factory that uses SOCKS
    socks.set_default_proxy(
        socks_type, 
        proxy_host, 
        proxy_port,
        username=proxy_username,
        password=proxy_password
    )
    socket.socket = socks.socksocket
    logger.info(f"Proxy configured: {proxy_type} {proxy_host}:{proxy_port}")

def generate_oauth2_string(username, access_token, base64_encode=True):
    """Generate the OAUTH2 string for SMTP authentication."""
    auth_string = f"user={username}\1auth=Bearer {access_token}\1\1"
    if base64_encode:
        auth_string = base64.b64encode(auth_string.encode()).decode()
    return auth_string

def refresh_gmail_token(refresh_token, client_id, client_secret):
    """Refresh Google/Gmail OAuth2 access token using refresh token."""
    try:
        # Use Google's token endpoint to get a new access token
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token"
            }
        )
        
        if response.status_code != 200:
            logger.error(f"Failed to refresh Gmail token: {response.text}")
            return None
            
        token_data = response.json()
        return token_data.get("access_token")
    except Exception as e:
        logger.error(f"Error refreshing Gmail token: {e}")
        return None

def refresh_outlook_token(refresh_token, client_id, client_secret, tenant_id="common"):
    """Refresh Microsoft/Outlook OAuth2 access token using refresh token."""
    try:
        # Use Microsoft's token endpoint to get a new access token
        auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        response = requests.post(
            auth_url,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
                "scope": "https://outlook.office.com/SMTP.Send"
            }
        )
        
        if response.status_code != 200:
            logger.error(f"Failed to refresh Outlook token: {response.text}")
            return None
            
        token_data = response.json()
        return token_data.get("access_token")
    except Exception as e:
        logger.error(f"Error refreshing Outlook token: {e}")
        return None

def create_attachment(attachment_path, target_email=None):
    """Prepare an attachment for the email"""
    # Strip any extra spaces in the attachment path
    attachment_path = attachment_path.strip()
    
    if not os.path.exists(attachment_path):
        # Try to find the file by checking if there's a space issue
        logger.warning(f"Attachment file does not exist at path: {attachment_path}")
        
        # Check if the file exists in the current directory with a different name
        base_dir = os.path.dirname(attachment_path) or '.'
        base_name = os.path.basename(attachment_path)
        
        for file in os.listdir(base_dir):
            if file.replace(' ', '') == base_name.replace(' ', ''):
                logger.info(f"Found matching file: {file}")
                attachment_path = os.path.join(base_dir, file)
                break
        
        if not os.path.exists(attachment_path):
            logger.error(f"Could not find attachment file: {attachment_path}")
            return None
        
    part = MIMEBase('application', "octet-stream")
    with open(attachment_path, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    
    filename = Path(attachment_path).name
    # Handle filenames with spaces correctly for email attachments
    # RFC 2231 and 5987 compliant filename handling
    if ' ' in filename or any(c in filename for c in '(),:;<>@[]'):
        filename_encoded = email.utils.encode_rfc2231(filename, 'utf-8', 'en')
        part.add_header('Content-Disposition', f'attachment; filename*={filename_encoded}')
    else:
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
    
    # For tracking purposes, you could customize the attachment name based on the target
    if target_email:
        # Add a tracking ID that associates with the target
        tracking_id = base64.b64encode(target_email.encode()).decode()[:8]
        part.add_header('X-Tracking-ID', tracking_id)
    
    return part

def send_mail(
    show_name, 
    send_from, 
    send_to, 
    subject, 
    message, 
    server, 
    port,
    username, 
    password=None,
    attachment_path=None,
    use_ssl=False,
    use_tls=True,
    content_type="plain",
    reply_to=None,
    custom_headers=None,
    impersonate=None,
    use_oauth2=False,
    access_token=None,
    refresh_token=None,
    client_id=None,
    client_secret=None,
    token_type=None,  # 'gmail' or 'outlook'
    account=None  # Pass the entire account object for updating tokens
):
    """Send an email with the specified parameters"""
    if isinstance(send_to, str):
        send_to = [send_to]
    
    msg = MIMEMultipart()
    msg['From'] = f'{show_name} <{send_from}>'
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg['Message-ID'] = make_msgid(domain=send_from.split('@')[1])
    
    if reply_to:
        msg['Reply-To'] = reply_to
    
    # Add custom headers if provided
    if custom_headers:
        for key, value in custom_headers.items():
            msg[key] = value
    
    # Add headers for impersonation if specified
    if impersonate and impersonate in MAIL_SERVER_SIGNATURES:
        headers = MAIL_SERVER_SIGNATURES[impersonate]
        for key, value in headers.items():
            # Replace placeholders with random values
            if "{random_hash}" in value:
                value = value.replace("{random_hash}", random_hash())
            if "{random_string}" in value:
                value = value.replace("{random_string}", random_string(12))
            if "{random_uuid}" in value:
                value = value.replace("{random_uuid}", random_uuid())
            msg[key] = value
    
    # Attach message body
    msg.attach(MIMEText(message, content_type))
    
    # Attach file if specified
    if attachment_path:
        attachment = create_attachment(attachment_path, send_to[0])
        if attachment:
            msg.attach(attachment)
    
    # Setup SSL context if needed
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        # Choose connection method based on SSL/TLS settings
        if use_ssl:
            smtp = smtplib.SMTP_SSL(server, port, context=context)
        else:
            smtp = smtplib.SMTP(server, port)
            if use_tls:
                smtp.starttls(context=context)
        
        # Use OAuth2 authentication if specified and tokens are provided
        if use_oauth2 and HAS_OAUTH2_SUPPORT and (access_token or refresh_token):
            # For OAuth2, username is usually the email address
            oauth2_string = None
            
            # If refresh token and related details are provided, we can try to refresh if needed
            if not access_token and refresh_token and client_id and client_secret and token_type:
                if token_type.lower() == 'gmail':
                    access_token = refresh_gmail_token(refresh_token, client_id, client_secret)
                    # Update account if provided
                    if account and access_token:
                        account['oauth2']['access_token'] = access_token
                elif token_type.lower() == 'outlook':
                    access_token = refresh_outlook_token(refresh_token, client_id, client_secret)
                    # Update account if provided
                    if account and access_token:
                        account['oauth2']['access_token'] = access_token
            
            if not access_token:
                raise ValueError("No valid access token for OAuth2 authentication")
                
            oauth2_string = generate_oauth2_string(username, access_token)
            
            # Use XOAUTH2 authentication mechanism
            smtp.ehlo()
            smtp.docmd("AUTH", f"XOAUTH2 {oauth2_string}")
        else:
            # Traditional username/password authentication
            smtp.login(username, password)
        
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()
        
        logger.info(f"Email sent successfully to {send_to[0]}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {send_to[0]}: {e}")
        
        # If authentication failed and we have refresh tokens, try to refresh and retry
        if "authentication failed" in str(e).lower() and use_oauth2 and refresh_token and client_id and client_secret and token_type:
            logger.info("Authentication failed. Attempting to refresh token and retry...")
            
            new_access_token = None
            if token_type.lower() == 'gmail':
                new_access_token = refresh_gmail_token(refresh_token, client_id, client_secret)
                # Update account if provided
                if account and new_access_token:
                    account['oauth2']['access_token'] = new_access_token
            elif token_type.lower() == 'outlook':
                new_access_token = refresh_outlook_token(refresh_token, client_id, client_secret)
                # Update account if provided
                if account and new_access_token:
                    account['oauth2']['access_token'] = new_access_token
                
            if new_access_token:
                logger.info("Token refreshed. Retrying send operation...")
                return send_mail(
                    show_name, send_from, send_to, subject, message, server, port,
                    username, password, attachment_path, use_ssl, use_tls, content_type,
                    reply_to, custom_headers, impersonate, use_oauth2, new_access_token,
                    refresh_token, client_id, client_secret, token_type, account
                )
        
        return False

def randomize_subject(subject, randomization_level=1):
    """Add randomization to the email subject to avoid detection"""
    if randomization_level <= 0:
        return subject
    
    # Apply placeholders to the subject first
    randomized = subject
    
    # Handle new format {random,type,length}
    new_placeholder_pattern = re.compile(r'{random,(str|int|hash|uuid),(\d+)}')
    for match in new_placeholder_pattern.finditer(randomized):
        placeholder = match.group(0)  # The entire placeholder
        random_type = match.group(1)  # Type of random data (str, int, hash, uuid)
        length = int(match.group(2))  # Length of random data
        
        # Generate replacement based on type
        if random_type == "str":
            replacement = random_string(length)
        elif random_type == "int":
            replacement = str(random_with_N_digits(length))
        elif random_type == "hash":
            replacement = random_hash(length)
        elif random_type == "uuid":
            # For UUID, length doesn't really apply but we could truncate
            replacement = random_uuid()[:length]
        
        # Replace in the content
        randomized = randomized.replace(placeholder, replacement)
    
    # Replace standard placeholders in the subject
    for placeholder, replacer in PLACEHOLDER_PATTERNS.items():
        if placeholder in randomized:
            if callable(replacer):
                replacement = replacer()
            elif replacer == "target_email":
                # Skip target_email for subject (we don't have it here)
                continue
            else:
                replacement = str(replacer)
                
            randomized = randomized.replace(placeholder, replacement)
    
    # Handle parameterized placeholders in the subject
    parameterized_pattern = re.compile(r'{{([a-zA-Z_]+):([^}]+)}}')
    
    for match in parameterized_pattern.finditer(randomized):
        placeholder = match.group(0)  # The entire placeholder
        function_name = match.group(1)
        parameter = match.group(2)
        
        # Similar placeholder processing as in personalize_message
        replacement = ""
        
        if function_name == "random_string":
            try:
                length = int(parameter)
                replacement = random_string(length)
            except ValueError:
                replacement = random_string(8)
        elif function_name == "random_digits":
            try:
                length = int(parameter)
                replacement = str(random_with_N_digits(length))
            except ValueError:
                replacement = str(random_with_N_digits(6))
        # Add more handlers for other function types as needed
        
        # Replace the placeholder with the generated value
        if replacement:
            randomized = randomized.replace(placeholder, replacement)
    
    # Level 1+: NO visible randomization unless explicitly included with placeholders like {{prefix}} or {{suffix}}
    # Only add invisible randomization that doesn't affect the visible appearance
    
    # Level 2+: Add random characters, spaces or UTF-8 characters that look like spaces
    if randomization_level >= 2:
        # Add zero-width spaces or other invisible characters
        invisible_chars = ['\u200B', '\u200C', '\u200D', '\u2060', '\uFEFF']
        
        # Insert 1-3 invisible characters at random positions
        for _ in range(random.randint(1, 3)):
            pos = random.randint(0, len(randomized))
            char = random.choice(invisible_chars)
            randomized = randomized[:pos] + char + randomized[pos:]
    
    # Level 3: More aggressive but still invisible randomization
    if randomization_level >= 3:
        try:
            from bs4 import BeautifulSoup
            
            # Use BeautifulSoup to safely parse and modify HTML
            soup = BeautifulSoup(randomized, 'html.parser')
            
            # Add hidden spans with random content to text nodes
            for element in soup.find_all(text=True):
                if len(element.strip()) > 20 and element.parent.name not in ['script', 'style']:
                    # Insert a hidden span with random content before some text nodes
                    if random.random() < 0.2:  # 20% chance
                        new_span = soup.new_tag('span')
                        new_span['style'] = 'display:none'
                        new_span.string = random_string(random.randint(5, 15))
                        element.insert_before(new_span)
            
            # Convert back to string
            randomized = str(soup)
        except ImportError:
            # Fallback if BeautifulSoup isn't available
            # This is less invasive and avoids breaking HTML
            # Only insert in very limited safe places
            pattern = re.compile(r'(<br>|<br/>|<hr>|<hr/>)')
            matches = list(pattern.finditer(randomized))
            
            # Insert hidden spans near some breaks
            if matches and len(matches) > 0:
                for _ in range(min(len(matches), 2)):
                    idx = random.randint(0, len(matches)-1)
                    match = matches[idx]
                    hidden_span = f'<span style="display:none">{random_string(8)}</span>'
                    end = match.end()
                    randomized = randomized[:end] + hidden_span + randomized[end:]
    
    return randomized

def randomize_html_content(html, randomization_level=1, target_email=""):
    """Add randomization to HTML content to avoid detection using placeholders"""
    if randomization_level <= 0:
        return html
    
    # Parse the content to identify safe insertion points
    result = html
    
    # Level 1+: Process existing placeholders
    # Look for placeholder comments like <!-- {{random_comment}} -->
    comment_placeholder = re.compile(r'<!--\s*{{random_comment}}\s*-->')
    comment_matches = list(comment_placeholder.finditer(result))
    
    if comment_matches:
        # Replace each placeholder with a random comment
        for match in comment_matches:
            comment = f"<!-- {random_string(12)} -->"
            result = result[:match.start()] + comment + result[match.end():]
    
    # Look for attribute placeholders like data-random="{{random_attributes}}"
    attr_placeholder = re.compile(r'{{random_attributes}}|data-random="{{random_string[^"]*}}"')
    attr_matches = list(attr_placeholder.finditer(result))
    
    if attr_matches:
        # Replace each placeholder with random attributes
        for match in attr_matches:
            placeholder = match.group(0)
            if placeholder == "{{random_attributes}}":
                replacement = f'data-id="{random_hash(8)}" data-t="{int(time.time())}"'
            else:
                # Extract parameters if any
                param_match = re.search(r'{{random_string(:(\d+))?}}', placeholder)
                if param_match and param_match.group(2):
                    length = int(param_match.group(2))
                    replacement = f'data-random="{random_string(length)}"'
                else:
                    replacement = f'data-random="{random_string(8)}"'
            
            result = result[:match.start()] + replacement + result[match.end():]
    
    # Look for invisible content placeholders
    invisible_placeholder = re.compile(r'{{invisible_content}}')
    invisible_matches = list(invisible_placeholder.finditer(result))
    
    if invisible_matches:
        # Replace each placeholder with random invisible content
        for match in invisible_matches:
            invisible_element = f'<span style="display:none">{random_string(random.randint(5, 20))}</span>'
            result = result[:match.start()] + invisible_element + result[match.end():]
    
    # Look for class placeholders
    class_placeholder = re.compile(r'class="([^"]*)\s*{{random_class}}\s*([^"]*)"')
    class_matches = list(class_placeholder.finditer(result))
    
    if class_matches:
        # Replace each placeholder with a random class
        for match in class_matches:
            prefix = match.group(1)
            suffix = match.group(2)
            random_class = f"c-{random_string(4)}"
            
            # Build the new class attribute
            if prefix and suffix:
                replacement = f'class="{prefix} {random_class} {suffix}"'
            elif prefix:
                replacement = f'class="{prefix} {random_class}"'
            elif suffix:
                replacement = f'class="{random_class} {suffix}"'
            else:
                replacement = f'class="{random_class}"'
            
            # Replace the placeholder
            result = result[:match.start()] + replacement + result[match.end():]
    
    # Handle new pattern format {random,type,length}
    new_placeholder_pattern = re.compile(r'{random,(str|int|hash|uuid),(\d+)}')
    for match in new_placeholder_pattern.finditer(result):
        placeholder = match.group(0)  # The entire placeholder
        random_type = match.group(1)  # Type of random data (str, int, hash, uuid)
        length = int(match.group(2))  # Length of random data
        
        # Generate replacement based on type
        if random_type == "str":
            replacement = random_string(length)
        elif random_type == "int":
            replacement = str(random_with_N_digits(length))
        elif random_type == "hash":
            replacement = random_hash(length)
        elif random_type == "uuid":
            # For UUID, length doesn't really apply but we could truncate
            replacement = random_uuid()[:length]
        
        # Replace in the content
        result = result.replace(placeholder, replacement)
    
    # Level 2+: Only add automatic invisible randomization
    if randomization_level >= 2:
        try:
            from bs4 import BeautifulSoup
            
            # Use BeautifulSoup to safely parse and modify HTML
            soup = BeautifulSoup(result, 'html.parser')
            
            # Add random data attributes to some non-critical tags
            safe_tags = ['div', 'span', 'p', 'li', 'td', 'a', 'section', 'article']
            elements = soup.find_all(safe_tags)
            
            # Randomly select a few elements to modify
            if elements:
                num_to_modify = min(len(elements), random.randint(2, 5))
                for _ in range(num_to_modify):
                    element = random.choice(elements)
                    element['data-r'] = random_string(8)
                
                # Convert back to string
                result = str(soup)
        except ImportError:
            # If BeautifulSoup isn't available, use a simple/safer approach
            # Find HTML tags - without changing visible content
            pattern = re.compile(r'<(div|span|p|a)([^>]*)>', re.IGNORECASE)
            matches = list(pattern.finditer(result))
            
            # Add invisible data attributes to some tags (no more than 3)
            if matches and len(matches) > 0:
                for _ in range(min(len(matches), 3)):
                    idx = random.randint(0, len(matches)-1)
                    match = matches[idx]
                    tag = match.group(1)
                    attrs = match.group(2)
                    
                    # Skip certain patterns
                    if 'data-r' in attrs:
                        continue
                    
                    # Add an invisible data attribute (doesn't affect appearance)
                    new_attr = f'{attrs} data-r="{random_string(8)}"'
                    new_tag = f'<{tag}{new_attr}>'
                    
                    # Replace the tag
                    start, end = match.span()
                    result = result[:start] + new_tag + result[end:]
    
    # Level 3: More aggressive but still invisible randomization
    if randomization_level >= 3:
        try:
            from bs4 import BeautifulSoup
            
            # Use BeautifulSoup to safely parse and modify HTML
            soup = BeautifulSoup(result, 'html.parser')
            
            # Add hidden spans with random content to text nodes
            for element in soup.find_all(text=True):
                if len(element.strip()) > 20 and element.parent.name not in ['script', 'style']:
                    # Insert a hidden span with random content before some text nodes
                    if random.random() < 0.2:  # 20% chance
                        new_span = soup.new_tag('span')
                        new_span['style'] = 'display:none'
                        new_span.string = random_string(random.randint(5, 15))
                        element.insert_before(new_span)
            
            # Convert back to string
            result = str(soup)
        except ImportError:
            # Fallback if BeautifulSoup isn't available
            # This is less invasive and avoids breaking HTML
            # Only insert in very limited safe places
            pattern = re.compile(r'(<br>|<br/>|<hr>|<hr/>)')
            matches = list(pattern.finditer(result))
            
            # Insert hidden spans near some breaks
            if matches and len(matches) > 0:
                for _ in range(min(len(matches), 2)):
                    idx = random.randint(0, len(matches)-1)
                    match = matches[idx]
                    hidden_span = f'<span style="display:none">{random_string(8)}</span>'
                    end = match.end()
                    result = result[:end] + hidden_span + result[end:]
    
    return result

def randomize_text_content(text, randomization_level=1):
    """Add randomization to plain text content to avoid detection using placeholders"""
    if randomization_level <= 0:
        return text
    
    # Look for placeholder markers like {{random_line}} or {{random_space}}
    result = text
    
    # Replace random line placeholders
    if "{{random_line}}" in result:
        lines = result.split('\n')
        new_lines = []
        for line in lines:
            new_lines.append(line.replace("{{random_line}}", random_string(random.randint(10, 30))))
        result = '\n'.join(new_lines)
    
    # Replace random space placeholders
    if "{{random_space}}" in result:
        result = result.replace("{{random_space}}", ' ' * random.randint(1, 5))
    
    # Replace random marker placeholders
    random_marker_pattern = re.compile(r'{{random_marker(:(\d+))?}}')
    for match in random_marker_pattern.finditer(result):
        placeholder = match.group(0)
        length = 8
        if match.group(2):
            length = int(match.group(2))
        marker = f"[ID:{random_hash(length)}]"
        result = result.replace(placeholder, marker)
    
    # Handle new format {random,type,length}
    new_placeholder_pattern = re.compile(r'{random,(str|int|hash|uuid),(\d+)}')
    for match in new_placeholder_pattern.finditer(result):
        placeholder = match.group(0)  # The entire placeholder
        random_type = match.group(1)  # Type of random data (str, int, hash, uuid)
        length = int(match.group(2))  # Length of random data
        
        # Generate replacement based on type
        if random_type == "str":
            replacement = random_string(length)
        elif random_type == "int":
            replacement = str(random_with_N_digits(length))
        elif random_type == "hash":
            replacement = random_hash(length)
        elif random_type == "uuid":
            # For UUID, length doesn't really apply but we could truncate
            replacement = random_uuid()[:length]
        
        # Replace in the content
        result = result.replace(placeholder, replacement)
    
    # Level 2+: Add invisible randomization only
    if randomization_level >= 2:
        # Add zero-width spaces at random positions
        invisible_chars = ['\u200B', '\u200C', '\u200D', '\u2060', '\uFEFF']
        
        lines = result.split('\n')
        for i in range(len(lines)):
            line = lines[i]
            if not line or line.isspace():
                continue
            
            # Insert 1-2 invisible characters at random positions
            for _ in range(random.randint(1, 2)):
                pos = random.randint(0, len(line))
                char = random.choice(invisible_chars)
                line = line[:pos] + char + line[pos:]
                
            lines[i] = line
            
        result = '\n'.join(lines)
    
    # Level 3: More aggressive invisible randomization
    if randomization_level >= 3:
        # Add random empty lines with invisible characters
        lines = result.split('\n')
        new_lines = []
        
        for line in lines:
            new_lines.append(line)
            
            # Occasionally add an empty line with invisible character
            if random.random() > 0.9:
                empty_line = random.choice(invisible_chars)
                new_lines.append(empty_line)
        
        result = '\n'.join(new_lines)
    
    return result

def personalize_message(
    message, 
    target_email, 
    randomize_content=0,
    content_type="plain"
):
    """Personalize the message for the recipient"""
    personalized = message
    
    # Process simple direct placeholders first
    simple_placeholders = {
        "{target_email}": target_email,
        "{random_order_id}": random_order_id(),
        "{random_tracking_id}": random_tracking_id(),
        "{random_invoice_number}": random_invoice_number(),
        "{random_timestamp}": random_timestamp(),
        "{random_ip_address}": random_ip_address(),
        "{random_user_agent}": random_user_agent(),
        "{random_credit_card}": random_credit_card_masked(),
        "{random_phone}": random_phone_number(),
        "{random_name}": random_name(),
        "{random_company}": random_company_name(),
        "{random_uuid}": random_uuid(),
        "{random_string}": random_string(8),
        "{current_date}": datetime.datetime.now().strftime("%Y-%m-%d"),
        "{current_time}": datetime.datetime.now().strftime("%H:%M:%S")
    }
    
    # Replace simple placeholders first
    for placeholder, value in simple_placeholders.items():
        if placeholder in personalized:
            personalized = personalized.replace(placeholder, str(value))
    
    # Handle new format {random,type,length}
    new_placeholder_pattern = re.compile(r'{random,(str|int|hash|uuid),(\d+)}')
    for match in new_placeholder_pattern.finditer(personalized):
        placeholder = match.group(0)  # The entire placeholder
        random_type = match.group(1)  # Type of random data (str, int, hash, uuid)
        length = int(match.group(2))  # Length of random data
        
        # Generate replacement based on type
        if random_type == "str":
            replacement = random_string(length)
        elif random_type == "int":
            replacement = str(random_with_N_digits(length))
        elif random_type == "hash":
            replacement = random_hash(length)
        elif random_type == "uuid":
            # For UUID, length doesn't really apply but we could truncate
            replacement = random_uuid()[:length]
        
        # Replace in the content
        personalized = personalized.replace(placeholder, replacement)
    
    # Replace standard placeholders
    for placeholder, replacer in PLACEHOLDER_PATTERNS.items():
        if placeholder in personalized:
            if callable(replacer):
                replacement = replacer()
            elif replacer == "target_email":
                replacement = target_email
            else:
                replacement = str(replacer)
                
            personalized = personalized.replace(placeholder, replacement)
    
    # Handle parameterized placeholders
    # Format: {{function_name:parameter}}
    parameterized_pattern = re.compile(r'{{([a-zA-Z_]+):([^}]+)}}')
    
    for match in parameterized_pattern.finditer(personalized):
        placeholder = match.group(0)  # The entire placeholder
        function_name = match.group(1)
        parameter = match.group(2)
        
        # Get replacement based on function name and parameter
        replacement = ""
        
        if function_name == "random_string":
            try:
                length = int(parameter)
                replacement = random_string(length)
            except ValueError:
                replacement = random_string(8)  # Default length
                
        elif function_name == "random_digits":
            try:
                length = int(parameter)
                replacement = str(random_with_N_digits(length))
            except ValueError:
                replacement = str(random_with_N_digits(6))  # Default length
                
        elif function_name == "timestamp":
            try:
                replacement = datetime.datetime.now().strftime(parameter)
            except ValueError:
                replacement = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
        elif function_name == "order_id":
            replacement = random_order_id(parameter)
            
        elif function_name == "tracking_id":
            replacement = random_tracking_id(parameter)
            
        elif function_name == "invoice_number":
            replacement = random_invoice_number(parameter)
            
        elif function_name == "phone":
            replacement = random_phone_number(parameter)
            
        elif function_name == "random_hash":
            try:
                length = int(parameter)
                replacement = random_hash(length)
            except ValueError:
                replacement = random_hash(16)  # Default length
        
        # Replace the placeholder with the generated value
        if replacement:
            personalized = personalized.replace(placeholder, replacement)
    
    # Apply content randomization if requested
    if randomize_content > 0:
        if content_type.lower() == "html":
            personalized = randomize_html_content(personalized, randomize_content, target_email)
        else:
            personalized = randomize_text_content(personalized, randomize_content)
    
    return personalized

def connect_to_imap(server, port, username, password, use_ssl=True):
    """Connect to an IMAP server"""
    try:
        if use_ssl:
            # Connect using SSL
            mail = imaplib.IMAP4_SSL(server, port)
        else:
            # Connect without SSL
            mail = imaplib.IMAP4(server, port)
        
        # Login to the server
        mail.login(username, password)
        return mail, None
    except Exception as e:
        return None, str(e)

def connect_to_pop3(server, port, username, password, use_ssl=True):
    """Connect to a POP3 server"""
    try:
        if use_ssl:
            # Connect using SSL
            mail = poplib.POP3_SSL(server, port)
        else:
            # Connect without SSL
            mail = poplib.POP3(server, port)
        
        # Login to the server
        mail.user(username)
        mail.pass_(password)
        return mail, None
    except Exception as e:
        return None, str(e)

def get_imap_folders(imap_conn):
    """Get list of folders from IMAP server"""
    try:
        # List all folders
        response, folders = imap_conn.list()
        
        if response != 'OK':
            return [], f"Failed to get folders: {response}"
        
        # Parse folder names
        folder_list = []
        for folder in folders:
            if not folder:
                continue
                
            parts = folder.decode().split(' "." ')
            if len(parts) > 1:
                # Extract folder name and remove quotes
                folder_name = parts[1].strip().strip('"')
                folder_list.append(folder_name)
        
        return folder_list, None
    except Exception as e:
        return [], str(e)

def get_emails_imap(imap_conn, folder='INBOX', limit=50, search_criteria='ALL'):
    """Get emails from an IMAP server"""
    try:
        # Select the folder
        response, data = imap_conn.select(folder)
        
        if response != 'OK':
            return [], f"Failed to select folder {folder}: {response}"
        
        # Search for all emails
        response, msg_nums = imap_conn.search(None, 'ALL')
        
        if response != 'OK':
            return [], f"Failed to search emails: {response}"
        
        # Get message numbers
        msg_nums = msg_nums[0].split()
        
        # Process from newest to oldest
        msg_nums.reverse()
        
        # Limit the number of emails
        if limit and len(msg_nums) > limit:
            msg_nums = msg_nums[:limit]
        
        emails = []
        
        # Fetch and process emails
        for num in msg_nums:
            # Fetch the email
            response, msg_data = imap_conn.fetch(num, '(RFC822)')
            
            if response != 'OK':
                continue
                
            # Parse the email
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extract email details
            subject = decode_email_header(msg['Subject'])
            from_addr = decode_email_header(msg['From'])
            date = msg['Date']
            
            # Get the body
            body = get_email_body(msg)
            
            # Get attachments
            attachments = get_email_attachments(msg)
            
            # Store email data
            email_data = {
                'subject': subject,
                'from': from_addr,
                'date': date,
                'body': body,
                'has_attachments': len(attachments) > 0,
                'attachments': attachments,
                'raw_message': msg
            }
            
            emails.append(email_data)
        
        return emails, None
    except Exception as e:
        return [], str(e)

def get_emails_pop3(pop3_conn, limit=50):
    """Get emails from a POP3 server"""
    try:
        # Get message count and size
        msg_count, total_size = pop3_conn.stat()
        
        # No emails
        if msg_count == 0:
            return [], None
        
        # Limit the number of emails
        msg_count = min(msg_count, limit)
        
        emails = []
        
        # Fetch and process emails (from newest to oldest)
        for i in range(msg_count, 0, -1):
            # Skip if we've reached the limit
            if len(emails) >= limit:
                break
                
            # Fetch the email
            response, lines, octets = pop3_conn.retr(i)
            
            # Join the lines and parse the email
            raw_email = b'\r\n'.join(lines)
            msg = email.message_from_bytes(raw_email)
            
            # Extract email details
            subject = decode_email_header(msg['Subject'])
            from_addr = decode_email_header(msg['From'])
            date = msg['Date']
            
            # Get the body
            body = get_email_body(msg)
            
            # Get attachments
            attachments = get_email_attachments(msg)
            
            # Store email data
            email_data = {
                'subject': subject,
                'from': from_addr,
                'date': date,
                'body': body,
                'has_attachments': len(attachments) > 0,
                'attachments': attachments,
                'raw_message': msg
            }
            
            emails.append(email_data)
        
        return emails, None
    except Exception as e:
        return [], str(e)

def decode_email_header(header):
    """Decode email header"""
    if not header:
        return ""
        
    decoded_parts = []
    for part, encoding in decode_header(header):
        if isinstance(part, bytes):
            # Try to decode with the specified encoding
            if encoding:
                try:
                    decoded_parts.append(part.decode(encoding))
                except:
                    # If that fails, try utf-8 or ignore errors
                    try:
                        decoded_parts.append(part.decode('utf-8'))
                    except:
                        decoded_parts.append(part.decode('utf-8', errors='ignore'))
            else:
                # Try to decode with utf-8
                try:
                    decoded_parts.append(part.decode('utf-8'))
                except:
                    decoded_parts.append(part.decode('utf-8', errors='ignore'))
        else:
            # If it's already a string, add it as is
            decoded_parts.append(part)
    
    return ''.join(decoded_parts)

def get_email_body(msg):
    """Extract the body from an email message"""
    # Check for multipart messages
    if msg.is_multipart():
        # Get the plaintext or HTML part
        html_part = None
        text_part = None
        
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            # Skip attachments
            if "attachment" in content_disposition:
                continue
                
            # Look for text parts
            if content_type == "text/html":
                html_part = part
            elif content_type == "text/plain":
                text_part = part
        
        # Prefer HTML over plain text
        if html_part:
            charset = html_part.get_content_charset() or 'utf-8'
            try:
                return html_part.get_payload(decode=True).decode(charset)
            except:
                return html_part.get_payload(decode=True).decode(charset, errors='ignore')
        elif text_part:
            charset = text_part.get_content_charset() or 'utf-8'
            try:
                return text_part.get_payload(decode=True).decode(charset)
            except:
                return text_part.get_payload(decode=True).decode(charset, errors='ignore')
        else:
            return ""
    else:
        # Single part message
        charset = msg.get_content_charset() or 'utf-8'
        try:
            return msg.get_payload(decode=True).decode(charset)
        except:
            return msg.get_payload(decode=True).decode(charset, errors='ignore')

def get_email_attachments(msg):
    """Extract attachments from an email message"""
    attachments = []
    
    for i, part in enumerate(msg.walk()):
        # Check if it's an attachment
        if part.get_content_maintype() == 'multipart':
            continue
            
        filename = part.get_filename()
        if not filename:
            # Not an attachment or no filename
            continue
        
        # Decode the filename if needed
        filename = decode_email_header(filename)
        
        # Get content type and size
        content_type = part.get_content_type() or "application/octet-stream"
        
        # Get size
        payload = part.get_payload(decode=True)
        size = len(payload) if payload else 0
        
        attachments.append({
            'filename': filename,
            'content_type': content_type,
            'size': size,
            'part_index': i  # Store part index for later retrieval
        })
    
    return attachments

def save_attachment(msg, attachment_index, save_dir):
    """Save an attachment from an email message"""
    try:
        # Find the attachment part
        parts = list(msg.walk())
        
        # Extract the attachment
        for i, part in enumerate(parts):
            if i == attachment_index:
                filename = part.get_filename()
                
                if not filename:
                    return None, "Invalid attachment or missing filename"
                
                # Decode the filename if needed
                filename = decode_email_header(filename)
                
                # Create the full path
                save_path = os.path.join(save_dir, filename)
                
                # Save the attachment
                with open(save_path, 'wb') as f:
                    payload = part.get_payload(decode=True)
                    if payload:
                        f.write(payload)
                    else:
                        return None, "Empty attachment content"
                
                return save_path, None
        
        return None, "Attachment not found"
    except Exception as e:
        return None, str(e)

def main():
    parser = argparse.ArgumentParser(
        description="RedMailer - Advanced Email Sending Tool for Red Teams",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Input files
    parser.add_argument('-a', '--accounts', help='JSON file containing email accounts', required=True)
    parser.add_argument('-t', '--targets', help='File containing list of target emails', required=True)
    parser.add_argument('-T', '--template', help='Email template file', required=True)
    
    # Email content options
    parser.add_argument('-s', '--subject', help='Email subject', required=True)
    parser.add_argument('-c', '--content-type', choices=['plain', 'html'], default='plain', help='Email content type')
    parser.add_argument('-A', '--attachment', help='File to attach to the email')
    
    # Content randomization options
    parser.add_argument('--randomize-subject', type=int, choices=[0, 1, 2, 3], default=0, 
                        help='Level of subject randomization (0=none, 1=basic, 2=medium, 3=high)')
    parser.add_argument('--randomize-content', type=int, choices=[0, 1, 2, 3], default=0,
                        help='Level of content randomization (0=none, 1=basic, 2=medium, 3=high)')
    
    # Sending options
    parser.add_argument('-d', '--delay', type=float, default=0, help='Delay between emails in seconds')
    parser.add_argument('-j', '--jitter', type=float, default=0, help='Random jitter to add to delay (in seconds)')
    parser.add_argument('--ssl', action='store_true', help='Use SSL instead of TLS')
    parser.add_argument('--no-tls', action='store_true', help='Disable TLS (use unencrypted connection)')
    parser.add_argument('-r', '--rotate', type=int, default=10, help='Number of emails to send before rotating accounts')
    
    # Impersonation options
    parser.add_argument('--impersonate', choices=['outlook', 'gmail', 'yahoo', 'office365', 'protonmail', 'zoho'],
                        help='Impersonate a specific mail server by adding appropriate headers')
    
    # OAuth2 authentication options
    oauth2_group = parser.add_argument_group('OAuth2 Authentication Options')
    oauth2_group.add_argument('--token-file', help='Optional JSON file containing OAuth2 tokens to update accounts.json')
    
    # Proxy options
    parser.add_argument('--proxy', help='Proxy server in format: type:host:port[:username:password]')
    
    # Additional options
    parser.add_argument('--test', type=int, default=0, help='Send only N test emails and exit')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--version', action='version', version=f'RedMailer v{VERSION}')
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Handle attachment path if provided (fix any spaces or path issues)
    if args.attachment:
        args.attachment = args.attachment.strip()
        if not os.path.exists(args.attachment):
            # Try to find the file with exact name in the current directory
            potential_file = os.path.join(os.getcwd(), os.path.basename(args.attachment))
            if os.path.exists(potential_file):
                args.attachment = potential_file
                logger.info(f"Using attachment from current directory: {args.attachment}")
            else:
                # Try to find any file in the current directory that matches when spaces are removed
                base_name = os.path.basename(args.attachment)
                base_name_nospaces = base_name.replace(' ', '')
                found = False
                
                for file in os.listdir(os.getcwd()):
                    if file.replace(' ', '') == base_name_nospaces:
                        args.attachment = os.path.join(os.getcwd(), file)
                        logger.info(f"Found matching attachment with similar name: {file}")
                        found = True
                        break
                
                if not found:
                    logger.warning(f"Attachment file not found: {args.attachment}")
                    logger.info("Will attempt to proceed but attachment may fail.")
    
    # Load accounts, targets, and template
    accounts = load_accounts(args.accounts)
    targets = load_targets(args.targets)
    template = load_template(args.template)
    
    # Load and apply OAuth2 tokens from token file if specified
    if args.token_file and os.path.exists(args.token_file):
        try:
            with open(args.token_file, 'r') as f:
                oauth2_tokens = json.load(f)
                logger.info(f"Loaded OAuth2 tokens from {args.token_file}")
                
                # Match tokens to accounts by username/email
                if "accounts" in oauth2_tokens and isinstance(oauth2_tokens["accounts"], list):
                    for token_account in oauth2_tokens["accounts"]:
                        if "username" in token_account:
                            # Find matching account in accounts list
                            for account in accounts:
                                if account.get("username") == token_account["username"]:
                                    # Update OAuth2 configuration for this account
                                    if "oauth2" in token_account:
                                        if "auth_type" not in account or account["auth_type"] != "oauth2":
                                            logger.info(f"Updating account {account['username']} to use OAuth2")
                                            account["auth_type"] = "oauth2"
                                        
                                        if "oauth2" not in account:
                                            account["oauth2"] = {}
                                            
                                        # Update OAuth2 fields
                                        for key, value in token_account["oauth2"].items():
                                            account["oauth2"][key] = value
                                            
                                        logger.info(f"Updated OAuth2 tokens for account: {account['username']}")
                                    break
                else:
                    logger.warning("Token file doesn't contain account-specific tokens. No accounts updated.")
                    
        except Exception as e:
            logger.error(f"Failed to load or apply OAuth2 tokens from file: {e}")
    
    # Set up proxy if specified
    if args.proxy:
        proxy_parts = args.proxy.split(':')
        if len(proxy_parts) >= 3:
            proxy_type = proxy_parts[0]
            proxy_host = proxy_parts[1]
            proxy_port = int(proxy_parts[2])
            proxy_username = proxy_parts[3] if len(proxy_parts) > 3 else None
            proxy_password = proxy_parts[4] if len(proxy_parts) > 4 else None
            
            setup_proxy(proxy_type, proxy_host, proxy_port, proxy_username, proxy_password)
    
    # Determine SSL/TLS settings
    use_ssl = args.ssl
    use_tls = not args.no_tls
    
    # Limit number of targets for testing if specified
    if args.test > 0:
        targets = targets[:args.test]
        logger.info(f"Test mode: will send to only {len(targets)} targets")

    # Initialize counters
    sent_count = 0
    failed_count = 0
    account_index = 0
    email_counter = 0

    # Count how many OAuth2 accounts are available
    oauth2_account_count = sum(1 for account in accounts if account.get("auth_type") == "oauth2")
    
    # Print banner
    print(f"""
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃           RedMailer v{VERSION}             ┃
    ┃      Advanced Email Sending Tool       ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    
    Loaded:
     - {len(accounts)} email accounts ({oauth2_account_count} using OAuth2)
     - {len(targets)} target email addresses
     - Content type: {args.content_type}
     - Using {'SSL' if use_ssl else ('TLS' if use_tls else 'unencrypted')} connection
    """)

    # Main sending loop
    try:
        for target in targets:
            # Skip empty or commented lines
            if not target or target.startswith('#'):
                continue
                
            # Get the current account
            account = accounts[account_index]
            
            # Personalize the message for this recipient
            personalized_message = personalize_message(
                template, 
                target,
                randomize_content=args.randomize_content,
                content_type=args.content_type
            )
            
            # Randomize subject if requested
            mail_subject = args.subject
            if args.randomize_subject > 0:
                mail_subject = randomize_subject(args.subject, args.randomize_subject)
                logger.debug(f"Randomized subject: {mail_subject}")
            
            # Determine if we're using OAuth2 based on account config
            use_oauth2 = account.get("auth_type") == "oauth2"
            
            # Prepare OAuth2 parameters if needed
            oauth2_params = {}
            if use_oauth2:
                oauth2_config = account.get("oauth2", {})
                oauth2_params = {
                    "use_oauth2": True,
                    "access_token": oauth2_config.get("access_token"),
                    "refresh_token": oauth2_config.get("refresh_token"),
                    "client_id": oauth2_config.get("client_id"),
                    "client_secret": oauth2_config.get("client_secret"),
                    "token_type": oauth2_config.get("type")
                }
            else:
                oauth2_params = {
                    "use_oauth2": False,
                    "access_token": None,
                    "refresh_token": None,
                    "client_id": None,
                    "client_secret": None,
                    "token_type": None
                }
            
            # Send the email
            success = send_mail(
                show_name=account.get('display_name', account['username'].split('@')[0]),
                send_from=account.get('from_email', account['username']),
                send_to=target,
                subject=mail_subject,
                message=personalized_message,
                server=account['server'],
                port=account['port'],
                username=account['username'],
                password=account.get('password'),
                attachment_path=args.attachment,
                use_ssl=use_ssl,
                use_tls=use_tls,
                content_type=args.content_type,
                reply_to=account.get('reply_to'),
                custom_headers=account.get('headers'),
                impersonate=args.impersonate,
                **oauth2_params,
                account=account
            )
            
            # Update counters
            if success:
                sent_count += 1
            else:
                failed_count += 1
            
            # Rotate account if needed
            email_counter += 1
            if email_counter >= args.rotate:
                account_index = (account_index + 1) % len(accounts)
                email_counter = 0
                logger.info(f"Rotating to next account: {accounts[account_index]['username']}")
            
            # Delay before next email if specified
            if args.delay > 0 and len(targets) > 1:
                delay_time = args.delay
                if args.jitter > 0:
                    delay_time += random.uniform(0, args.jitter)
                logger.debug(f"Sleeping for {delay_time:.2f} seconds")
                time.sleep(delay_time)
    
    except KeyboardInterrupt:
        logger.warning("Operation interrupted by user")
    
    # Print summary
    print(f"""
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                Summary                 ┃
    ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
    ┃ Total emails processed: {sent_count + failed_count:14d} ┃
    ┃ Successfully sent:      {sent_count:14d} ┃
    ┃ Failed:                 {failed_count:14d} ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """)

if __name__ == "__main__":
    main()
