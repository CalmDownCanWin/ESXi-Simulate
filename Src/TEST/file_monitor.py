import os
import time
import hashlib
import stat
import math
import logging
import threading
from queue import Queue
from collections import defaultdict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileDeletedEvent, FileModifiedEvent, FileMovedEvent
from config import HONEYPOT_ROOT, LOG_ROOT, FILE_LOG_DIR, IGNORE_PATTERNS, RANSOMWARE_HASH_DB, ENABLE_RANSOMWARE_DETECTION, SENSITIVE_DIRS, ACCESS_THRESHOLD, ENTROPY_THRESHOLDS
from event_logger import log_file_event, log_queue
from utils import check_ransomware_hash, get_file_diff
from behavior_analyzer import BehaviorAnalyzer
import zlib  # For CRC32 checksum
import json

# Khởi tạo BehaviorAnalyzer
behavior_analyzer = BehaviorAnalyzer(SENSITIVE_DIRS)

for dir_path in [LOG_ROOT, FILE_LOG_DIR]:
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")
        except OSError as e:
            print(f"Error creating directory {dir_path}: {e}")

def calculate_file_checksum(filename, algorithm="crc32"):
    """Calculate file checksum."""
    checksum = 0  # Khởi tạo biến checksum
    with open(filename, "rb") as f:
        first_chunk = f.read(4096)
        if algorithm == "crc32":
            checksum = zlib.crc32(first_chunk)  # Gán giá trị checksum CRC32
        else:
            hash_obj = hashlib.md5()
            hash_obj.update(first_chunk)
            checksum = hash_obj.hexdigest()

        for chunk in iter(lambda: f.read(4096), b""):
            if algorithm == "md5":  # Chỉ update hash_obj nếu là md5
                hash_obj.update(chunk)
            else:
                checksum = zlib.crc32(chunk, checksum)  # Cập nhật checksum CRC32

        if algorithm == "md5":
            checksum = hash_obj.hexdigest()
        else:
            checksum = hex(checksum)[2:]  # Chuyển đổi checksum CRC32 sang hex

    return checksum

file_access_count = defaultdict(lambda: {"count": 0, "ip": None, "commands": []})

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, session=None):
        global file_access_count  # Khai báo global
        self.file_access_count = defaultdict(lambda: {"count": 0, "ip": None, "commands": []})
        self.file_info = {}
        self.file_checksums = {}  # Lưu checksum của file
        self.ignore_patterns = IGNORE_PATTERNS
        self.sensitive_dirs = SENSITIVE_DIRS
        self.access_threshold = ACCESS_THRESHOLD
        self.file_access_count = defaultdict(lambda: {"count": 0, "ip": None, "commands": []})
        self.file_event_queue = Queue()
        self.debounce_timers = defaultdict(threading.Timer)
        self.session = session  # Lưu trữ session
        self.session_events = defaultdict(list)  # Lưu trữ event theo session

        # Scan existing files on startup
        self.scan_existing_files(HONEYPOT_ROOT)
        print("[File Monitor] Scan completed. Starting to monitor file changes...")

        # Initialize the queue processing thread AFTER file scanning
        self.file_processor = threading.Thread(target=self.process_file_queue, daemon=True)
        self.file_processor.start()

    def on_any_event(self, event):
        if not event.is_directory and not any(pattern in event.src_path for pattern in self.ignore_patterns):
            self.handle_file_event(event)

    def handle_file_event(self, event):
        """General handler for file events."""
        try:
            # Debounce all events
            filepath = event.src_path
            if event.event_type == "moved":
                filepath = event.dest_path
            if filepath not in self.debounce_timers:
                timer = threading.Timer(0.5, self.file_event_queue.put, args=[event])
                self.debounce_timers[filepath] = timer
                timer.start()
            else:
                timer = self.debounce_timers[filepath]
                if timer.is_alive():
                    timer.cancel()
                timer = threading.Timer(0.5, self.file_event_queue.put, args=[event])
                self.debounce_timers[filepath] = timer
                timer.start()
        except Exception as e:
            logging.error(f"Error handling file event: {e}")

    def process_file_queue(self):
        """Process file events in the queue."""
        while True:
            event = self.file_event_queue.get()

            # Kiểm tra session
            if self.session:
                session_key = self.session.session_id
            else:
                session_key = "no_session"

            if event.event_type == "deleted":
                self.process_file_deletion(event.src_path, session_key)
            elif event.event_type in ["created", "modified", "moved"]:
                self.process_file_change(event, session_key)
            self.file_event_queue.task_done()

    def process_file_deletion(self, filepath, session_key):
        """Handle file deletion event."""
        if filepath in self.file_info:
            del self.file_info[filepath]
            del self.file_checksums[filepath]  # Xóa checksum khi file bị xóa

            # Tạo log event
            log_data = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": self.session.client_ip if self.session else None,
                "ssh_username": self.session.username if self.session else None,
                "ssh_commands": [cmd[1] for cmd in self.session.commands] if self.session else None,
                "file_events": [
                    {
                        "action": "deleted",
                        "filepath": filepath,
                        "hash": None,  # Không có hash khi file bị xóa
                        "ransomware_name": None,
                        "severity": "NORMAL"
                    }
                ]
            }

            # Thêm event vào danh sách event của session
            self.session_events[session_key].append(log_data["file_events"][0])

            # Ghi log vào file
            self.log_file_event(log_data)

            print(f"[File Monitor] File {filepath} has been deleted.")
        else:
            # Xử lý trường hợp file không tồn tại
            logging.warning(f"File not found during deletion: {filepath}")

    def process_file_change(self, event, session_key):
        """Handle file creation, modification, and movement events."""
        filepath = event.src_path
        if event.event_type == "moved":
            filepath = event.dest_path  # Get the new file path for move events

        if os.path.exists(filepath):
            try:
                # Kiểm tra checksum trước
                current_checksum = calculate_file_checksum(filepath)
                if filepath in self.file_checksums and current_checksum == self.file_checksums[filepath]:
                    return  # Checksum không thay đổi, bỏ qua xử lý

                self.file_checksums[filepath] = current_checksum

                # Kiểm tra ransomware (chỉ khi file được tạo)
                ransomware_name = None
                if ENABLE_RANSOMWARE_DETECTION and event.event_type == "created":
                    ransomware_name = self.check_ransomware(filepath)

                # Phân tích entropy và behavior (chỉ khi không phải moved event)
                if event.event_type != "moved":
                    self.handle_modified_event(filepath)

                # Lấy event_type từ event
                event_type = event.event_type

                self.analyze_file_behavior(filepath, event_type)

                # Tính toán SHA256 sau khi checksum thay đổi
                file_hash = self.calculate_file_hash(filepath)

                # Xác định severity
                severity = self.analyze_severity(filepath, event_type)

                # Tạo log event
                log_data = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "ip_address": self.session.client_ip if self.session else None,
                    "ssh_username": self.session.username if self.session else None,
                    "ssh_commands": [cmd[1] for cmd in self.session.commands] if self.session else None,
                    "file_events": [
                        {
                            "action": event_type,
                            "filepath": filepath,
                            "hash": file_hash,
                            "ransomware_name": ransomware_name if event_type == "created" and ransomware_name else None,
                            "severity": severity
                        }
                    ]
                }

                # Thêm event vào danh sách event của session
                self.session_events[session_key].append(log_data["file_events"][0])

                # Ghi log vào file
                self.log_file_event(log_data)

            except FileNotFoundError:
                logging.warning(f"File not found while monitoring: {filepath}")
                # Xóa file khỏi danh sách file_info và file_checksums
                if filepath in self.file_info:
                    del self.file_info[filepath]
                if filepath in self.file_checksums:
                    del self.file_checksums[filepath]

    def handle_modified_event(self, filepath):
        """Handle modified event with debounce."""
        if filepath not in self.debounce_timers:
            timer = threading.Timer(0.5, self.analyze_file_behavior, args=[filepath, "modified"])
            self.debounce_timers[filepath] = timer
            timer.start()
        else:
            timer = self.debounce_timers[filepath]
            if timer.is_alive():
                timer.cancel()
            timer = threading.Timer(0.5, self.analyze_file_behavior, args=[filepath, "modified"])
            self.debounce_timers[filepath] = timer
            timer.start()

    def analyze_file_behavior(self, filepath, event_type):
        """Analyze file entropy and behavior."""
        try:
            stat_info = os.stat(filepath)

            # Tính toán SHA256 sau khi checksum thay đổi
            file_hash = self.calculate_file_hash(filepath)

            current_info = {
                "hash": file_hash,
                "size": stat_info.st_size,
                "permissions": stat.filemode(stat_info.st_mode),
                "extension": os.path.splitext(filepath)[1],
                "mtime": stat_info.st_mtime,
                "entropy": self.calculate_entropy(filepath)
            }

            # Update file access count
            if self.session:
                self.file_access_count[filepath]["count"] += 1
                self.file_access_count[filepath]["ip"] = self.session.client_ip
                self.file_access_count[filepath]["commands"].extend(cmd[1] for cmd in self.session.commands)

            severity = "NORMAL"
            if filepath in self.file_info:
                old_info = self.file_info[filepath].copy()
                if old_info != current_info:
                    changes = get_file_diff(filepath, next((f for f, info in self.file_info.items() if info["hash"] == old_info["hash"]), None))

                    # Analyze severity
                    severity = self.analyze_severity(filepath, event_type, current_info, old_info, changes)

            self.file_info[filepath] = current_info

        except FileNotFoundError:
            logging.warning(f"File not found during analysis: {filepath}")

    def analyze_severity(self, filepath, event_type, current_info=None, old_info=None, changes=None):
        """Analyzes the severity of a file event."""
        severity = "NORMAL"

        # Phân loại file theo extension
        if current_info:
            extension = current_info["extension"].lower()
            entropy_threshold = ENTROPY_THRESHOLDS.get(extension, ENTROPY_THRESHOLDS["default"])

            # Check entropy for new files
            if event_type == "created":
                if current_info["entropy"] > entropy_threshold["suspicious"]:
                    severity = "WARNING"

        # Check if file is in a sensitive directory
        elif any(sensitive_dir in filepath for sensitive_dir in self.sensitive_dirs):
            severity = "WARNING"

        # Analyze changes
        if severity == "WARNING" or event_type == "modified":
            if current_info and old_info and "hash" in current_info and "hash" in old_info and current_info["hash"] != old_info["hash"]:
                # Content has changed
                severity = "DANGEROUS"

        # Check access count
        if self.file_access_count[filepath]["count"] > ACCESS_THRESHOLD:
            severity = "DANGEROUS"

        # Kết hợp phân tích hành vi attacker
        global behavior_analyzer
        is_suspicious, reason = behavior_analyzer.analyze_event(
            {"filepath": filepath, "action": event_type}
        )
        if is_suspicious:
            severity = "DANGEROUS"

        return severity

    def check_ransomware(self, filepath):
        """Check if a file matches known ransomware hashes."""
        file_hash = self.calculate_file_hash(filepath)
        is_ransomware, ransomware_name = check_ransomware_hash(file_hash, RANSOMWARE_HASH_DB)
        if is_ransomware:
            print(f"[Ransomware Detected] File: {filepath} - Ransomware: {ransomware_name}")
            return ransomware_name
        return None

    def calculate_file_hash(self, filename, algorithm="sha256", chunk_size=4096):
        """Calculate file hash."""
        try:
            hash_obj = hashlib.new(algorithm)
            with open(filename, "rb") as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except PermissionError:
            logging.warning(f"No permission to read file: {filename}")
            return None

    def calculate_entropy(self, filename):
        """Calculate file entropy."""
        with open(filename, 'rb') as f:
            data = f.read()
        if not data:
            return 0
        probabilities = [float(data.count(c)) / len(data) for c in dict.fromkeys(list(data))]
        entropy = - sum([p * math.log(p, 2) for p in probabilities])
        return entropy

    def scan_existing_files(self, path):
        """Scan existing files in the honeypot directory."""
        for root, _, files in os.walk(path):
            for file in files:
                filepath = os.path.join(root, file)
                if not any(pattern in filepath for pattern in self.ignore_patterns):
                    try:
                        stat_info = os.stat(filepath)
                        # Tính toán và lưu trữ checksum ban đầu, chỉ định algorithm là crc32
                        self.file_checksums[filepath] = calculate_file_checksum(filepath, algorithm="crc32")
                        self.file_info[filepath] = {
                            "hash": self.calculate_file_hash(filepath),
                            "size": stat_info.st_size,
                            "permissions": stat.filemode(stat_info.st_mode),
                            "extension": os.path.splitext(filepath)[1],
                            "mtime": stat_info.st_mtime,
                            "entropy": self.calculate_entropy(filepath)
                        }
                    except Exception as e:
                        logging.error(f"Error scanning file {filepath}: {e}")

    def log_file_event(self, log_data):
        """Logs a file event with appropriate severity."""
        with open("file_log.json", "a") as f:
            f.write(json.dumps(log_data) + "\n")

# Hàm ghi log định kỳ 
def log_session_events(event_handler, session_key):
    """Ghi log các event của session vào file."""
    if session_key in event_handler.session_events:
        # Tạo log entry
        log_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": event_handler.session.client_ip if event_handler.session else None,
            "ssh_username": event_handler.session.username if event_handler.session else None,
            "ssh_commands": [cmd[1] for cmd in event_handler.session.commands] if event_handler.session else None,
            "file_events": event_handler.session_events[session_key]
        }

        # Ghi log vào file
        event_handler.log_file_event(log_data)

        # Xóa event của session khỏi dictionary
        del event_handler.session_events[session_key]

def start_file_monitor(watch_path, session=None):
    """Start file monitoring."""
    event_handler = FileMonitorHandler(session=session)
    observer = Observer()
    observer.schedule(event_handler, path=watch_path, recursive=True)
    observer.start()

    # Timer để ghi log định kỳ (ví dụ: mỗi 5 giây)
    timer = threading.Timer(5.0, log_session_events, args=[event_handler, session.session_id if session else "no_session"])
    timer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        timer.cancel()  # Dừng timer khi kết thúc
        observer.join()

if __name__ == "__main__":
    start_file_monitor(HONEYPOT_ROOT)