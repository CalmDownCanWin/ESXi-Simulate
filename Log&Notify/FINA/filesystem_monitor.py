import os
import time
import hashlib
from configure import ESXI_ROOT, MONITOR_INTERVAL
from LOG_TO_SPLUNK import log_attack  # Import hàm log_attack

def calculate_file_hash(filename, algorithm="sha256", chunk_size=1024 * 1024):
    """Tính toán hash của file."""
    hash_obj = hashlib.new(algorithm)
    with open(filename, 'rb') as file:
        for chunk in iter(lambda: file.read(chunk_size), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def get_file_info(filepath):
    """Lấy thông tin về file."""
    return {
        "filename": os.path.basename(filepath),
        "extension": os.path.splitext(filepath)[1],
        "size": os.path.getsize(filepath),
        "hash": calculate_file_hash(filepath),
        "permissions": oct(os.stat(filepath).st_mode)[-3:],
        "type": "file"
    }

def scan_filesystem(directory):
    """Quét toàn bộ hệ thống file."""
    filesystem_state = {}
    for root, dirs, files in os.walk(directory):
        filesystem_state[root] = {"type": "directory", "contents": {}}
        for file in files:
            filepath = os.path.join(root, file)
            filesystem_state[root]["contents"][filepath] = get_file_info(filepath)      
    return filesystem_state

def detect_changes(previous_state, current_state):
    """Phát hiện thay đổi trong hệ thống file và ghi log."""
    changes = []
    for path, current_info in current_state.items():
        if path not in previous_state:
            changes.append({"action": "created", "path": path, "details": current_info})
            log_attack(event_type="filesystem_change", action="created", path=path, details=current_info)
        elif previous_state.get(path, {}).get("type") == current_info.get("type"):
            if current_info["type"] == "directory":
                changes.extend(detect_changes(previous_state[path]["contents"], current_info["contents"]))
            elif previous_state[path] != current_info:
                changes.append({"action": "modified", "path": path, "details": current_info})
                log_attack(event_type="filesystem_change", action="modified", path=path, details=current_info)
        else:
            changes.append({"action": "type_changed", "path": path, "details": current_info})
            log_attack(event_type="filesystem_change", action="type_changed", path=path, details=current_info)

    for path in set(previous_state.keys()) - set(current_state.keys()):
        changes.append({"action": "deleted", "path": path, "details": previous_state[path]})
        log_attack(event_type="filesystem_change", action="deleted", path=path, details=previous_state[path])

    return changes

def monitor_filesystem():
    """Theo dõi thay đổi trong hệ thống file."""
    previous_state = scan_filesystem(ESXI_ROOT)
    print("Bắt đầu theo dõi thay đổi...")
    while True:
        time.sleep(MONITOR_INTERVAL)
        current_state = scan_filesystem(ESXI_ROOT)
        changes = detect_changes(previous_state, current_state)
        # Không cần print change ở đây nữa vì đã ghi log trong detect_changes
        previous_state = current_state