import os
import json
import logging
import threading
from queue import Queue
from datetime import datetime
import socket
from Settings.config import LOG_ROOT, SPLUNK_HOST, SPLUNK_PORT

# === CONFIGURATION ===

# General configuration
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.path.join(LOG_ROOT, 'attack_logs.json')
MAX_QUEUE_SIZE = 10000

# === FUNCTIONS ===

def get_logger():
    """Initialize and configure the logger."""
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler
    file_handler = logging.FileHandler(LOG_FILE, mode='a')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Splunk handler (UDP)
    if SPLUNK_HOST and SPLUNK_PORT:
        splunk_handler = SplunkUdpHandler(SPLUNK_HOST, SPLUNK_PORT)
        splunk_handler.setFormatter(formatter)
        logger.addHandler(splunk_handler)

    return logger

class SplunkUdpHandler(logging.Handler):
    """Handler for sending logs to Splunk via UDP."""

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def emit(self, record):
        """Send log event to Splunk via UDP."""
        log_entry = self.format(record)
        try:
            self.send_to_splunk(log_entry)
        except Exception as e:
            print(f"Error sending log to Splunk: {e}")

    def send_to_splunk(self, log_entry):
        """Send log entry to Splunk via UDP socket."""
        # Assuming Splunk is configured to receive logs over UDP on port 514 (adjust if needed)
        self.socket.sendto(log_entry.encode(), (self.host, self.port))

def log_command(**kwargs):
    """Log attacker's command behavior.

    Example:
    log_attack(event_type="file_access", filepath="/etc/passwd", username="attacker")
    """
    global logger
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        **kwargs
    }
    logger.info(json.dumps(event))

def log_recon(**kwargs):
    """Log attacker's reconnaissance activity."""
    global logger
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "Reconnaissance activity",
        **kwargs
    }
    logger.info(json.dumps(event))

def log_login(**kwargs):
    """Log attacker's login information."""
    global logger
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "Login_activity",
        **kwargs
    }
    logger.info(json.dumps(event))

def log_exploitation(**kwargs):
    """Log attacker's exploitation activity."""
    global logger
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "Exploitation_activity",
        **kwargs
    }
    logger.info(json.dumps(event))


def log_event(message, level=logging.INFO):
    """Logs a message to the Splunk handler (if configured) and the file handler.

    Args:
        message (str): The message to log.
        level (int, optional): The logging level (INFO, DEBUG, etc.). Defaults to logging.INFO.
    """
    logger.log(level, message)


# === INITIALIZATION ===
logger = get_logger()
log_queue = Queue(maxsize=MAX_QUEUE_SIZE)
log_thread = threading.Thread(target=logger.info, args=(log_queue,))
log_thread.daemon = True
log_thread.start()
