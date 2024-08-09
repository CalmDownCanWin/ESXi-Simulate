import time
import math
from collections import deque

class BehaviorAnalyzer:
    """
    Analyzes file system events for suspicious activity.

    Attributes:
        sensitive_dirs (list): A list of sensitive directories to monitor.
        activity_threshold (int): The number of recent events to consider for analysis.
        entropy_threshold (float): The threshold for significant entropy change to trigger an alert.
        recent_activities (deque): A queue storing recent file system events.
        file_access_count (dict): A dictionary to track file access count.
        file_access_time (dict): A dictionary to track last access time.
    """
    def __init__(self, sensitive_dirs, activity_threshold=10, entropy_threshold=0.5):
        self.sensitive_dirs = sensitive_dirs
        self.activity_threshold = activity_threshold
        self.entropy_threshold = entropy_threshold
        self.recent_activities = deque(maxlen=activity_threshold)
        self.file_access_count = {}
        self.file_access_time = {}

    def analyze_event(self, event):
        """
        Analyzes a file event and returns the result.

        Args:
            event (dict): A dictionary containing information about the file event.

        Returns:
            tuple: A tuple containing a boolean indicating whether the event is suspicious and a string describing the reason.
        """
        self.recent_activities.append(event)
        if len(self.recent_activities) >= self.activity_threshold:
            is_suspicious, reason = self.check_suspicious_activity()
            if is_suspicious:
                return True, reason
        return False, None

    def check_suspicious_activity(self):
        """
        Checks for suspicious activity in the recent_activities queue.

        Returns:
            tuple: A tuple containing a boolean indicating whether any suspicious activity was detected and a string describing the reason.
        """
        modified_count = 0
        deleted_count = 0
        sensitive_access_count = 0
        entropy_change_count = 0

        for event in self.recent_activities:
            filepath = event["filepath"]
            if event["action"] == "modify":
                modified_count += 1
                # Check for significant entropy change
                if "old_hash" in event and "new_hash" in event and event["old_hash"] != event["new_hash"]:
                    entropy_change_count += 1
                    # Check if file has been accessed frequently
                    if filepath in self.file_access_count and self.file_access_count[filepath] > 5:
                        return True, f"Significant entropy change and frequent access to file: {filepath}"
            elif event["action"] == "deleted":
                deleted_count += 1
            # Check for access to sensitive directories
            if any(sensitive_dir in event["filepath"] for sensitive_dir in self.sensitive_dirs):
                sensitive_access_count += 1
                # Check if file has been accessed frequently
                if filepath in self.file_access_count and self.file_access_count[filepath] > 5:
                    return True, f"Frequent access to sensitive directory: {filepath}"

        # Check for suspicious conditions
        if modified_count >= self.activity_threshold / 2:
            return True, f"Large number of file modifications: {modified_count}"
        if deleted_count >= self.activity_threshold / 2:
            return True, f"Large number of file deletions: {deleted_count}"
        if sensitive_access_count >= self.activity_threshold / 2:
            return True, f"Frequent access to sensitive directories: {sensitive_access_count}"
        if entropy_change_count >= self.activity_threshold / 2:
            return True, f"Large number of significant entropy changes: {entropy_change_count}"

        return False, None

    def track_file_access(self, filepath, timestamp):
        """
        Tracks file access.

        Args:
            filepath (str): Path to the file.
            timestamp (str): Timestamp of the access.
        """
        if filepath in self.file_access_count:
            self.file_access_count[filepath] += 1
            self.file_access_time[filepath] = timestamp
        else:
            self.file_access_count[filepath] = 1
            self.file_access_time[filepath] = timestamp