import os
import json
import logging
import threading
from queue import Queue
from datetime import datetime
import requests
from configure import LOG_FILE, LOG_LEVEL, SPLUNK_HOST, SPLUNK_PORT, MAX_QUEUE_SIZE, SPLUNK_INDEX, SPLUNK_TOKEN, SPLUNK_SOURCE

# === FUNCTIONS ===

def get_logger():
    """Khởi tạo và cấu hình logger."""
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler
    file_handler = logging.FileHandler(LOG_FILE, mode='a')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Splunk handler (HEC)
    if SPLUNK_HOST and SPLUNK_PORT:
        splunk_handler = SplunkHecHandler(SPLUNK_HOST, SPLUNK_PORT)
        splunk_handler.setFormatter(formatter)
        logger.addHandler(splunk_handler)

    return logger

class SplunkHecHandler(logging.Handler):
    """Handler để gửi log đến Splunk qua HEC."""

    def __init__(self, host, port, token=SPLUNK_TOKEN, index=SPLUNK_INDEX, source=SPLUNK_SOURCE):
        super().__init__()
        self.host = host
        self.port = port
        self.token = token
        self.index = index
        self.source = source
        self.url = f"https://{self.host}:{self.port}/services/collector"

    def emit(self, record):
        """Gửi log event đến Splunk qua HEC."""
        log_entry = self.format(record)
        try:
            self.send_to_splunk(log_entry)
        except Exception as e:
            print(f"Error sending log to Splunk: {e}")

    def send_to_splunk(self, log_entry):
        """Gửi log entry đến Splunk qua HEC."""
        headers = {
            "Authorization": f"Splunk {self.token}",
            "Content-Type": "application/json"
        }
        data = {
            "event": log_entry,
            "time": datetime.utcnow().isoformat(),
            "sourcetype": "python_logger",
            "index": self.index,
            "source": self.source
        }
        response = requests.post(self.url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            print(f"Error sending log to Splunk: {response.status_code}, {response.text}")

def log_attack(**kwargs):
    """Ghi lại hành vi của attacker.

    Ví dụ:
    log_attack(event_type="file_access", filepath="/etc/passwd", username="attacker")
    """
    global logger
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        **kwargs
    }
    logger.info(json.dumps(event))

# === KHỞI TẠO ===
logger = get_logger()
log_queue = Queue(maxsize=MAX_QUEUE_SIZE)
log_thread = threading.Thread(target=logger.info, args=(log_queue,))
log_thread.daemon = True
log_thread.start()