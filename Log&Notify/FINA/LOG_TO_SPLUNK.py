import os
import json
import logging
import threading
from queue import Queue
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# === CẤU HÌNH ===

# Cấu hình chung
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_FILE = "attack_logs.json"
MAX_QUEUE_SIZE = 10000

# Cấu hình Splunk HEC (bỏ comment nếu sử dụng)
SPLUNK_HEC_URL = os.environ.get("SPLUNK_HEC_URL", "") 
SPLUNK_HEC_TOKEN = os.environ.get("SPLUNK_HEC_TOKEN", "")
SPLUNK_HEC_INDEX = os.environ.get("SPLUNK_HEC_INDEX", "main")
SPLUNK_HEC_SOURCE = os.environ.get("SPLUNK_HEC_SOURCE", "esxi_honeypot")


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

    # Splunk handler (nếu được cấu hình)
    if SPLUNK_HEC_URL and SPLUNK_HEC_TOKEN:
        splunk_handler = SplunkHandler()
        splunk_handler.setFormatter(formatter)
        logger.addHandler(splunk_handler)

    return logger

class SplunkHandler(logging.Handler):
    """Handler để gửi log đến Splunk HEC."""

    def __init__(self, level=logging.NOTSET):
        super().__init__(level=level)
        # Cấu hình retry cho requests
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1,
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def emit(self, record):
        """Gửi log event đến Splunk HEC."""
        log_entry = self.format(record)
        try:
            self.send_to_splunk(log_entry)
        except Exception as e:
            print(f"Error sending log to Splunk: {e}")

    def send_to_splunk(self, log_entry):
        """Gửi log entry đến Splunk HEC bằng requests."""
        headers = {
            "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
            "Content-Type": "application/json",
        }
        data = {
            "index": SPLUNK_HEC_INDEX,
            "source": SPLUNK_HEC_SOURCE,
            "event": json.loads(log_entry),
        }
        response = self.session.post(SPLUNK_HEC_URL, headers=headers, json=data)
        response.raise_for_status() 


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