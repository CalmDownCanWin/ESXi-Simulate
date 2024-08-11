import os
import time
import hashlib
import json
import threading
from queue import Queue
import socket
import logging
import stat
import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config import SPLUNK_HOST, SPLUNK_PORT, ESXI_ROOT, FILE_LOG_DIR, MAX_QUEUE_SIZE, IGNORE_PATTERNS
from utils import get_file_diff

# Cấu hình logging
if not os.path.exists(FILE_LOG_DIR):
    os.makedirs(FILE_LOG_DIR)
logging.basicConfig(filename=os.path.join(FILE_LOG_DIR, "file_monitor.log"), level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class Handler(FileSystemEventHandler):
    def __init__(self, log_queue):
        self.log_queue = log_queue
        self.file_info = {}
        self.ignore_patterns = IGNORE_PATTERNS

    def log_change(self, event, action, additional_info={}):
        if any(pattern in event.src_path for pattern in self.ignore_patterns):
            return

        log_entry = {
            "timestamp": time.time(),
            "event_type": "file_change",
            "action": action,
            "filepath": event.src_path,
            **additional_info
        }
        self.log_queue.put(log_entry)
        logging.info(f"File Change Detected: {log_entry}")
        print(f"File Change Detected: {log_entry}")

    def on_any_event(self, event):
        if not event.is_directory:
            try:
                time.sleep(0.1)  # Đảm bảo file đã tồn tại
                if os.path.exists(event.src_path):
                    if event.event_type == 'created':
                        self.log_change(event, "created")
                        self.track_file(event.src_path)
                    elif event.event_type == 'modified' and event.src_path in self.file_info:
                        if self.has_file_changed(event.src_path):
                            diff = get_file_diff(event.src_path, self.file_info[event.src_path].get("hash", ""))
                            self.log_change(event, "modified", {"diff": diff, "changes": self.get_changes(event.src_path)})
                            self.track_file(event.src_path)
                    elif event.event_type == 'deleted' and event.src_path in self.file_info:
                        self.log_change(event, "deleted")
                        del self.file_info[event.src_path]
            except Exception as e:
                logging.error(f"Lỗi khi xử lý sự kiện file: {e}")

    def track_file(self, filepath):
        stat_info = os.stat(filepath)
        self.file_info[filepath] = {
            "hash": self.calculate_file_hash(filepath),
            "size": stat_info.st_size,
            "permissions": stat.filemode(stat_info.st_mode),
            "extension": os.path.splitext(filepath)[1],
            "mtime": stat_info.st_mtime
        }

    def has_file_changed(self, filepath):
        try:
            stat_info = os.stat(filepath)
            current_info = {
                "hash": self.calculate_file_hash(filepath),
                "size": stat_info.st_size,
                "permissions": stat.filemode(stat_info.st_mode),
                "mtime": stat_info.st_mtime
            }
            old_info = self.file_info.get(filepath)
            if old_info is None:
                return True
            return current_info != old_info
        except FileNotFoundError:
            return False

    def get_changes(self, filepath):
        changes = []
        old_info = self.file_info.get(filepath)
        current_info = {
            "hash": self.calculate_file_hash(filepath),
            "size": os.path.getsize(filepath),
            "permissions": stat.filemode(os.stat(filepath).st_mode),
            "extension": os.path.splitext(filepath)[1]
        }
        for key in current_info:
            if current_info[key] != old_info.get(key):
                changes.append(f"{key} changed from {old_info[key]} to {current_info[key]}")
        return changes

    def calculate_file_hash(self, filename, algorithm="sha256", chunk_size=4096):
        hash_obj = hashlib.new(algorithm)
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()

def log_worker(queue):
    while True:
        log_entry = queue.get()

        # Ghi vào file
        log_file = os.path.join(FILE_LOG_DIR, "file_changes.log")
        with open(log_file, "a") as f:
            json.dump(log_entry, f)
            f.write("\n")

        # Gửi đến Splunk nếu cấu hình tồn tại
        if SPLUNK_HOST and SPLUNK_PORT:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((SPLUNK_HOST, SPLUNK_PORT))
                    sock.sendall(json.dumps(log_entry).encode() + b'\n')
            except Exception as e:
                logging.error(f"Lỗi khi gửi log đến Splunk: {e}")
                time.sleep(5)  # Thử gửi lại sau 5 giây
                log_worker(Queue(maxsize=1).put(log_entry))

        queue.task_done()

def monitor_files():
    log_queue = Queue(maxsize=MAX_QUEUE_SIZE)
    event_handler = Handler(log_queue)
    observer = Observer()
    observer.schedule(event_handler, path=ESXI_ROOT, recursive=True)

    # Duyệt qua các file hiện có để bắt đầu theo dõi
    for root, _, files in os.walk(ESXI_ROOT):
        for file in files:
            filepath = os.path.join(root, file)
            if not any(pattern in filepath for pattern in IGNORE_PATTERNS):
                event_handler.track_file(filepath)

    observer.start()
    threading.Thread(target=log_worker, args=(log_queue,), daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_files()
