import os
import time
import hashlib
import datetime
from log import log_filesystem_change
from concurrent.futures import ThreadPoolExecutor
import threading
import queue

# --- Cấu hình ---
ESXI_ROOT = "/home/testserver/Desktop/ESXI 7/"
MONITOR_INTERVAL = 1
FOLDER_LOG_FILE = "folder_changes.txt"
NUM_THREADS = 4
CHANGE_QUEUE = queue.Queue()  # Queue để lưu trữ thay đổi

# --- Hàm hỗ trợ ---

def calculate_file_hash(filename, algorithm="sha256", chunk_size=1024 * 1024):
    """Tính toán hash của file (mặc định SHA-256 cho 1MB đầu)."""
    hash_obj = hashlib.new(algorithm)
    with open(filename, 'rb') as file:
        chunk = file.read(chunk_size)
        if chunk:
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def get_file_info(filepath):
    """Lấy thông tin về file: tên, kích thước, hash, quyền."""
    return {
        "filename": os.path.basename(filepath),
        "size": os.path.getsize(filepath),
        "hash": calculate_file_hash(filepath),
        "permissions": oct(os.stat(filepath).st_mode)[-3:]
    }

def scan_filesystem(directory, print_output=False):
    """Quét toàn bộ hệ thống file và trả về thông tin của tất cả các file.
       Tham số `print_output`  kiểm soát việc in ra console.
    """
    if print_output:
        print(f"Đang quét hệ thống file...")

    file_info = {}
    for root, _, files in os.walk(directory):
        if print_output:
            print(f"- Thư mục: {root}")
        for file in files:
            filepath = os.path.join(root, file)
            file_info[filepath] = get_file_info(filepath)
            if print_output:
                print(f"  - File: {filepath}")
    return file_info

def detect_changes(previous_state, current_state):
    """Phát hiện thay đổi giữa hai trạng thái của hệ thống file."""
    changes = []
    for filepath, current_info in current_state.items():
        if filepath not in previous_state:
            changes.append({"action": "created", "file": current_info, "previous": {}})
        elif previous_state[filepath] != current_info:
            changes.append({"action": "modified", "file": current_info, "previous": previous_state[filepath]})

    for filepath in set(previous_state) - set(current_state):
        changes.append({"action": "deleted", "file": previous_state[filepath], "previous": {}})

    return changes


def log_folder_change(timestamp, folder_path, change_type, details=""):
    """Ghi log thay đổi thư mục vào file text."""
    log_entry = f"{timestamp} - {change_type}: {folder_path} - {details}"
    with open(FOLDER_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")
    print(log_entry)

def monitor_folders(directory, initial_state):
    """Giám sát thay đổi trong thư mục."""
    print(f"Bắt đầu giám sát thư mục: {directory}")
    previous_folders = initial_state

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        while True:
            time.sleep(MONITOR_INTERVAL)
            current_folders = set(os.listdir(directory))

            # Kiểm tra thư mục mới/xóa
            added_folders = current_folders - previous_folders
            deleted_folders = previous_folders - current_folders
            for folder in added_folders:
                CHANGE_QUEUE.put((datetime.datetime.now(), os.path.join(directory, folder), "Thư mục mới", ""))
            for folder in deleted_folders:
                CHANGE_QUEUE.put((datetime.datetime.now(), os.path.join(directory, folder), "Thư mục bị xóa", ""))

            # Kiểm tra thay đổi trong thư mục con
            for folder in current_folders.intersection(previous_folders):
                folder_path = os.path.join(directory, folder)
                if os.path.isdir(folder_path):
                    executor.submit(monitor_folder_content, folder_path)

            previous_folders = current_folders

def monitor_folder_content(folder_path):
    """Giám sát thay đổi nội dung của một thư mục."""
    print(f"Giám sát nội dung thư mục: {folder_path}")
    previous_files = scan_filesystem(folder_path)
    print(f"Quét file ban đầu trong thư mục {folder_path} hoàn tất.")

    while True:
        time.sleep(MONITOR_INTERVAL)
        current_files = scan_filesystem(folder_path)
        changes = detect_changes(previous_files, current_files)

        if changes:
            for change in changes:
                timestamp = datetime.datetime.now()
                filepath = os.path.join(folder_path, change['file']['filename'])
                if change['action'] == 'created':
                    details = f"Quyền: {change['file']['permissions']}, Kích thước: {change['file']['size']}, Hash: {change['file']['hash']}"
                elif change['action'] == 'deleted':
                    details = f"Quyền: {change['file']['permissions']}, Kích thước: {change['file']['size']}, Hash: {change['file']['hash']}"
                else:  # modified
                    details = (f"Quyền cũ: {change['previous']['permissions']}, Quyền mới: {change['file']['permissions']}, "
                               f"Kích thước cũ: {change['previous']['size']}, Kích thước mới: {change['file']['size']}, "
                               f"Hash cũ: {change['previous']['hash']}, Hash mới: {change['file']['hash']}")
                # Đưa thay đổi vào queue
                CHANGE_QUEUE.put((timestamp, filepath, change['action'], details))  
        previous_files = current_files

# Hàm ghi log từ queue
def log_changes_from_queue():
    """Đọc thay đổi từ queue và ghi log."""
    while True:
        timestamp, filepath, action, details = CHANGE_QUEUE.get()
        log_folder_change(timestamp.strftime("%Y-%m-%d %H:%M:%S"), filepath, action, details)

# --- Vòng lặp theo dõi ---

def monitor_filesystem():
    """Theo dõi thay đổi trong hệ thống file và ghi log."""
    initial_state = set(os.listdir(ESXI_ROOT))
    scan_filesystem(ESXI_ROOT, print_output=True)
    print("Quét file ban đầu hoàn tất.")

    # Khởi tạo thread ghi log từ queue
    log_thread = threading.Thread(target=log_changes_from_queue)
    log_thread.daemon = True  # Cho phép thread kết thúc khi main thread thoát
    log_thread.start()

    monitor_folders(ESXI_ROOT, initial_state)

if __name__ == "__main__":
    monitor_filesystem()