import os
import json
import logging
import threading
from queue import Queue
from datetime import datetime
import socket
from config import LOG_ROOT, LOG_FILE, LOG_LEVEL, SPLUNK_HOST, SPLUNK_PORT, MAX_QUEUE_SIZE

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
    """Handler to send logs to Splunk over UDP."""

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def emit(self, record):
        """Send log events to Splunk via UDP."""
        log_entry = self.format(record)
        try:
            self.send_to_splunk(log_entry)
        except Exception as e:
            print(f"Error sending log to Splunk: {e}")

    def send_to_splunk(self, log_entry):
        """Send log entry to Splunk over UDP socket."""
        self.socket.sendto(log_entry.encode(), (self.host, self.port))

def log_command(**kwargs):
    """Record attacker behavior..

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
    """Record the attacker's reconnaissance activity."""
    global logger
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "Reconnaissance activity",
        **kwargs
    }
    logger.info(json.dumps(event))

def log_login(**kwargs):
    """Record the attacker's login information."""
    global logger
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "Login_activity",
        **kwargs
    }
    logger.info(json.dumps(event))

def log_exploitation(**kwargs):
    """Record attacker's exploit activity."""
    global logger
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "Exploitation_activity",
        **kwargs
    }
    logger.info(json.dumps(event))

# === KHỞI TẠO ===
logger = get_logger()
log_queue = Queue(maxsize=MAX_QUEUE_SIZE)
log_thread = threading.Thread(target=logger.info, args=(log_queue,))
log_thread.daemon = True
log_thread.start()
