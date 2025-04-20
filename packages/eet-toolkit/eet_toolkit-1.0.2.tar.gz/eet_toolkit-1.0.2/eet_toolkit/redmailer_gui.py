#!/usr/bin/env python3
import sys
import os
import json
import logging
import platform
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
    QFileDialog, QMessageBox, QComboBox, QSpinBox, QCheckBox,
    QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem, QProgressBar,
    QStatusBar, QSplashScreen, QDialog, QInputDialog, QStyleFactory
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QTimer, QDateTime, QRect
from PyQt6.QtGui import QIcon, QFont, QAction, QPixmap, QColor, QPalette, QGuiApplication, QPainter, QKeySequence, QShortcut
import datetime
import base64
import time
import html

# Import the RedMailer functionality
import eet_toolkit.redmail as redmail
# Application information
APP_NAME = "EET Email Enumeration Toolkit"
APP_VERSION = "1.0.0"
APP_COMPANY = "Script1337"
APP_COPYRIGHT = f"© {datetime.datetime.now().year} {APP_COMPANY}"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('redmailer_gui.log')
    ]
)
logger = logging.getLogger('redmailer_gui')

# Embedded application icon (base64 encoded)
APP_ICON = """
iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAABmJLR0QA/wD/AP+gvaeTAAAHLElEQVR4nO2dW2wUVRjHf9PdpVzKHVoIpRAsLRHkpgRNTEQgpvCkhAQkwaAJQTAxmBg18YF4e/KW+GIMMSYGjYlBExHkBeFBg4EAFZAILRVKCTe5tKV0t91dH3a37bLn7MzuzOyZ2f1/yabpnO/M+f9n55w5c+acAYPBYDAYDAaDwWDIM0Ky5JIkjQUeA2YBdwJTgPFAWJacDuRACWgBTgPHgEPAQSAqQW8QeDDAqymXXcDfEvRSMiQTwBJgL5DV8NoLLE4gSzpLPSl0DTKH7vdG1+s2UAd8ClR5LHs8MA8oAhfRN1ByQDMwMwBXmSztzvUv8FHB9UuXCnwK9KB/gPSRwRsC+a7CXzlJngvEWQwxYCf6B4bSxJQr0QOL8dZ0WbAYeB7YDpzsMXtadYQqYIXL6/ZDMeBbIEvnrNuIVJHhEtDqkpMXVqjomghsEBRIWBzYJdEUQLwGP6wCnkHQ+UkHudJlwpfM6PD4fj9kJfPchUqYVbqMcIVCIUKha6LeBGpMHFIgKXKh0H8yQyGoqgrG6QOYQPRghBAVi7JqL6ZqWWgp/faNYYYmU0YYtBT9ZYg0JhA9mKrFoAWzDokmrBNDzCGhIeaQkGDWIXoQdhHMICQa05gbtGDKED0IZ1kGTZhAtGAC0YMJRAMmED2YQDQQ1qnc0ULnfD8UCkGpBLmc874oQwILRHWDqyrcUMifL1EZ/fvK9x2fFWXgwDHy1CG6p8Ky9UU+i5S+ZwEJLJBw2F8gqgPJ5fzJ9OPLj7xoJxF5MIHowQSiBxOIHkwgejCB6EH5hYksVF/C9CpfHRt1jwkWdGMMvI+FgbBxELbPgmRJl2XKNYHoQdg2DKveMnRgAtGDGYdEY+qQaEwgejCBaMEEogdTh0RjAtGCCUQPwvnCIDLzXI6ofjZFdTyic0YgE0O6DFFdyXqdr+t+D8BN9Z2Tp/WOVXRmpAoS93dQ1Ow5e5ab7z/r6Dd+3Bi+eP9NAP7Yd5iVL2z0pePHlyijHJ2BixDpQGJtMfv6v0/yyBOvkUp1vbRXFRrFnj3bAJj3xFpOnjrr+Tx+fMmQN4FolhW5bnf/Y55GIXn3h+2sPriFXV8cZOMHnzE+PJafvtvMHZMnADB16kTe3LiOlS9u9KSl0lfRBdK/XshlnfeVA+ms44d0OptlyTvbTzHn5deYNSvCzl+3MHHi+P5jnliykKZzLaxY/aaQm0pfJRNIsdj7ky3W/pXO/n9DaG5PsPqTfdw39Q6WZdbAvn3XHFu9fClbt//KyVNnXeso9cXlFXshsJbmdhK5DPdmH+WZJ56DhQuhvr5/f11dDaUSTL7zdg4ebXRVuUpfh7C5w8PumOoK+a7x0PTNEQpTRsLYsdDc7Dh28eLfAKTTWZqaWsjlCo4yVPoKbVVeQogrFAsU2kZQnDoWxow5V3fs2MYD3HR9HQ319cy4+y7GxUe5rlSlrzBmDDGc1Rc/yxSP5HLdG0WJRPeyYTQw794ZbPvgbao8lGsqfQHCMqTgpQxRhayyB1JJ9R0zfFRsBC8te1K5ryMvGQS9UFRpq9RXgfCWO1muQH9x06GQOz1d/j2fCMsQE0hnTA8rGjMOiSYUsn9v9DBzCArWDRnVzZ8oQ9rfDTpmWefOt3K+qQWAxnMt/dtF+hDUF2GG5HL+5deuXXft34sX//H3j4vl4yrpYMqQaITtkEGqt9y0y3R+7kdGhLyoj9B3PFGGmLUsoQ6UlrZhgwpVvvJpVS0ShSV/6SccFrcbTCDRmKolGtPLisZ0DIcE5jkkQoQ9EJXzfl0+VeqL3nMhwoFhSNcvqhNW6StsHwYl1xCCsIcl0lfpK8uhCHsYFy9d4ZmXNtHW1s7ChfNZ9/oaxo0dXVZepS84HpicGUUZ0tXVxUMPL2Hp0iVs2bKJ9o4Etm3bJlN29r1/vzfvbHbl3bmvS1+3/OQHdmwmKpHE4oKnN92+ZW3c+DErVz7H4MGD+rd1dHS4ylhZ8qp8rdv6GRf/auGxR+cJFYXTG1kZ4nTVRD9Vz6hRIzl//gLpdBcAqVSK+ob/OHLH9dz3xJusWb+FTz/fw/GG/yiVblBVOYi33lzH6fomXlmz0ZOvS191ooS7v1KJfD5PUxO89toann32eQDWrl1NuFyPiXVt/lG5FhXxJX7dX5ghoVCIU6dO9P+9bNkSNmxY7yio7IqJpkwifc+f/5OVKxq49947efWVRQwaNEjYW1HtK+yY2nYFctm0Zf/nxOJRduz62Tbj8+cvYNuHO393KZM/jn1Ld9Ut3DtjGrZtI+u7p4LyJRxDOj7dV6+u5uDBAyQSkDh/hcOHmhg2opb6hnP2kSNH3XjXlAZXvlS9m5w5c4bdu3eTSqUYNWoUCxYsoLe3NyLiK8pn4Isvjxw50tLc3Jw9derUeaAmHo/nYrFY3q+vOiCbzQ5qaWnJpVKp7gATJ04sFQoFEb3+az5n7Sc84JfBYDAYDAaDwWAw+OZ/Kk8rSXbmYH0AAAAASUVORK5CYII=
"""

# Load application icon from base64
def get_app_icon():
    icon_data = base64.b64decode(APP_ICON)
    pixmap = QPixmap()
    pixmap.loadFromData(icon_data)
    return QIcon(pixmap)

# Create splash screen image
def create_splash_image():
    pixmap = QPixmap(450, 250)
    pixmap.fill(QColor("#1e3a8a"))  # Dark blue background
    
    # Add app name and version
    painter = QPainter(pixmap)
    painter.setPen(QColor("white"))
    
    # App name
    font = QFont("Arial", 26, QFont.Weight.Bold)
    painter.setFont(font)
    rect = QRect(0, 60, 450, 50)
    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, APP_NAME)
    
    # Version
    font = QFont("Arial", 14)
    painter.setFont(font)
    rect = QRect(0, 120, 450, 30)
    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"Version {APP_VERSION}")
    
    # Description
    font = QFont("Arial", 12)
    painter.setFont(font)
    rect = QRect(0, 160, 450, 25)
    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Email Enumeration & Reader Tool")
    
    # Copyright
    font = QFont("Arial", 10)
    painter.setFont(font)
    rect = QRect(0, 200, 450, 20)
    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, APP_COPYRIGHT)
    
    # Contact info
    font = QFont("Arial", 8)
    painter.setFont(font)
    rect = QRect(0, 225, 450, 15)
    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Telegram: @script1337 | GitHub: script1337")
    
    painter.end()
    return pixmap

# Create dark theme palette
def create_dark_theme():
    palette = QPalette()
    
    # Set colors
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    
    return palette

def validate_email(email):
    """Validate an email address format"""
    import re
    # Simple regex for email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

class EmailSenderThread(QThread):
    """Thread for sending emails without blocking the GUI"""
    update_progress = pyqtSignal(int, int)  # (current, total)
    update_status = pyqtSignal(str)
    email_sent = pyqtSignal(str, bool, str)  # (email, success, error_message)
    error_occurred = pyqtSignal(str)  # Error message
    finished_sending = pyqtSignal(int, int)  # (success_count, fail_count)
    
    def __init__(self, accounts, targets, template, subject, content_type, 
                 attachment=None, randomize_subject=0, randomize_content=0, 
                 delay=0, jitter=0, use_ssl=False, no_tls=False, 
                 rotate=10, impersonate=None):
        super().__init__()
        self.accounts = accounts
        self.targets = targets
        self.template = template
        self.subject = subject
        self.content_type = content_type
        self.attachment = attachment
        self.randomize_subject = randomize_subject
        self.randomize_content = randomize_content
        self.delay = delay
        self.jitter = jitter
        self.use_ssl = use_ssl
        self.use_tls = not no_tls
        self.rotate = rotate
        self.impersonate = impersonate
        self.is_running = True
    
    def run(self):
        """Run the email sending process"""
        # Validate accounts
        if not self.accounts:
            self.error_occurred.emit("No email accounts loaded")
            return
            
        # Validate targets
        if not self.targets:
            self.error_occurred.emit("No target email addresses loaded")
            return
        
        # Initialize counters
        sent_count = 0
        failed_count = 0
        account_index = 0
        email_counter = 0
        total = len(self.targets)
        
        self.update_status.emit("Starting email sending process...")
        
        try:
            for i, target in enumerate(self.targets):
                if not self.is_running:
                    self.update_status.emit("Email sending process stopped by user")
                    break
                
                # Skip empty or commented lines
                if not target or target.startswith('#'):
                    continue
                
                # Validate email format
                if not validate_email(target):
                    self.update_status.emit(f"Invalid email format: {target}")
                    self.email_sent.emit(target, False, "Invalid email format")
                    failed_count += 1
                    continue
                
                # Update progress
                self.update_progress.emit(i+1, total)
                self.update_status.emit(f"Sending to {target} ({i+1}/{total})")
                
                try:
                    # Get the current account
                    if not self.accounts:
                        self.error_occurred.emit("No email accounts available")
                        break
                        
                    if account_index >= len(self.accounts):
                        account_index = 0
                        
                    account = self.accounts[account_index]
                    
                    # Personalize the message
                    try:
                        personalized_message = redmail.personalize_message(
                            self.template,
                            target,
                            randomize_content=self.randomize_content,
                            content_type=self.content_type
                        )
                    except Exception as e:
                        self.update_status.emit(f"Error personalizing message: {str(e)}")
                        self.email_sent.emit(target, False, f"Error personalizing message: {str(e)}")
                        failed_count += 1
                        continue
                    
                    # Randomize subject if requested
                    mail_subject = self.subject
                    if self.randomize_subject > 0:
                        try:
                            mail_subject = redmail.randomize_subject(self.subject, self.randomize_subject)
                        except Exception as e:
                            self.update_status.emit(f"Error randomizing subject: {str(e)}")
                            # Continue with original subject
                    
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
                    
                    # Check attachment path
                    attachment_path = None
                    if self.attachment:
                        if os.path.exists(self.attachment):
                            attachment_path = self.attachment
                        else:
                            self.update_status.emit(f"Warning: Attachment file not found: {self.attachment}")
                    
                    # Send the email
                    error_message = ""
                    try:
                        success = redmail.send_mail(
                            show_name=account.get('display_name', account['username'].split('@')[0]),
                            send_from=account.get('from_email', account['username']),
                            send_to=target,
                            subject=mail_subject,
                            message=personalized_message,
                            server=account['server'],
                            port=account['port'],
                            username=account['username'],
                            password=account.get('password'),
                            attachment_path=attachment_path,
                            use_ssl=self.use_ssl,
                            use_tls=self.use_tls,
                            content_type=self.content_type,
                            reply_to=account.get('reply_to'),
                            custom_headers=account.get('headers'),
                            impersonate=self.impersonate,
                            **oauth2_params,
                            account=account
                        )
                    except Exception as e:
                        success = False
                        error_message = str(e)
                        self.update_status.emit(f"Error sending to {target}: {error_message}")
                    
                    # Emit signal for each email result
                    self.email_sent.emit(target, success, error_message)
                    
                    # Update counters
                    if success:
                        sent_count += 1
                    else:
                        failed_count += 1
                    
                    # Rotate account if needed
                    email_counter += 1
                    if email_counter >= self.rotate:
                        account_index = (account_index + 1) % len(self.accounts)
                        email_counter = 0
                        self.update_status.emit(f"Rotating to next account: {self.accounts[account_index]['username']}")
                    
                    # Delay before next email if specified
                    if self.delay > 0 and i < total - 1:
                        delay_time = self.delay
                        if self.jitter > 0:
                            import random
                            delay_time += random.uniform(0, self.jitter)
                        self.update_status.emit(f"Waiting for {delay_time:.2f} seconds before next email")
                        time.sleep(delay_time)
                
                except Exception as e:
                    self.update_status.emit(f"Unexpected error processing {target}: {str(e)}")
                    self.email_sent.emit(target, False, f"Unexpected error: {str(e)}")
                    failed_count += 1
                    logger.error(f"Unexpected error processing {target}: {str(e)}", exc_info=True)
                
        except Exception as e:
            self.error_occurred.emit(f"Error in email sender thread: {str(e)}")
            logger.error(f"Error in email sender thread: {e}", exc_info=True)
        
        # Emit finished signal with final counts
        self.finished_sending.emit(sent_count, failed_count)
    
    def stop(self):
        """Stop the email sending process"""
        self.is_running = False

class AboutDialog(QDialog):
    """About dialog showing application information"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"About {APP_NAME}")
        self.setWindowIcon(get_app_icon())
        self.setFixedSize(400, 350)
        
        layout = QVBoxLayout(self)
        
        # App icon
        icon_label = QLabel()
        icon_label.setPixmap(get_app_icon().pixmap(QSize(64, 64)))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # App name
        name_label = QLabel(APP_NAME)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = name_label.font()
        font.setPointSize(16)
        font.setBold(True)
        name_label.setFont(font)
        layout.addWidget(name_label)
        
        # Version
        version_label = QLabel(f"Version {APP_VERSION}")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        # System info
        sys_info = QLabel(f"Running on {platform.system()} {platform.release()}")
        sys_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sys_info)
        
        # Python version
        py_version = QLabel(f"Python {platform.python_version()}")
        py_version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(py_version)
        
        layout.addSpacing(20)
        
        # Description
        desc_label = QLabel("Email enumeration and mail reading toolkit")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addSpacing(10)
        
        # Contact info
        contact_label = QLabel("Contact Information:")
        contact_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(contact_label)
        
        # Telegram
        telegram_label = QLabel("Telegram: @script1337")
        telegram_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(telegram_label)
        
        # GitHub
        github_label = QLabel("GitHub: https://github.com/script1337")
        github_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(github_label)
        
        layout.addSpacing(20)
        
        # Copyright
        copyright_label = QLabel(APP_COPYRIGHT)
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_label)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

class MainWindow(QMainWindow):
    """Main window for the RedMailer GUI application"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(get_app_icon())
        self.setMinimumSize(900, 700)
        
        # Initialize variables
        self.accounts = []
        self.targets = []
        self.email_thread = None
        self.is_dark_theme = False
        self.emails = []
        self.email_connection = None
        self.connection_type = None  # 'imap' or 'pop3'
        self.email_reader_thread = None
        
        # Set up the UI
        self.setup_ui()
        self.create_menu()
        
        # Create keyboard shortcuts
        self.create_shortcuts()
        
        # Restore saved settings if available
        self.load_settings()
        
        # Auto-save settings timer
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.timeout.connect(self.save_settings)
        self.auto_save_timer.start(60000)  # Save every minute
    
    def create_menu(self):
        """Create application menu"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_accounts = QAction("Open Accounts File", self)
        open_accounts.triggered.connect(self.browse_accounts)
        file_menu.addAction(open_accounts)
        
        open_targets = QAction("Open Targets File", self)
        open_targets.triggered.connect(self.browse_targets)
        file_menu.addAction(open_targets)
        
        open_template = QAction("Open Template File", self)
        open_template.triggered.connect(self.browse_template)
        file_menu.addAction(open_template)
        
        file_menu.addSeparator()
        
        save_settings_action = QAction("Save Settings", self)
        save_settings_action.triggered.connect(self.save_settings)
        file_menu.addAction(save_settings_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        self.toggle_theme_action = QAction("Toggle Dark Theme", self)
        self.toggle_theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(self.toggle_theme_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        clear_log_action = QAction("Clear Log", self)
        clear_log_action.triggered.connect(self.clear_log)
        tools_menu.addAction(clear_log_action)
        
        clear_results_action = QAction("Clear Results", self)
        clear_results_action.triggered.connect(self.clear_results)
        tools_menu.addAction(clear_results_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_shortcuts(self):
        """Create keyboard shortcuts"""
        # Ctrl+O for open accounts
        shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        shortcut.activated.connect(self.browse_accounts)
        
        # Ctrl+T for open targets
        shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        shortcut.activated.connect(self.browse_targets)
        
        # Ctrl+E for open template
        shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        shortcut.activated.connect(self.browse_template)
        
        # Ctrl+S for save settings
        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(self.save_settings)
        
        # F1 for about
        shortcut = QShortcut(QKeySequence("F1"), self)
        shortcut.activated.connect(self.show_about)
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.is_dark_theme = not self.is_dark_theme
        
        if self.is_dark_theme:
            app = QApplication.instance()
            app.setPalette(create_dark_theme())
            self.log("Switched to dark theme")
        else:
            app = QApplication.instance()
            app.setPalette(app.style().standardPalette())
            self.log("Switched to light theme")
    
    def show_about(self):
        """Show the about dialog"""
        about_dialog = AboutDialog(self)
        about_dialog.exec()
    
    def setup_ui(self):
        """Set up the main UI components"""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget for different sections
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Create main tabs
        self.config_tab = QWidget()
        self.email_tab = QWidget()
        self.accounts_tab = QWidget()
        self.logs_tab = QWidget()
        self.reader_tab = QWidget()
        
        tabs.addTab(self.email_tab, "Compose Email")
        tabs.addTab(self.config_tab, "Configuration")
        tabs.addTab(self.accounts_tab, "Accounts")
        tabs.addTab(self.logs_tab, "Logs")
        tabs.addTab(self.reader_tab, "Email Reader")
        
        # Set up the tabs
        self.setup_email_tab()
        self.setup_config_tab()
        self.setup_accounts_tab()
        self.setup_logs_tab()
        self.setup_reader_tab()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Create progress bar in status bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def setup_email_tab(self):
        """Set up the email composition tab"""
        layout = QVBoxLayout(self.email_tab)
        
        # Email subject
        subject_layout = QHBoxLayout()
        subject_label = QLabel("Subject:")
        self.subject_input = QLineEdit()
        subject_layout.addWidget(subject_label)
        subject_layout.addWidget(self.subject_input)
        layout.addLayout(subject_layout)
        
        # Email content
        content_label = QLabel("Email Content:")
        self.content_edit = QTextEdit()
        self.content_edit.setAcceptRichText(False)  # Plain text only
        layout.addWidget(content_label)
        layout.addWidget(self.content_edit)
        
        # Template file
        template_layout = QHBoxLayout()
        template_label = QLabel("Or Load Template File:")
        self.template_path = QLineEdit()
        self.template_path.setReadOnly(True)
        template_button = QPushButton("Browse...")
        template_button.clicked.connect(self.browse_template)
        template_layout.addWidget(template_label)
        template_layout.addWidget(self.template_path)
        template_layout.addWidget(template_button)
        layout.addLayout(template_layout)
        
        # Targets file
        targets_layout = QHBoxLayout()
        targets_label = QLabel("Targets File:")
        self.targets_path = QLineEdit()
        self.targets_path.setReadOnly(True)
        targets_button = QPushButton("Browse...")
        targets_button.clicked.connect(self.browse_targets)
        targets_layout.addWidget(targets_label)
        targets_layout.addWidget(self.targets_path)
        targets_layout.addWidget(targets_button)
        layout.addLayout(targets_layout)
        
        # Attachment file
        attachment_layout = QHBoxLayout()
        attachment_label = QLabel("Attachment (optional):")
        self.attachment_path = QLineEdit()
        self.attachment_path.setReadOnly(True)
        attachment_button = QPushButton("Browse...")
        attachment_button.clicked.connect(self.browse_attachment)
        attachment_layout.addWidget(attachment_label)
        attachment_layout.addWidget(self.attachment_path)
        attachment_layout.addWidget(attachment_button)
        layout.addLayout(attachment_layout)
        
        # Content type
        content_type_layout = QHBoxLayout()
        content_type_label = QLabel("Content Type:")
        self.content_type = QComboBox()
        self.content_type.addItems(["plain", "html"])
        content_type_layout.addWidget(content_type_label)
        content_type_layout.addWidget(self.content_type)
        content_type_layout.addStretch()
        layout.addLayout(content_type_layout)
        
        # Randomization options
        rand_group = QGroupBox("Randomization")
        rand_layout = QFormLayout(rand_group)
        
        self.randomize_subject = QSpinBox()
        self.randomize_subject.setRange(0, 3)
        self.randomize_subject.setToolTip("0=none, 1=basic, 2=medium, 3=high")
        
        self.randomize_content = QSpinBox()
        self.randomize_content.setRange(0, 3)
        self.randomize_content.setToolTip("0=none, 1=basic, 2=medium, 3=high")
        
        rand_layout.addRow("Randomize Subject (0-3):", self.randomize_subject)
        rand_layout.addRow("Randomize Content (0-3):", self.randomize_content)
        
        layout.addWidget(rand_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        self.test_button = QPushButton("Send Test Email")
        self.test_button.clicked.connect(self.send_test_email)
        
        self.send_button = QPushButton("Send All Emails")
        self.send_button.clicked.connect(self.send_emails)
        
        self.stop_button = QPushButton("Stop Sending")
        self.stop_button.clicked.connect(self.stop_sending)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.test_button)
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)
    
    def setup_config_tab(self):
        """Set up the configuration tab"""
        layout = QVBoxLayout(self.config_tab)
        
        # Sending options
        sending_group = QGroupBox("Sending Options")
        sending_layout = QFormLayout(sending_group)
        
        # Delay
        self.delay_input = QSpinBox()
        self.delay_input.setRange(0, 3600)
        self.delay_input.setSuffix(" sec")
        sending_layout.addRow("Delay between emails:", self.delay_input)
        
        # Jitter
        self.jitter_input = QSpinBox()
        self.jitter_input.setRange(0, 60)
        self.jitter_input.setSuffix(" sec")
        sending_layout.addRow("Random jitter:", self.jitter_input)
        
        # Rotate
        self.rotate_input = QSpinBox()
        self.rotate_input.setRange(1, 100)
        self.rotate_input.setValue(10)
        sending_layout.addRow("Rotate accounts after:", self.rotate_input)
        
        # SSL/TLS options
        self.use_ssl = QCheckBox("Use SSL instead of TLS")
        self.no_tls = QCheckBox("Disable TLS (unencrypted)")
        sending_layout.addRow("", self.use_ssl)
        sending_layout.addRow("", self.no_tls)
        
        # Connect SSL/TLS checkboxes to ensure they don't conflict
        self.use_ssl.stateChanged.connect(self.ssl_changed)
        self.no_tls.stateChanged.connect(self.tls_changed)
        
        layout.addWidget(sending_group)
        
        # Impersonation options
        impersonate_group = QGroupBox("Impersonation (Headers)")
        impersonate_layout = QVBoxLayout(impersonate_group)
        
        self.impersonate_combo = QComboBox()
        self.impersonate_combo.addItem("None")
        self.impersonate_combo.addItems(["outlook", "gmail", "yahoo", "office365", "protonmail", "zoho"])
        
        impersonate_layout.addWidget(QLabel("Impersonate Mail Service:"))
        impersonate_layout.addWidget(self.impersonate_combo)
        
        layout.addWidget(impersonate_group)
        
        # Accounts file
        accounts_layout = QHBoxLayout()
        accounts_label = QLabel("Accounts File:")
        self.accounts_path = QLineEdit()
        self.accounts_path.setReadOnly(True)
        accounts_button = QPushButton("Browse...")
        accounts_button.clicked.connect(self.browse_accounts)
        accounts_layout.addWidget(accounts_label)
        accounts_layout.addWidget(self.accounts_path)
        accounts_layout.addWidget(accounts_button)
        layout.addLayout(accounts_layout)
        
        # Create save settings button
        save_button = QPushButton("Save Configuration")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        
        # Add spacer at the bottom
        layout.addStretch()
    
    def setup_accounts_tab(self):
        """Set up the accounts management tab"""
        layout = QVBoxLayout(self.accounts_tab)
        
        # Accounts table
        self.accounts_table = QTableWidget()
        self.accounts_table.setColumnCount(4)
        self.accounts_table.setHorizontalHeaderLabels(["Username", "Server", "Port", "Auth Type"])
        self.accounts_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.accounts_table)
        
        # Refresh button
        refresh_button = QPushButton("Refresh Accounts")
        refresh_button.clicked.connect(self.refresh_accounts)
        layout.addWidget(refresh_button)
        
        # OAuth2 token file
        oauth2_layout = QHBoxLayout()
        oauth2_label = QLabel("Update OAuth2 Tokens File:")
        self.oauth2_path = QLineEdit()
        self.oauth2_path.setReadOnly(True)
        oauth2_button = QPushButton("Browse...")
        oauth2_button.clicked.connect(self.browse_oauth2_tokens)
        apply_tokens_button = QPushButton("Apply Tokens")
        apply_tokens_button.clicked.connect(self.apply_oauth2_tokens)
        
        oauth2_layout.addWidget(oauth2_label)
        oauth2_layout.addWidget(self.oauth2_path)
        oauth2_layout.addWidget(oauth2_button)
        oauth2_layout.addWidget(apply_tokens_button)
        layout.addLayout(oauth2_layout)
    
    def setup_logs_tab(self):
        """Set up the logs tab"""
        layout = QVBoxLayout(self.logs_tab)
        
        # Log viewer
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)
        
        # Results table
        label = QLabel("Email Sending Results:")
        layout.addWidget(label)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Email", "Status"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.results_table)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        clear_log_button = QPushButton("Clear Log")
        clear_log_button.clicked.connect(self.clear_log)
        
        clear_results_button = QPushButton("Clear Results")
        clear_results_button.clicked.connect(self.clear_results)
        
        export_button = QPushButton("Export Results")
        export_button.clicked.connect(self.export_results)
        
        button_layout.addWidget(clear_log_button)
        button_layout.addWidget(clear_results_button)
        button_layout.addWidget(export_button)
        layout.addLayout(button_layout)
    
    def ssl_changed(self, state):
        """Handle SSL checkbox state change"""
        if state == Qt.CheckState.Checked:
            self.no_tls.setChecked(False)
    
    def tls_changed(self, state):
        """Handle TLS checkbox state change"""
        if state == Qt.CheckState.Checked:
            self.use_ssl.setChecked(False)
    
    def browse_template(self):
        """Browse for a template file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Template File", "", "Text Files (*.txt);;HTML Files (*.html);;All Files (*)"
        )
        if file_path:
            self.template_path.setText(file_path)
            try:
                with open(file_path, 'r') as f:
                    self.content_edit.setPlainText(f.read())
                self.log("Template file loaded successfully")
            except Exception as e:
                self.log(f"Error loading template: {str(e)}")
    
    def browse_targets(self):
        """Browse for a targets file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Targets File", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.targets_path.setText(file_path)
            try:
                self.targets = redmail.load_targets(file_path)
                self.log(f"Loaded {len(self.targets)} target email addresses")
            except Exception as e:
                self.log(f"Error loading targets: {str(e)}")
    
    def browse_attachment(self):
        """Browse for an attachment file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Attachment File", "", "All Files (*)"
        )
        if file_path:
            self.attachment_path.setText(file_path)
            self.log(f"Attachment selected: {os.path.basename(file_path)}")
    
    def browse_accounts(self):
        """Browse for an accounts file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Accounts File", "", "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self.accounts_path.setText(file_path)
            try:
                self.accounts = redmail.load_accounts(file_path)
                self.log(f"Loaded {len(self.accounts)} email accounts")
                self.refresh_accounts()
            except Exception as e:
                self.log(f"Error loading accounts: {str(e)}")
    
    def browse_oauth2_tokens(self):
        """Browse for an OAuth2 tokens file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select OAuth2 Tokens File", "", "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self.oauth2_path.setText(file_path)
    
    def apply_oauth2_tokens(self):
        """Apply OAuth2 tokens to accounts"""
        if not self.oauth2_path.text():
            QMessageBox.warning(self, "Missing OAuth2 Tokens File", "Please select an OAuth2 tokens file first.")
            return
            
        if not self.accounts:
            QMessageBox.warning(self, "Missing Accounts", "No email accounts loaded. Please load an accounts file first.")
            return
        
        try:
            # Read OAuth2 tokens file
            with open(self.oauth2_path.text(), 'r') as f:
                oauth2_tokens = json.load(f)
            
            updated = 0
            
            # Check if the file has the expected structure
            if "accounts" not in oauth2_tokens or not isinstance(oauth2_tokens["accounts"], list):
                QMessageBox.warning(self, "Invalid OAuth2 Tokens File", 
                                   "The OAuth2 tokens file does not have the expected structure. It should contain an 'accounts' list.")
                return
                
            # Match tokens to accounts by username/email
            for token_account in oauth2_tokens["accounts"]:
                if "username" not in token_account:
                    continue
                    
                # Find matching account in accounts list
                for account in self.accounts:
                    if account.get("username") == token_account["username"]:
                        # Update OAuth2 configuration for this account
                        if "oauth2" in token_account:
                            # Set auth_type to oauth2
                            account["auth_type"] = "oauth2"
                            
                            # Ensure oauth2 field exists
                            if "oauth2" not in account:
                                account["oauth2"] = {}
                                
                            # Update OAuth2 fields
                            for key, value in token_account["oauth2"].items():
                                account["oauth2"][key] = value
                            
                            self.log(f"Updated OAuth2 tokens for account: {account['username']}")
                            updated += 1
                            break
            
            if updated > 0:
                # Try to save the updated accounts back to the accounts file
                try:
                    accounts_path = self.accounts_path.text()
                    if accounts_path and os.path.exists(accounts_path):
                        with open(accounts_path, 'w') as f:
                            json.dump(self.accounts, f, indent=2)
                        self.log(f"Saved updated accounts to {accounts_path}")
                    else:
                        self.log("Warning: Could not save updated accounts to file (path not found)")
                except Exception as e:
                    self.log(f"Warning: Could not save updated accounts to file: {str(e)}")
                
                # Refresh the accounts display
                self.refresh_accounts()
                QMessageBox.information(self, "OAuth2 Tokens Updated", f"Updated OAuth2 tokens for {updated} accounts.")
            else:
                QMessageBox.warning(self, "No Updates", "No accounts were updated. Make sure the usernames match between the tokens file and accounts.")
                self.log("No accounts were updated with OAuth2 tokens")
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Invalid JSON", "The OAuth2 tokens file contains invalid JSON.")
            self.log(f"Error: The OAuth2 tokens file contains invalid JSON")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error applying OAuth2 tokens: {str(e)}")
            self.log(f"Error applying OAuth2 tokens: {str(e)}")
    
    def refresh_accounts(self):
        """Refresh the accounts table with current accounts data"""
        if not self.accounts:
            return
        
        self.accounts_table.setRowCount(0)  # Clear existing rows
        
        for account in self.accounts:
            row = self.accounts_table.rowCount()
            self.accounts_table.insertRow(row)
            
            # Fill in account details
            self.accounts_table.setItem(row, 0, QTableWidgetItem(account.get("username", "")))
            self.accounts_table.setItem(row, 1, QTableWidgetItem(account.get("server", "")))
            self.accounts_table.setItem(row, 2, QTableWidgetItem(str(account.get("port", ""))))
            self.accounts_table.setItem(row, 3, QTableWidgetItem(account.get("auth_type", "password")))
    
    def load_settings(self):
        """Load saved settings"""
        try:
            if os.path.exists("redmailer_gui_settings.json"):
                with open("redmailer_gui_settings.json", "r") as f:
                    settings = json.load(f)
                
                # Apply settings to UI elements
                if "accounts_path" in settings:
                    if settings["accounts_path"] != "":
                        self.accounts_path.setText(settings["accounts_path"])
                        try:
                            self.accounts = redmail.load_accounts(settings["accounts_path"])
                            self.refresh_accounts()
                            # Also populate reader accounts
                            self.populate_reader_accounts()
                        except Exception as e:
                            self.log(f"Error loading accounts: {str(e)}")
                
                if "targets_path" in settings:
                    if settings["targets_path"] != "":
                        self.targets_path.setText(settings["targets_path"])
                        try:
                            self.targets = redmail.load_targets(settings["targets_path"])
                        except Exception:
                            pass
                
                if "template_path" in settings:
                    if settings["template_path"] != "":
                        self.template_path.setText(settings["template_path"])
                        try:
                            with open(settings["template_path"], 'r') as f:
                                self.content_edit.setPlainText(f.read())
                        except Exception:
                            pass
                
                if "subject" in settings:
                    if settings["subject"] != "":
                        self.subject_input.setText(settings["subject"])
                
                if "content_type" in settings:
                    index = self.content_type.findText(settings["content_type"])
                    if index >= 0:
                        self.content_type.setCurrentIndex(index)
                
                if "delay" in settings:
                    self.delay_input.setValue(settings["delay"])
                
                if "jitter" in settings:
                    self.jitter_input.setValue(settings["jitter"])
                
                if "rotate" in settings:
                    self.rotate_input.setValue(settings["rotate"])
                
                if "use_ssl" in settings:
                    self.use_ssl.setChecked(settings["use_ssl"])
                
                if "no_tls" in settings:
                    self.no_tls.setChecked(settings["no_tls"])
                
                if "impersonate" in settings and settings["impersonate"] != "":
                    index = self.impersonate_combo.findText(settings["impersonate"])
                    if index >= 0:
                        self.impersonate_combo.setCurrentIndex(index)
                
                # Email reader settings
                if "reader_protocol" in settings:
                    index = self.protocol_combo.findText(settings["reader_protocol"])
                    if index >= 0:
                        self.protocol_combo.setCurrentIndex(index)
                
                if "reader_use_ssl" in settings:
                    self.reader_ssl.setChecked(settings["reader_use_ssl"])
                
                if "reader_limit" in settings:
                    self.limit_spin.setValue(settings["reader_limit"])
                
                self.log("Settings loaded successfully")
        except Exception as e:
            self.log(f"Error loading settings: {str(e)}")
    
    def save_settings(self):
        """Save current settings"""
        try:
            settings = {
                "accounts_path": self.accounts_path.text(),
                "targets_path": self.targets_path.text(),
                "template_path": self.template_path.text(),
                "subject": self.subject_input.text(),
                "content_type": self.content_type.currentText(),
                "delay": self.delay_input.value(),
                "jitter": self.jitter_input.value(),
                "rotate": self.rotate_input.value(),
                "use_ssl": self.use_ssl.isChecked(),
                "no_tls": self.no_tls.isChecked(),
                "impersonate": self.impersonate_combo.currentText() if self.impersonate_combo.currentIndex() > 0 else "",
                "reader_protocol": self.protocol_combo.currentText(),
                "reader_use_ssl": self.reader_ssl.isChecked(),
                "reader_limit": self.limit_spin.value()
            }
            
            with open("redmailer_gui_settings.json", "w") as f:
                json.dump(settings, f, indent=2)
            
            self.log("Settings saved successfully")
        except Exception as e:
            self.log(f"Error saving settings: {str(e)}")
    
    def get_template_content(self):
        """Get template content from either the editor or file"""
        if self.template_path.text() and os.path.exists(self.template_path.text()):
            try:
                with open(self.template_path.text(), 'r') as f:
                    return f.read()
            except Exception as e:
                self.log(f"Error reading template file: {str(e)}")
                return self.content_edit.toPlainText()
        else:
            return self.content_edit.toPlainText()
    
    def log(self, message):
        """Add a message to the log display"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_display.append(f"[{timestamp}] {message}")
        logger.info(message)
    
    def clear_log(self):
        """Clear the log display"""
        self.log_display.clear()
    
    def clear_results(self):
        """Clear the results table"""
        self.results_table.setRowCount(0)
    
    def validate_inputs(self):
        """Validate required inputs before sending emails"""
        if not self.accounts:
            QMessageBox.warning(self, "Missing Accounts", "No email accounts loaded. Please load an accounts file.")
            return False
        
        if not self.targets:
            QMessageBox.warning(self, "Missing Targets", "No target email addresses loaded. Please load a targets file.")
            return False
        
        if not self.subject_input.text():
            QMessageBox.warning(self, "Missing Subject", "Please enter an email subject.")
            return False
        
        if not self.content_edit.toPlainText() and (not self.template_path.text() or not os.path.exists(self.template_path.text())):
            QMessageBox.warning(self, "Missing Content", "Please enter email content or load a template file.")
            return False
        
        # Check if attachment exists
        if self.attachment_path.text() and not os.path.exists(self.attachment_path.text()):
            result = QMessageBox.warning(
                self, 
                "Attachment Not Found", 
                f"The attachment file does not exist: {self.attachment_path.text()}\n\nDo you want to continue without the attachment?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if result == QMessageBox.StandardButton.No:
                return False
        
        # Validate account credentials
        valid_accounts = 0
        for account in self.accounts:
            if account.get("auth_type") == "oauth2":
                oauth2 = account.get("oauth2", {})
                if oauth2.get("access_token") or (oauth2.get("refresh_token") and oauth2.get("client_id") and oauth2.get("client_secret")):
                    valid_accounts += 1
            elif account.get("password"):
                valid_accounts += 1
        
        if valid_accounts == 0:
            QMessageBox.warning(self, "Invalid Accounts", "No accounts with valid credentials found.")
            return False
        
        return True
    
    def send_test_email(self):
        """Send a single test email"""
        if not self.validate_inputs():
            return
        
        # Get a single target
        dialog_result = QInputDialog.getText(self, "Test Email", "Enter recipient email address:")
        target_email = dialog_result[0]
        ok = dialog_result[1]
        
        if not ok or not target_email:
            return
        
        # Validate email format
        if not validate_email(target_email):
            QMessageBox.warning(self, "Invalid Email", f"The email address '{target_email}' is not valid.")
            return
        
        # Set up test configuration
        self.log(f"Sending test email to {target_email}")
        self.results_table.setRowCount(0)
        
        # Configure and start the email thread
        self.email_thread = EmailSenderThread(
            accounts=self.accounts,
            targets=[target_email],
            template=self.get_template_content(),
            subject=self.subject_input.text(),
            content_type=self.content_type.currentText(),
            attachment=self.attachment_path.text() if self.attachment_path.text() else None,
            randomize_subject=self.randomize_subject.value(),
            randomize_content=self.randomize_content.value(),
            delay=0,  # No delay for test
            jitter=0,  # No jitter for test
            use_ssl=self.use_ssl.isChecked(),
            no_tls=self.no_tls.isChecked(),
            rotate=self.rotate_input.value(),
            impersonate=self.impersonate_combo.currentText() if self.impersonate_combo.currentIndex() > 0 else None
        )
        
        # Connect signals
        self.connect_thread_signals()
        
        # Start the thread
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.update_buttons(True)
        self.email_thread.start()
    
    def send_emails(self):
        """Send emails to all targets"""
        if not self.validate_inputs():
            return
        
        # Confirm with the user
        confirm = QMessageBox.question(
            self, 
            "Confirm Email Sending",
            f"Are you sure you want to send emails to {len(self.targets)} recipients?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm != QMessageBox.StandardButton.Yes:
            return
        
        # Clear previous results
        self.results_table.setRowCount(0)
        self.log(f"Starting email sending to {len(self.targets)} recipients")
        
        # Configure and start the email thread
        self.email_thread = EmailSenderThread(
            accounts=self.accounts,
            targets=self.targets,
            template=self.get_template_content(),
            subject=self.subject_input.text(),
            content_type=self.content_type.currentText(),
            attachment=self.attachment_path.text() if self.attachment_path.text() else None,
            randomize_subject=self.randomize_subject.value(),
            randomize_content=self.randomize_content.value(),
            delay=self.delay_input.value(),
            jitter=self.jitter_input.value(),
            use_ssl=self.use_ssl.isChecked(),
            no_tls=self.no_tls.isChecked(),
            rotate=self.rotate_input.value(),
            impersonate=self.impersonate_combo.currentText() if self.impersonate_combo.currentIndex() > 0 else None
        )
        
        # Connect signals
        self.connect_thread_signals()
        
        # Start the thread
        self.progress_bar.setRange(0, len(self.targets))
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.update_buttons(True)
        self.email_thread.start()
    
    def connect_thread_signals(self):
        """Connect the email sender thread signals"""
        self.email_thread.update_progress.connect(self.update_progress)
        self.email_thread.update_status.connect(self.update_status)
        self.email_thread.email_sent.connect(self.email_sent)
        self.email_thread.error_occurred.connect(self.handle_error)
        self.email_thread.finished_sending.connect(self.finished_sending)
    
    def handle_error(self, error_message):
        """Handle thread errors"""
        self.log(f"ERROR: {error_message}")
        QMessageBox.critical(self, "Error", error_message)
        self.progress_bar.setVisible(False)
        self.update_buttons(False)
    
    def update_buttons(self, is_sending):
        """Update button states based on sending status"""
        self.test_button.setEnabled(not is_sending)
        self.send_button.setEnabled(not is_sending)
        self.stop_button.setEnabled(is_sending)
    
    def stop_sending(self):
        """Stop the email sending process"""
        if self.email_thread and self.email_thread.isRunning():
            self.log("Stopping email sending process...")
            self.email_thread.stop()
    
    def update_progress(self, current, total):
        """Update the progress bar"""
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(current)
    
    def update_status(self, message):
        """Update the status message"""
        self.status_bar.showMessage(message)
        self.log(message)
    
    def email_sent(self, email, success, error_message):
        """Update the results table with email sending result"""
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        
        # Add email address
        self.results_table.setItem(row, 0, QTableWidgetItem(email))
        
        # Add status
        status_text = "Success" if success else "Failed"
        if not success and error_message:
            status_text = f"Failed: {error_message}"
            
        status_item = QTableWidgetItem(status_text)
        status_item.setBackground(Qt.GlobalColor.green if success else Qt.GlobalColor.red)
        self.results_table.setItem(row, 1, status_item)
        
        # Ensure the table scrolls to show the latest entry
        self.results_table.scrollToItem(status_item)
    
    def finished_sending(self, success_count, fail_count):
        """Handle completion of the email sending process"""
        self.progress_bar.setVisible(False)
        self.update_buttons(False)
        self.log(f"Email sending completed. {success_count} succeeded, {fail_count} failed.")
        
        # Show completion message
        QMessageBox.information(
            self,
            "Email Sending Complete",
            f"Email sending process completed.\n\n"
            f"• {success_count} emails sent successfully\n"
            f"• {fail_count} emails failed"
        )
    
    def export_results(self):
        """Export results to a CSV file"""
        if self.results_table.rowCount() == 0:
            QMessageBox.information(self, "No Results", "There are no results to export.")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Results", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w') as f:
                # Write header
                f.write("Email,Status,Timestamp\n")
                
                # Write data
                for row in range(self.results_table.rowCount()):
                    email = self.results_table.item(row, 0).text()
                    status = self.results_table.item(row, 1).text()
                    timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
                    
                    # CSV format
                    f.write(f"\"{email}\",\"{status}\",\"{timestamp}\"\n")
                    
            self.log(f"Results exported to {file_path}")
            QMessageBox.information(self, "Export Successful", f"Results successfully exported to {file_path}")
        except Exception as e:
            self.log(f"Error exporting results: {str(e)}")
            QMessageBox.critical(self, "Export Error", f"Failed to export results: {str(e)}")
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.email_thread and self.email_thread.isRunning():
            # Ask for confirmation if emails are being sent
            result = QMessageBox.question(
                self,
                "Confirm Exit",
                "Emails are still being sent. Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if result == QMessageBox.StandardButton.Yes:
                # Stop the email thread
                self.email_thread.stop()
                self.email_thread.wait()  # Wait for the thread to finish
                
                # Save settings before exit
                self.save_settings()
                
                # Disconnect from mail server if connected
                if self.email_connection:
                    try:
                        if self.connection_type == "imap":
                            self.email_connection.logout()
                        else:  # POP3
                            self.email_connection.quit()
                    except:
                        pass
                    
                event.accept()
            else:
                event.ignore()
        else:
            # Save settings before exit
            self.save_settings()
            
            # Disconnect from mail server if connected
            if self.email_connection:
                try:
                    if self.connection_type == "imap":
                        self.email_connection.logout()
                    else:  # POP3
                        self.email_connection.quit()
                except:
                    pass
                
            event.accept()

    def setup_reader_tab(self):
        """Set up the email reader tab"""
        layout = QVBoxLayout(self.reader_tab)
        
        # Connection settings group
        connection_group = QGroupBox("Connection Settings")
        connection_layout = QFormLayout(connection_group)
        
        # Protocol selection
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(["IMAP", "POP3"])
        self.protocol_combo.currentIndexChanged.connect(self.update_reader_port)
        self.protocol_combo.currentIndexChanged.connect(self.protocol_changed)
        connection_layout.addRow("Protocol:", self.protocol_combo)
        
        # Account selection
        self.reader_account_combo = QComboBox()
        self.reader_account_combo.setEditable(False)
        connection_layout.addRow("Account:", self.reader_account_combo)
        
        # Populate accounts if available
        if self.accounts:
            self.populate_reader_accounts()
        
        # Server settings
        self.reader_server = QLineEdit()
        connection_layout.addRow("Server:", self.reader_server)
        
        self.reader_port = QSpinBox()
        self.reader_port.setRange(1, 65535)
        self.reader_port.setValue(993)  # Default IMAP SSL port
        connection_layout.addRow("Port:", self.reader_port)
        
        # Username and password
        self.reader_username = QLineEdit()
        connection_layout.addRow("Username:", self.reader_username)
        
        self.reader_password = QLineEdit()
        self.reader_password.setEchoMode(QLineEdit.EchoMode.Password)
        connection_layout.addRow("Password:", self.reader_password)
        
        # Connection options
        self.reader_ssl = QCheckBox("Use SSL")
        self.reader_ssl.setChecked(True)
        self.reader_ssl.stateChanged.connect(self.update_reader_port)
        connection_layout.addRow("", self.reader_ssl)
        
        # Connect handlers to update fields when account is selected
        self.reader_account_combo.currentIndexChanged.connect(self.update_reader_account_fields)
        
        # Connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_mail_server)
        connection_layout.addRow("", self.connect_button)
        
        layout.addWidget(connection_group)
        
        # Folder selection (for IMAP)
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Folder:")
        self.folder_combo = QComboBox()
        self.folder_combo.setEnabled(False)
        self.refresh_folders_button = QPushButton("Refresh Folders")
        self.refresh_folders_button.setEnabled(False)
        self.refresh_folders_button.clicked.connect(self.refresh_folders)
        
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_combo)
        folder_layout.addWidget(self.refresh_folders_button)
        layout.addLayout(folder_layout)
        
        # Email list and controls
        emails_layout = QHBoxLayout()
        
        # Email list
        emails_list_layout = QVBoxLayout()
        emails_list_label = QLabel("Emails:")
        self.emails_table = QTableWidget()
        self.emails_table.setColumnCount(4)
        self.emails_table.setHorizontalHeaderLabels(["From", "Subject", "Date", "Attachments"])
        self.emails_table.horizontalHeader().setStretchLastSection(True)
        self.emails_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.emails_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.emails_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.emails_table.itemSelectionChanged.connect(self.email_selected)
        
        # Refresh emails button
        refresh_layout = QHBoxLayout()
        self.refresh_emails_button = QPushButton("Refresh Emails")
        self.refresh_emails_button.setEnabled(False)
        self.refresh_emails_button.clicked.connect(self.refresh_emails_in_thread)
        
        self.limit_spin = QSpinBox()
        self.limit_spin.setRange(10, 100)
        self.limit_spin.setValue(50)
        self.limit_spin.setSingleStep(10)
        
        refresh_layout.addWidget(QLabel("Limit:"))
        refresh_layout.addWidget(self.limit_spin)
        refresh_layout.addWidget(self.refresh_emails_button)
        refresh_layout.addStretch()
        
        emails_list_layout.addWidget(emails_list_label)
        emails_list_layout.addWidget(self.emails_table)
        emails_list_layout.addLayout(refresh_layout)
        
        # Email preview and attachment handling
        preview_layout = QVBoxLayout()
        preview_label = QLabel("Email Preview:")
        self.email_preview = QTextEdit()
        self.email_preview.setReadOnly(True)
        
        # Attachments
        attachments_label = QLabel("Attachments:")
        self.attachments_table = QTableWidget()
        self.attachments_table.setColumnCount(2)
        self.attachments_table.setHorizontalHeaderLabels(["Filename", "Size"])
        self.attachments_table.horizontalHeader().setStretchLastSection(True)
        self.attachments_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.attachments_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Download attachment button
        self.download_attachment_button = QPushButton("Download Selected Attachment")
        self.download_attachment_button.setEnabled(False)
        self.download_attachment_button.clicked.connect(self.download_attachment)
        
        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(self.email_preview)
        preview_layout.addWidget(attachments_label)
        preview_layout.addWidget(self.attachments_table)
        preview_layout.addWidget(self.download_attachment_button)
        
        # Split the layout
        emails_layout.addLayout(emails_list_layout, 1)
        emails_layout.addLayout(preview_layout, 1)
        
        layout.addLayout(emails_layout)

    def protocol_changed(self):
        """Handle protocol change in reader tab"""
        # When protocol changes, adapt the server address if it looks like an SMTP/IMAP/POP server
        server = self.reader_server.text().strip()
        protocol = self.protocol_combo.currentText()
        
        # Only try to adapt if we have a server value
        if not server:
            return
            
        # If the server looks like an SMTP/IMAP/POP server, attempt to adapt it
        if 'smtp.' in server.lower():
            # Switching from SMTP to IMAP/POP3
            if protocol == 'IMAP':
                new_server = server.lower().replace('smtp.', 'imap.')
            else:  # POP3
                new_server = server.lower().replace('smtp.', 'pop.')
            self.reader_server.setText(new_server)
            self.log(f"Adapted server for {protocol}: {new_server}")
        elif 'imap.' in server.lower() and protocol == 'POP3':
            # Switching from IMAP to POP3
            new_server = server.lower().replace('imap.', 'pop.')
            self.reader_server.setText(new_server)
            self.log(f"Adapted server for POP3: {new_server}")
        elif 'pop.' in server.lower() and protocol == 'IMAP':
            # Switching from POP3 to IMAP
            new_server = server.lower().replace('pop.', 'imap.')
            self.reader_server.setText(new_server)
            self.log(f"Adapted server for IMAP: {new_server}")
        
        # Use correct standard port for this protocol (IMPORTANT)
        use_ssl = self.reader_ssl.isChecked()
        if protocol == 'IMAP':
            self.reader_port.setValue(993 if use_ssl else 143)
        else:  # POP3
            self.reader_port.setValue(995 if use_ssl else 110)
        
        self.log(f"Updated port for {protocol}: {self.reader_port.value()}")

    def populate_reader_accounts(self):
        """Populate the account combo box with available accounts"""
        self.reader_account_combo.clear()
        self.reader_account_combo.addItem("Select an account...")
        
        # Track if we have any appropriate accounts for email reading
        has_proper_mail_accounts = False
        has_smtp_accounts = False
        
        for account in self.accounts:
            display_name = account.get('display_name', account['username'])
            
            # Check if this appears to be an SMTP account
            server = account.get('server', '')
            port = account.get('port', 0)
            
            # Common SMTP ports
            smtp_ports = [25, 465, 587, 2525]
            is_smtp_account = port in smtp_ports or 'smtp.' in server.lower()
            
            # Add a warning indicator for SMTP accounts
            if is_smtp_account:
                has_smtp_accounts = True
                display_text = f"{display_name} ({account['username']}) [SMTP - may need config]"
            else:
                has_proper_mail_accounts = True
                display_text = f"{display_name} ({account['username']})"
                
            self.reader_account_combo.addItem(display_text, account)
        
        # Add option for manual input
        self.reader_account_combo.addItem("Manual Entry")
        
        # Show a warning message if we only have SMTP accounts
        if has_smtp_accounts and not has_proper_mail_accounts:
            self.log("Warning: Your accounts.json appears to contain only SMTP accounts (for sending mail).")
            self.log("Email reading requires IMAP/POP3 accounts. The app will try to adapt your settings.")
            
            # If using the app for the first time, show a message box
            if not os.path.exists("redmailer_gui_settings.json"):
                QMessageBox.information(
                    self, 
                    "Account Configuration", 
                    "Your accounts appear to be configured for sending mail (SMTP), not receiving (IMAP/POP3).\n\n"
                    "The app will try to adapt these settings when you select an account, but you might need to "
                    "manually adjust server and port settings.\n\n"
                    "Common mail server settings:\n"
                    "- IMAP with SSL: server=imap.domain.com, port=993\n"
                    "- POP3 with SSL: server=pop.domain.com, port=995\n"
                    "- IMAP without SSL: server=imap.domain.com, port=143\n"
                    "- POP3 without SSL: server=pop.domain.com, port=110"
                )

    def update_reader_account_fields(self):
        """Update the fields when account is selected"""
        index = self.reader_account_combo.currentIndex()
        if index <= 0:  # Nothing or "Select an account..."
            self.reader_server.clear()
            self.reader_username.clear()
            self.reader_password.clear()
            self.reader_server.setReadOnly(False)
            self.reader_username.setReadOnly(False)
            self.reader_password.setReadOnly(False)
            return
        
        # Check if "Manual Entry" is selected
        if index == self.reader_account_combo.count() - 1:
            self.reader_server.clear()
            self.reader_username.clear()
            self.reader_password.clear()
            self.reader_server.setReadOnly(False)
            self.reader_username.setReadOnly(False)
            self.reader_password.setReadOnly(False)
            return
        
        # Get the selected account
        account = self.reader_account_combo.currentData()
        if not account:
            return
        
        # Detect if the account is for SMTP instead of IMAP/POP3
        protocol = self.protocol_combo.currentText()
        is_smtp_account = False
        
        # Check if account server contains SMTP indicators
        smtp_indicators = ['smtp', 'mail.', 'outgoing']
        account_server = account.get('server', '')
        account_port = account.get('port', 0)
        
        # Common SMTP ports
        smtp_ports = [25, 465, 587, 2525]
        
        if account_port in smtp_ports or any(indicator in account_server.lower() for indicator in smtp_indicators):
            is_smtp_account = True
            self.log(f"Note: Account appears to be an SMTP account, adapting for {protocol}")
        
        # Fill username and server (with possible modification)
        self.reader_username.setText(account['username'])
        
        # Get server name and potentially adapt it for IMAP/POP3
        if is_smtp_account:
            # Derive IMAP/POP3 server from username domain or SMTP server
            username = account['username']
            if '@' in username:
                domain = username.split('@')[1]
                
                # Try to detect proper server for domain
                self.reader_username.setText(username)
                if self.detect_mail_server():
                    # Server details were auto-detected and set
                    self.log(f"Auto-detected {protocol} settings for {domain}")
                else:
                    # Could not auto-detect, make an educated guess
                    if 'smtp.' in account_server:
                        # Replace smtp. with imap. or pop.
                        if protocol == 'IMAP':
                            guessed_server = account_server.replace('smtp.', 'imap.')
                        else:  # POP3
                            guessed_server = account_server.replace('smtp.', 'pop.')
                        self.reader_server.setText(guessed_server)
                        self.log(f"Guessed {protocol} server: {guessed_server}")
                    else:
                        # Just use the original server but warn
                        self.reader_server.setText(account_server)
                        self.log(f"Warning: Using SMTP server for {protocol}. This may not work.")
                    
                    # Always use appropriate port for protocol regardless of account settings
                    use_ssl = self.reader_ssl.isChecked()
                    if protocol == 'IMAP':
                        self.reader_port.setValue(993 if use_ssl else 143)
                    else:  # POP3
                        self.reader_port.setValue(995 if use_ssl else 110)
            else:
                # No domain in username, just use the server
                self.reader_server.setText(account_server)
                # Always use appropriate port for protocol
                use_ssl = self.reader_ssl.isChecked()
                if protocol == 'IMAP':
                    self.reader_port.setValue(993 if use_ssl else 143)
                else:  # POP3
                    self.reader_port.setValue(995 if use_ssl else 110)
        else:
            # Not an SMTP account, use server directly
            self.reader_server.setText(account_server)
            # Always use appropriate port for protocol regardless of account settings
            use_ssl = self.reader_ssl.isChecked()
            if protocol == 'IMAP':
                self.reader_port.setValue(993 if use_ssl else 143)
            else:  # POP3
                self.reader_port.setValue(995 if use_ssl else 110)
        
        # Set password if available
        if 'password' in account:
            self.reader_password.setText(account['password'])
        else:
            self.reader_password.clear()
        
        # Make fields read-only for accounts
        self.reader_server.setReadOnly(False)  # Allow server to be edited
        self.reader_username.setReadOnly(True)
        
        # But allow password to be editable since it might not be stored
        self.reader_password.setReadOnly(False)

    def update_reader_port(self):
        """Update the port based on selected protocol"""
        protocol = self.protocol_combo.currentText()
        use_ssl = self.reader_ssl.isChecked()
        
        # Standard ports for mail protocols
        standard_ports = {
            "IMAP": {True: 993, False: 143},  # SSL/non-SSL
            "POP3": {True: 995, False: 110},
            "SMTP": {True: 465, False: 25}    # For reference
        }
        
        # Set port based on protocol and SSL setting
        if protocol in standard_ports:
            self.reader_port.setValue(standard_ports[protocol][use_ssl])
        else:
            # Default fallback
            self.reader_port.setValue(993 if use_ssl else 143)

    def connect_to_mail_server(self):
        """Connect to the mail server using the specified settings"""
        # Get connection settings
        protocol = self.protocol_combo.currentText()
        
        # Check if account is selected
        account_index = self.reader_account_combo.currentIndex()
        use_oauth2 = False
        oauth2_params = {}
        
        # Default values
        server = self.reader_server.text().strip()
        port = self.reader_port.value()
        username = self.reader_username.text().strip()
        password = self.reader_password.text()
        use_ssl = self.reader_ssl.isChecked()
        
        # Check if we're using an account from the list
        if account_index > 0 and account_index < self.reader_account_combo.count() - 1:
            account = self.reader_account_combo.currentData()
            if account:
                # We don't use server/port directly from account anymore
                # Instead we use what's currently in the UI fields
                # This allows for manual adjustment from SMTP to IMAP/POP3
                username = account.get('username', username)
                
                # OAuth2 authentication
                if account.get('auth_type') == 'oauth2' and 'oauth2' in account:
                    use_oauth2 = True
                    oauth2_config = account.get('oauth2', {})
                    oauth2_params = {
                        'access_token': oauth2_config.get('access_token'),
                        'refresh_token': oauth2_config.get('refresh_token'),
                        'client_id': oauth2_config.get('client_id'),
                        'client_secret': oauth2_config.get('client_secret'),
                        'token_type': oauth2_config.get('type')
                    }
                else:
                    # Use password from account if available
                    if 'password' in account and not password:
                        password = account['password']
        else:
            # For manual entry, try to detect server settings if server is empty
            if not server and username:
                self.detect_mail_server()
                # Get updated values
                server = self.reader_server.text().strip()
                port = self.reader_port.value()
                use_ssl = self.reader_ssl.isChecked()
        
        # Validate inputs
        if not server or not username or (not password and not use_oauth2):
            QMessageBox.warning(self, "Missing Input", "Please enter server, username, and password.")
            return
        
        # Additional validation for potentially misconfigured connections
        is_likely_smtp = False
        
        # Check for common SMTP ports
        smtp_ports = [25, 465, 587, 2525]
        if port in smtp_ports:
            is_likely_smtp = True
        
        # Check for SMTP in server name
        smtp_indicators = ['smtp', 'mail.', 'outgoing']
        if any(indicator in server.lower() for indicator in smtp_indicators):
            is_likely_smtp = True
        
        # Warn if using likely SMTP server for IMAP/POP3
        if is_likely_smtp:
            response = QMessageBox.warning(
                self,
                "Possible Misconfiguration",
                f"The server '{server}:{port}' appears to be an SMTP server (for sending mail), "
                f"but you're trying to connect with {protocol} (for receiving mail).\n\n"
                f"Common {protocol} ports are:\n"
                f"- {protocol} with SSL: {993 if protocol == 'IMAP' else 995}\n"
                f"- {protocol} without SSL: {143 if protocol == 'IMAP' else 110}\n\n"
                f"Do you want to proceed with the current settings?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if response == QMessageBox.StandardButton.No:
                # Suggest correct port
                suggest_port = 993 if protocol == 'IMAP' and use_ssl else 143 if protocol == 'IMAP' else 995 if use_ssl else 110
                
                # Try to suggest a better server name
                suggest_server = server
                if 'smtp.' in server.lower():
                    if protocol == 'IMAP':
                        suggest_server = server.lower().replace('smtp.', 'imap.')
                    else:
                        suggest_server = server.lower().replace('smtp.', 'pop.')
                
                self.reader_port.setValue(suggest_port)
                if suggest_server != server:
                    self.reader_server.setText(suggest_server)
                
                self.log(f"Connection attempt canceled. Suggested {protocol} settings: {suggest_server}:{suggest_port}")
                return
        
        # Disconnect if already connected
        if self.email_connection:
            try:
                self.disconnect_from_mail_server()
            except Exception as e:
                self.log(f"Error during disconnect: {str(e)}")
        
        # Disable connect button during connection
        self.connect_button.setEnabled(False)
        self.connect_button.setText("Connecting...")
        QApplication.processEvents()
        
        try:
            # Check if the server looks like an SMTP server instead of IMAP/POP3
            smtp_indicators = ['smtp', 'mail', 'outgoing']
            if any(indicator in server.lower() for indicator in smtp_indicators) and protocol in ["IMAP", "POP3"]:
                self.log(f"Warning: Server name contains SMTP indicators but protocol is {protocol}. Check your settings.")
            
            # Connect to the mail server
            if protocol == "IMAP":
                self.connection_type = "imap"
                
                if use_oauth2:
                    # Currently not implemented for IMAP - fall back to password
                    self.log("OAuth2 not yet implemented for IMAP reading, falling back to password")
                    
                # Attempt connection with SSL first if requested
                if use_ssl:
                    self.log(f"Attempting IMAP connection with SSL to {server}:{port}")
                    self.email_connection, error = redmail.connect_to_imap(
                        server, port, username, password, use_ssl=True
                    )
                    
                    # If SSL fails, try without SSL as fallback
                    if error and "[SSL:" in str(error):
                        self.log(f"SSL connection failed: {error}. Trying without SSL...")
                        self.email_connection, error = redmail.connect_to_imap(
                            server, port, username, password, use_ssl=False
                        )
                else:
                    self.log(f"Attempting IMAP connection without SSL to {server}:{port}")
                    self.email_connection, error = redmail.connect_to_imap(
                        server, port, username, password, use_ssl=False
                    )
            else:  # POP3
                self.connection_type = "pop3"
                
                if use_oauth2:
                    # Currently not implemented for POP3 - fall back to password
                    self.log("OAuth2 not yet implemented for POP3 reading, falling back to password")
                    
                # Attempt connection with SSL first if requested
                if use_ssl:
                    self.log(f"Attempting POP3 connection with SSL to {server}:{port}")
                    self.email_connection, error = redmail.connect_to_pop3(
                        server, port, username, password, use_ssl=True
                    )
                    
                    # If SSL fails, try without SSL as fallback
                    if error and "[SSL:" in str(error):
                        self.log(f"SSL connection failed: {error}. Trying without SSL...")
                        self.email_connection, error = redmail.connect_to_pop3(
                            server, port, username, password, use_ssl=False
                        )
                else:
                    self.log(f"Attempting POP3 connection without SSL to {server}:{port}")
                    self.email_connection, error = redmail.connect_to_pop3(
                        server, port, username, password, use_ssl=False
                    )
            
            # Check if connection was successful
            if error:
                self.log(f"Connection error: {error}")
                
                # Check for common errors and provide helpful messages
                if "wrong version number" in str(error):
                    QMessageBox.critical(self, "Connection Error", 
                        f"Failed to connect: SSL error. Try turning off 'Use SSL' or use a different port.\n\nDetails: {error}")
                elif "unexpect" in str(error) and "ESMTP" in str(error):
                    QMessageBox.critical(self, "Connection Error", 
                        f"The server {server}:{port} appears to be an SMTP server, not an {protocol} server.\n\nCheck your server and port settings.")
                else:
                    QMessageBox.critical(self, "Connection Error", f"Failed to connect: {error}")
                    
                self.connect_button.setText("Connect")
                self.connect_button.setEnabled(True)
                return
            
            self.log(f"Successfully connected to {protocol} server: {server}")
            
            # Enable UI elements based on protocol
            if protocol == "IMAP":
                self.folder_combo.setEnabled(True)
                self.refresh_folders_button.setEnabled(True)
                # Get folders
                self.refresh_folders()
            else:
                self.folder_combo.setEnabled(False)
                self.refresh_folders_button.setEnabled(False)
                self.folder_combo.clear()
            
            # Enable email refresh
            self.refresh_emails_button.setEnabled(True)
            
            # Connect button becomes disconnect
            self.connect_button.setText("Disconnect")
            self.connect_button.clicked.disconnect()
            self.connect_button.clicked.connect(self.disconnect_from_mail_server)
            self.connect_button.setEnabled(True)
            
            # Load emails
            self.refresh_emails_in_thread()
        except Exception as e:
            self.log(f"Error connecting to mail server: {str(e)}")
            QMessageBox.critical(self, "Connection Error", f"An error occurred: {str(e)}")
            self.connect_button.setText("Connect")
            self.connect_button.setEnabled(True)

    def disconnect_from_mail_server(self):
        """Disconnect from the mail server"""
        if not self.email_connection:
            self.log("Not connected to any mail server")
            return
        
        self.log("Disconnecting from mail server...")
        
        try:
            # Cancel any running email fetch thread
            if self.email_reader_thread and self.email_reader_thread.isRunning():
                self.log("Waiting for email reader thread to finish...")
                self.email_reader_thread.wait(2000)  # Wait up to 2 seconds
            
            # Disconnect based on connection type
            if self.connection_type == "imap":
                self.email_connection.logout()
                self.log("Successfully logged out from IMAP server")
            else:  # POP3
                self.email_connection.quit()
                self.log("Successfully disconnected from POP3 server")
            
        except Exception as e:
            self.log(f"Error during disconnection: {str(e)}")
        finally:
            # Reset connection state
            self.email_connection = None
            self.connection_type = None
            
            # Reset UI state
            self.connect_button.setText("Connect")
            self.connect_button.clicked.disconnect()
            self.connect_button.clicked.connect(self.connect_to_mail_server)
            self.connect_button.setEnabled(True)
            
            self.folder_combo.setEnabled(False)
            self.refresh_folders_button.setEnabled(False)
            self.refresh_emails_button.setEnabled(False)
            
            # Clear data
            self.folder_combo.clear()
            self.emails_table.setRowCount(0)
            self.attachments_table.setRowCount(0)
            self.email_preview.clear()
            self.emails = []
            self.download_attachment_button.setEnabled(False)
            
            self.log("Disconnected from mail server")

    def refresh_folders(self):
        """Refresh the list of IMAP folders"""
        if not self.email_connection or self.connection_type != "imap":
            self.log("Cannot refresh folders: Not connected to an IMAP server")
            return
        
        # Disable refresh button during operation
        self.refresh_folders_button.setEnabled(False)
        self.refresh_folders_button.setText("Loading...")
        QApplication.processEvents()
        
        try:
            folders, error = redmail.get_imap_folders(self.email_connection)
            
            if error:
                self.log(f"Error getting folders: {error}")
                QMessageBox.warning(self, "Folder Error", f"Failed to get folders: {error}")
                self.refresh_folders_button.setText("Refresh Folders")
                self.refresh_folders_button.setEnabled(True)
                return
            
            # Update folder dropdown
            self.folder_combo.clear()
            
            # If no folders were found
            if not folders:
                self.log("No folders found on the server")
                self.folder_combo.addItem("INBOX")
            else:
                for folder in folders:
                    self.folder_combo.addItem(folder)
                
                # Select INBOX if available
                inbox_index = self.folder_combo.findText("INBOX")
                if inbox_index >= 0:
                    self.folder_combo.setCurrentIndex(inbox_index)
                
                self.log(f"Loaded {len(folders)} folders")
            
            # Enable folder selection
            self.folder_combo.setEnabled(True)
            
        except Exception as e:
            self.log(f"Error getting folders: {str(e)}")
            QMessageBox.warning(self, "Folder Error", f"An error occurred: {str(e)}")
        finally:
            # Re-enable the button
            self.refresh_folders_button.setText("Refresh Folders")
            self.refresh_folders_button.setEnabled(True)

    def refresh_emails_in_thread(self):
        """Refresh emails in a background thread to prevent GUI freezing"""
        if not self.email_connection:
            return
        
        self.refresh_emails_button.setEnabled(False)
        self.refresh_emails_button.setText("Loading...")
        QApplication.processEvents()
        
        folder = None
        if self.connection_type == "imap":
            folder = self.folder_combo.currentText()
            self.log(f"Loading emails from folder: {folder}")
        else:
            self.log("Loading emails via POP3")
        
        # Create and configure the thread
        self.email_reader_thread = EmailReaderThread(
            self.email_connection,
            self.connection_type,
            folder,
            self.limit_spin.value()
        )
        
        # Connect signals
        self.email_reader_thread.update_status.connect(self.log)
        self.email_reader_thread.error_occurred.connect(self.handle_email_error)
        self.email_reader_thread.emails_retrieved.connect(self.update_emails_table)
        
        # Start the thread
        self.email_reader_thread.start()

    def update_emails_table(self, emails):
        """Update the emails table with retrieved emails"""
        # Store emails
        self.emails = emails
        
        # Update email table
        self.emails_table.setRowCount(0)
        for email in emails:
            row = self.emails_table.rowCount()
            self.emails_table.insertRow(row)
            
            # Fill email details
            self.emails_table.setItem(row, 0, QTableWidgetItem(email['from']))
            self.emails_table.setItem(row, 1, QTableWidgetItem(email['subject']))
            self.emails_table.setItem(row, 2, QTableWidgetItem(email['date']))
            
            # Show attachment indicator
            attachments_text = f"{len(email['attachments'])} attachments" if email['has_attachments'] else "None"
            self.emails_table.setItem(row, 3, QTableWidgetItem(attachments_text))
        
        self.log(f"Loaded {len(emails)} emails")
        
        # Reset button
        self.refresh_emails_button.setText("Refresh Emails")
        self.refresh_emails_button.setEnabled(True)
        
        # Clear preview
        self.email_preview.clear()
        self.attachments_table.setRowCount(0)
        self.download_attachment_button.setEnabled(False)

    def handle_email_error(self, error_message):
        """Handle errors from the email reader thread"""
        self.log(f"ERROR: {error_message}")
        QMessageBox.warning(self, "Email Error", error_message)
        
        # Reset button
        self.refresh_emails_button.setText("Refresh Emails")
        self.refresh_emails_button.setEnabled(True)

    def email_selected(self):
        """Handle email selection"""
        selected_rows = self.emails_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        # Get the selected email
        row_index = selected_rows[0].row()
        if row_index < 0 or row_index >= len(self.emails):
            return
        
        email = self.emails[row_index]
        
        # Update preview
        body_text = email['body']
        if body_text:
            # If it's HTML, use it as is; otherwise, escape it and add line breaks
            if '<html' in body_text.lower() or '<body' in body_text.lower():
                self.email_preview.setHtml(body_text)
            else:
                formatted_text = html.escape(body_text).replace('\n', '<br>')
                self.email_preview.setHtml(f"<pre>{formatted_text}</pre>")
        else:
            self.email_preview.setPlainText("No content available")
        
        # Update attachments table
        self.attachments_table.setRowCount(0)
        for i, attachment in enumerate(email['attachments']):
            row = self.attachments_table.rowCount()
            self.attachments_table.insertRow(row)
            
            # Show attachment info
            self.attachments_table.setItem(row, 0, QTableWidgetItem(attachment['filename']))
            size_text = f"{attachment['size'] / 1024:.1f} KB"
            self.attachments_table.setItem(row, 1, QTableWidgetItem(size_text))
        
        # Enable download button if there are attachments
        self.download_attachment_button.setEnabled(len(email['attachments']) > 0)

    def download_attachment(self):
        """Download the selected attachment"""
        # Get selected email
        email_rows = self.emails_table.selectionModel().selectedRows()
        if not email_rows:
            return
        
        email_index = email_rows[0].row()
        if email_index < 0 or email_index >= len(self.emails):
            return
        
        email = self.emails[email_index]
        
        # Get selected attachment
        attachment_rows = self.attachments_table.selectionModel().selectedRows()
        if not attachment_rows:
            QMessageBox.warning(self, "No Selection", "Please select an attachment to download.")
            return
        
        attachment_index = attachment_rows[0].row()
        if attachment_index < 0 or attachment_index >= len(email['attachments']):
            return
        
        attachment = email['attachments'][attachment_index]
        
        # Ask for save location
        save_dir = QFileDialog.getExistingDirectory(
            self, "Select Folder to Save Attachment", ""
        )
        
        if not save_dir:
            return
        
        try:
            # Save the attachment
            part_index = attachment['part_index']
            file_path, error = redmail.save_attachment(
                email['raw_message'], part_index, save_dir
            )
            
            if error:
                self.log(f"Error saving attachment: {error}")
                QMessageBox.warning(self, "Download Error", f"Failed to save attachment: {error}")
                return
            
            self.log(f"Attachment saved to: {file_path}")
            QMessageBox.information(
                self, "Download Complete", 
                f"Attachment '{attachment['filename']}' was saved to:\n{file_path}"
            )
        except Exception as e:
            self.log(f"Error downloading attachment: {str(e)}")
            QMessageBox.warning(self, "Download Error", f"An error occurred: {str(e)}")

    def detect_mail_server(self):
        """Detect mail server settings based on username/email domain"""
        username = self.reader_username.text().strip()
        protocol = self.protocol_combo.currentText()
        
        # Only auto-detect if we have an email address
        if not username or '@' not in username:
            return False
            
        # Extract the domain part
        domain = username.split('@')[1].lower()
        
        # Common email provider settings
        provider_settings = {
            'gmail.com': {
                'IMAP': {'server': 'imap.gmail.com', 'port': 993, 'ssl': True},
                'POP3': {'server': 'pop.gmail.com', 'port': 995, 'ssl': True}
            },
            'outlook.com': {
                'IMAP': {'server': 'outlook.office365.com', 'port': 993, 'ssl': True},
                'POP3': {'server': 'outlook.office365.com', 'port': 995, 'ssl': True}
            },
            'hotmail.com': {
                'IMAP': {'server': 'outlook.office365.com', 'port': 993, 'ssl': True},
                'POP3': {'server': 'outlook.office365.com', 'port': 995, 'ssl': True}
            },
            'live.com': {
                'IMAP': {'server': 'outlook.office365.com', 'port': 993, 'ssl': True},
                'POP3': {'server': 'outlook.office365.com', 'port': 995, 'ssl': True}
            },
            'yahoo.com': {
                'IMAP': {'server': 'imap.mail.yahoo.com', 'port': 993, 'ssl': True},
                'POP3': {'server': 'pop.mail.yahoo.com', 'port': 995, 'ssl': True}
            },
            'aol.com': {
                'IMAP': {'server': 'imap.aol.com', 'port': 993, 'ssl': True},
                'POP3': {'server': 'pop.aol.com', 'port': 995, 'ssl': True}
            },
            'icloud.com': {
                'IMAP': {'server': 'imap.mail.me.com', 'port': 993, 'ssl': True},
                'POP3': {'server': 'pop.mail.me.com', 'port': 995, 'ssl': True}
            },
            'protonmail.com': {
                'IMAP': {'server': 'imap.protonmail.ch', 'port': 993, 'ssl': True},
                'POP3': {'server': 'pop.protonmail.ch', 'port': 995, 'ssl': True}
            },
            'zoho.com': {
                'IMAP': {'server': 'imap.zoho.com', 'port': 993, 'ssl': True},
                'POP3': {'server': 'pop.zoho.com', 'port': 995, 'ssl': True}
            }
        }
        
        # Check if we know this domain
        if domain in provider_settings and protocol in provider_settings[domain]:
            settings = provider_settings[domain][protocol]
            
            # Update UI with detected settings
            self.reader_server.setText(settings['server'])
            self.reader_port.setValue(settings['port'])
            self.reader_ssl.setChecked(settings['ssl'])
            
            self.log(f"Auto-detected {protocol} settings for {domain}")
            return True
            
        return False

class EmailReaderThread(QThread):
    """Thread for retrieving emails without blocking the GUI"""
    update_status = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    emails_retrieved = pyqtSignal(list)
    
    def __init__(self, connection, connection_type, folder=None, limit=50):
        super().__init__()
        self.connection = connection
        self.connection_type = connection_type
        self.folder = folder
        self.limit = limit
    
    def run(self):
        """Run the email retrieval process"""
        try:
            self.update_status.emit(f"Retrieving emails...")
            
            if self.connection_type == "imap":
                emails, error = redmail.get_emails_imap(self.connection, self.folder, self.limit)
            else:  # POP3
                emails, error = redmail.get_emails_pop3(self.connection, self.limit)
            
            if error:
                self.error_occurred.emit(f"Error retrieving emails: {error}")
            else:
                self.emails_retrieved.emit(emails)
                self.update_status.emit(f"Retrieved {len(emails)} emails")
        except Exception as e:
            self.error_occurred.emit(f"Error retrieving emails: {str(e)}")


def main():
    try:
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName(APP_NAME)
        app.setApplicationVersion(APP_VERSION)
        app.setWindowIcon(get_app_icon())
        
        # Set application style
        app.setStyle("Fusion")
        
        # Show splash screen
        splash_pixmap = create_splash_image()
        splash = QSplashScreen(splash_pixmap)
        splash.show()

        # Process events to make sure splash screen is visible
        app.processEvents()
        
        # Add startup message to splash screen
        splash.showMessage("Loading application...", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
        
        # Create and set up main window (with small delay to show splash)
        window = MainWindow()
        
        # Simulate loading delay for better user experience
        for i in range(1, 6):
            splash.showMessage(f"Initializing components... ({i}/5)", 
                              Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, 
                              Qt.GlobalColor.white)
            app.processEvents()
            time.sleep(0.2)
        
        # Show the main window and close splash
        window.show()
        splash.finish(window)
        
        # Start application event loop
        sys.exit(app.exec())
    except Exception as e:
        # If an error occurs during startup, show error dialog
        import traceback
        error_message = f"Error starting application: {str(e)}\n\n{traceback.format_exc()}"
        print(error_message)
        
        # Try to show error dialog if QApplication was created
        try:
            if 'app' in locals():
                QMessageBox.critical(None, "Startup Error", error_message)
        except:
            pass
        
        sys.exit(1)
# Entry point
if __name__ == "__main__":
    main()