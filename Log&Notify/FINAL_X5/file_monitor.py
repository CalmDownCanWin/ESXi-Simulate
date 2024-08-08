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
from config import HONEYPOT_ROOT, IGNORE_PATTERNS, ENABLE_RANSOMWARE_DETECTION, SENSITIVE_DIRS, ACCESS_THRESHOLD, ENTROPY_THRESHOLDS
from event_logger import log_event, attack_log
from utils import get_file_diff, calculate_file_checksum, is_potential_ransomware, is_file_encrypted
from behavior_analyzer import BehaviorAnalyzer

# Khởi tạo BehaviorAnalyzer
behavior_analyzer = BehaviorAnalyzer(SENSITIVE_DIRS)

class FileMonitorHandler(FileSystemEventHandler):
    """
    Handles file system events and analyzes suspicious activities.
    """
    def __init__(self):
        """
        Initializes the FileMonitorHandler.
        """
        self.file_info = {}  # Stores information about files (hash, size, permissions, etc.)
        self.file_checksums = {}  # Stores checksums of files for quick comparison
        self.ignore_patterns = IGNORE_PATTERNS  # Patterns to ignore during monitoring
        self.sensitive_dirs = SENSITIVE_DIRS  # List of sensitive directories to monitor
        self.access_threshold = ACCESS_THRESHOLD  # Threshold for frequent file access
        self.file_access_count = defaultdict(lambda: {"count": 0, "ip": None, "commands": []})  # Tracks file access count and associated session information
        self.file_event_queue = Queue()  # Queue to process file events in a separate thread
        self.debounce_timers = defaultdict(threading.Timer)  # Debounce timers to prevent excessive event processing
        self.session = None  # Current SSH/service session
        self.last_command = None  # Last command executed by the attacker

        # Initialize the queue processing thread AFTER file scanning
        self.file_processor = threading.Thread(target=self.process_file_queue, daemon=True)
        self.file_processor.start()

    def on_any_event(self, event):
        """
        Handles any file system event.
        """
        if not event.is_directory and not any(pattern in event.src_path for pattern in self.ignore_patterns):
            self.handle_file_event(event)

    def handle_file_event(self, event):
        """
        Handles file events with debouncing.
        """
        try:
            filepath = event.src_path
            if event.event_type == "moved":
                filepath = event.dest_path  # Get the new file path for move events

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
        """
        Processes file events from the queue.
        """
        while True:
            event = self.file_event_queue.get()
            if event.event_type == "deleted":
                self.process_file_deletion(event.src_path)
            elif event.event_type in ["created", "modified", "moved"]:
                self.process_file_change(event)
            self.file_event_queue.task_done()

    def process_file_deletion(self, filepath):
        """
        Handles file deletion events.
        """
        if filepath in self.file_info:
            del self.file_info[filepath]
            del self.file_checksums[filepath]  # Delete checksum when file is deleted
            self.log_file_event(filepath, "deleted", severity="NORMAL")
            print(f"[File Monitor] File {filepath} has been deleted.")

    def process_file_change(self, event):
        """
        Handles file creation, modification, and movement events.
        """
        filepath = event.src_path
        if event.event_type == "moved":
            filepath = event.dest_path  # Get the new file path for move events

        if os.path.exists(filepath):
            try:
                # Check checksum first
                current_checksum = calculate_file_checksum(filepath)
                if filepath in self.file_checksums and current_checksum == self.file_checksums[filepath]:
                    return  # Checksum didn't change, skip processing

                self.file_checksums[filepath] = current_checksum
                # Check for ransomware (only if file is created)
                if ENABLE_RANSOMWARE_DETECTION and event.event_type == "created":
                    self.check_ransomware_behavior(filepath)

                # Analyze entropy and behavior (only if not a moved event)
                if event.event_type != "moved":
                    self.handle_modified_event(filepath)
                self.analyze_file_behavior(filepath, event.event_type)
            except FileNotFoundError:
                logging.warning(f"File not found while monitoring: {filepath}")

    def handle_modified_event(self, filepath):
        """
        Handles modified event with debounce.
        """
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
        """
        Analyzes file entropy and behavior.
        """
        try:
            stat_info = os.stat(filepath)
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

            # Check if the file was created by a command like wget or a similar download command
            if event_type == "created" and (self.last_command == "wget" or self.last_command.startswith("curl")):
                severity = "WARNING"

            # If the file was created, check for ransomware behavior
            if event_type == "created" and ENABLE_RANSOMWARE_DETECTION:
                severity = self.check_ransomware_behavior(filepath, severity)

            # If the file was created, log the event
            if event_type == "created" and os.path.basename(filepath) != ".mtoolsrc":  
                self.log_file_event(filepath, "created", info=current_info, severity=severity)
                print(f"[File Monitor] File {filepath} has been created.")

            # If the file was modified, log the event
            if filepath in self.file_info:
                old_info = self.file_info[filepath].copy()
                if old_info != current_info:
                    changes = get_file_diff(filepath, next((f for f, info in self.file_info.items() if info["hash"] == old_info["hash"]), None))

                    # Analyze severity
                    severity = self.analyze_severity(filepath, event_type, current_info, old_info, changes)
                    self.log_file_event(filepath, "modified", changes, current_info["entropy"], severity)

                    print(f"[File Monitor] File {filepath} has been modified:")
                    for change in changes:
                        print(f"  - {change}")

            # Update file information
            self.file_info[filepath] = current_info

        except FileNotFoundError:
            logging.warning(f"File not found during analysis: {filepath}")

    def check_ransomware_behavior(self, filepath, severity):
        """
        Checks for ransomware behavior after file creation.
        """
        if ENABLE_RANSOMWARE_DETECTION:
            # Check if the file is a potential ransomware executable (e.g., based on extension or entropy)
            if self.is_potential_ransomware(filepath):
                # Analyze sensitive directories for encryption
                for sensitive_dir in self.sensitive_dirs:
                    for root, _, files in os.walk(sensitive_dir):
                        for file in files:
                            full_path = os.path.join(root, file)
                            if self.is_file_encrypted(full_path):
                                severity = "DANGEROUS"  # Set severity to dangerous if any file in sensitive directory is encrypted
                                attack_log(
                                    service="File Monitor",
                                    event_type="ransomware_suspicion",
                                    message=f"Ransomware suspicion: File {filepath} created, sensitive directory {sensitive_dir} has encrypted files",
                                    session=self.session,
                                    additional_info={"filepath": full_path},
                                    severity="DANGEROUS"
                                )
                                break  # Stop checking other files in the sensitive directory
                        if severity == "DANGEROUS":
                            break  # Stop checking other sensitive directories
                # If no file in sensitive directory is encrypted, keep severity as WARNING 
                if severity != "DANGEROUS":
                    severity = "WARNING"
        return severity

    def analyze_severity(self, filepath, event_type, current_info, old_info, changes):
        """
        Analyzes the severity of a file event.
        """
        severity = "NORMAL"

        # Classify file by extension
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
            if "hash" in current_info and "hash" in old_info and current_info["hash"] != old_info["hash"]:
                # Content has changed
                severity = "DANGEROUS" 

        # Check access count
        if self.file_access_count[filepath]["count"] > ACCESS_THRESHOLD:
            severity = "DANGEROUS"

        # Combine analysis with attacker behavior
        global behavior_analyzer
        is_suspicious, reason = behavior_analyzer.analyze_event(
            {"filepath": filepath, "action": event_type}
        )
        if is_suspicious:
            severity = "DANGEROUS"

        return severity

def start_file_monitor(watch_path):
    """
    Starts file monitoring.
    """
    event_handler = FileMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=watch_path, recursive=True)
    print("File Monitor started!!")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    start_file_monitor(HONEYPOT_ROOT)