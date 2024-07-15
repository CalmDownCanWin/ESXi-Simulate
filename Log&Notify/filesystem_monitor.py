import os
import time
import hashlib
import datetime
from log import log_filesystem_change

# --- Cấu hình ---
ESXI_ROOT = "/home/testserver/Desktop/ESXI 7/"  # Thư mục gốc của hệ thống file ESXi giả mạo
MONITOR_INTERVAL = 0.1  # Khoảng thời gian kiểm tra thay đổi (giây)

# --- Hàm hỗ trợ ---
def calculate_file_hash(filename):
    """Tính toán hash SHA-256 của file."""
    hasher = hashlib.sha256()
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(4096)  # Đọc file theo từng khối
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

def get_file_info(filepath):
    """Lấy thông tin về file: tên, kích thước, hash."""
    return {
        "filename": os.path.basename(filepath),
        "size": os.path.getsize(filepath),
        "hash": calculate_file_hash(filepath)
    }

def scan_filesystem(directory):
    """Quét toàn bộ hệ thống file và trả về thông tin của tất cả các file."""
    file_info = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_info[filepath] = get_file_info(filepath)
    return file_info

def detect_changes(previous_state, current_state):
    """Phát hiện thay đổi giữa hai trạng thái của hệ thống file."""
    changes = []
    for filepath, current_info in current_state.items():
        if filepath not in previous_state:
            changes.append({"action": "created", "file": current_info})
        elif previous_state[filepath] != current_info:
            changes.append({"action": "modified", "file": current_info})

    deleted_files = set(previous_state.keys()) - set(current_state.keys())
    for filepath in deleted_files:
        changes.append({"action": "deleted", "file": previous_state[filepath]})

    return changes

# --- Vòng lặp theo dõi ---

def monitor_filesystem():
    """Theo dõi thay đổi trong hệ thống file và ghi log."""
    previous_state = scan_filesystem(ESXI_ROOT)
    while True:
        time.sleep(MONITOR_INTERVAL)
        current_state = scan_filesystem(ESXI_ROOT)
        changes = detect_changes(previous_state, current_state)

        if changes:
            print("[!] Phát hiện thay đổi:")
            for change in changes:
                print(f"  - {change['action']}: {change['file']['filename']}")
                log_filesystem_change(change['action'], change['file'])  # Ghi log

        previous_state = current_state

if __name__ == "__main__":
    monitor_filesystem()