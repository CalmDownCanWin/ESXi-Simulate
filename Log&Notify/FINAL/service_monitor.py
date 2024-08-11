import os
import time
import subprocess
import json
import threading
from queue import Queue
import socket



from config import SPLUNK_HOST, SPLUNK_PORT, SERVICES_TO_MONITOR, \
    FILE_LOG_DIR, MAX_QUEUE_SIZE

# Cấu hình logging
import logging
if not os.path.exists(FILE_LOG_DIR):
    os.makedirs(FILE_LOG_DIR)

logging.basicConfig(filename=os.path.join(FILE_LOG_DIR, "service_monitor.log"), level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def check_service_status(service_name):
    """Kiểm tra trạng thái của dịch vụ và trả về output đầy đủ."""
    try:
        output = subprocess.check_output(["service", service_name, "status"], stderr=subprocess.STDOUT)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode().strip()}"

def log_change(queue, service_name, old_state, new_state):
    """Ghi log thay đổi trạng thái dịch vụ."""
    log_entry = {
        "timestamp": time.time(),
        "event_type": "service_change",
        "service_name": service_name,
        "old_state": old_state,
        "new_state": new_state
    }
    queue.put(log_entry)
    logging.info(f"Service Change Detected: {log_entry}")

def log_worker(queue):
    """Đọc log từ queue và gửi đến Splunk, ghi vào file."""
    while True:
        log_entry = queue.get()

        # Ghi vào file
        log_file = os.path.join(FILE_LOG_DIR, "service_changes.log")
        with open(log_file, "a") as f:
            json.dump(log_entry, f)
            f.write("\n")

        # Gửi đến Splunk nếu cấu hình tồn tại
        if SPLUNK_HOST and SPLUNK_PORT:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.sendto(json.dumps(log_entry).encode(), (SPLUNK_HOST, SPLUNK_PORT))
            except Exception as e:
                logging.error(f"Lỗi khi gửi log đến Splunk: {e}")

        queue.task_done()


def monitor_services():
    """Giám sát thay đổi trạng thái dịch vụ."""
    service_states = {}
    log_queue = Queue(maxsize=MAX_QUEUE_SIZE)

    threading.Thread(target=log_worker, args=(log_queue,), daemon=True).start()

    while True:
        for service_name in SERVICES_TO_MONITOR:
            status = check_service_status(service_name)
            previous_state = service_states.get(service_name)
            if previous_state and status != previous_state:
                log_change(log_queue, service_name, previous_state, status)
            service_states[service_name] = status
        time.sleep(15)  # Giảm thời gian chờ


if __name__ == "__main__":
    monitor_services()