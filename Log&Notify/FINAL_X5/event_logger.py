import os
import json
import time
import threading
from queue import Queue
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import logging
import socket  # Import socket cho kết nối TCP

from config import LOG_ROOT, FILE_LOG_DIR, MAX_QUEUE_SIZE, SPLUNK_HOST, SPLUNK_PORT, LOG_CONFIG, ADMIN_EMAIL, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD

# Cấu hình logging cơ bản
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Queue để lưu trữ log event
log_queue = Queue(maxsize=MAX_QUEUE_SIZE)

# Khóa để đồng bộ hóa việc ghi log vào file
log_lock = threading.Lock()

if not os.path.exists(FILE_LOG_DIR):
    os.makedirs(FILE_LOG_DIR) 

# Hàm ghi log SSH
def log_ssh_event(ip_address, username, command):
    """Ghi log event liên quan đến SSH."""
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": ip_address,
        "ssh_username": username,
        "ssh_commands": [command] if command else [],  # Chỉ thêm command nếu có
        "file_events": [],
        "severity": "NORMAL"  # Mặc định là NORMAL
    }

    # Ghi log vào file
    with log_lock:
        with open(os.path.join(FILE_LOG_DIR, "honeypot_log.json"), "a") as f:
            f.write(json.dumps(log_entry) + "\n")

# Hàm ghi log file
def log_file_event(log_data):
    """Ghi log event liên quan đến file."""
    # Đưa log data vào queue
    log_queue.put(log_data)

def log_event(service, event_type, message, session=None, additional_info={}, severity="NORMAL"):
    """Ghi log sự kiện."""
    log_entry = {
        "service": service,
        "event_type": event_type,
        "message": message,
        "severity": severity,
        "session": {
            "session_id": session.session_id if session else None,
            "client_ip": session.client_ip if session else None,
            "username": session.username if session else None,
            "start_time": session.start_time if session else None,
            "end_time": session.end_time if session else None,
            "commands": session.commands if session else None,
            "accessed_files": session.accessed_files if session else None,
        },
        **additional_info
    }
    log_queue.put(log_entry)

# Thread để xử lý log event
class LogProcessor(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.daemon = True
        self.splunk_handler = self._init_splunk_handler()  # Khởi tạo Splunk handler (nếu được cấu hình)
        self.start()

    def run(self):
        while True:
            log_entry = self.queue.get()
            self._process_log(log_entry)
            self.queue.task_done()

    def _process_log(self, log_entry):
        # Ghi log vào file
        self._log_to_file(log_entry)

        # Gửi log đến Splunk (nếu được cấu hình)
        if self.splunk_handler:
            try:
                # Chuyển log entry thành JSON
                log_json = json.dumps(log_entry)

                # Gửi log qua TCP
                self.splunk_handler.sendall(log_json.encode() + b"\n")

            except Exception as e:
                print(f"Error sending log to Splunk: {e}")

        # Gửi email cảnh báo (nếu được bật)
        severity = log_entry.get("severity", "NORMAL").upper()
        log_config = LOG_CONFIG.get(severity)
        if log_config and log_config.get("email_enabled", False):
            subject = f"Cảnh báo Honeypot: {log_entry['file_events'][0]['action']} - Severity: {severity}"
            log_message = json.dumps(log_entry, indent=4)
            _send_email_alert(subject, log_message)

    def _log_to_file(self, log_entry):
        with log_lock:
            with open(os.path.join(FILE_LOG_DIR, "honeypot_log.json"), "a") as f:
                f.write(json.dumps(log_entry) + "\n")

    def _init_splunk_handler(self):
        # Khởi tạo Splunk handler (nếu được cấu hình)
        if SPLUNK_HOST and SPLUNK_PORT:
            try:
                # Tạo socket TCP
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Kết nối đến Splunk server
                sock.connect((SPLUNK_HOST, SPLUNK_PORT))

                # Trả về socket
                return sock

            except Exception as e:
                print(f"Error initializing Splunk handler: {e}")
        return None

# Khởi tạo LogProcessor
log_processor = LogProcessor(log_queue)

def _send_email_alert(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME if SMTP_USERNAME else ADMIN_EMAIL
    msg["To"] = ADMIN_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            if SMTP_USERNAME and SMTP_PASSWORD:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME if SMTP_USERNAME else ADMIN_EMAIL, ADMIN_EMAIL, msg.as_string())
        logging.info(f"Email alert sent to {ADMIN_EMAIL}")
    except Exception as e:
        logging.error(f"Lỗi khi gửi email cảnh báo: {e}")

def attack_log(**kwargs):
    """Ghi lại hành vi của kẻ tấn công."""
    kwargs["severity"] = "WARNING"
    log_queue.put(kwargs)