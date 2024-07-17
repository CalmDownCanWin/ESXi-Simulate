import datetime
import os
import sqlite3

# Đường dẫn đến file database (giả sử db.py nằm cùng thư mục)
from db import DB_FILE

# --- Hàm hỗ trợ ---

def _log_to_file(log_entry, log_file):
    """Hàm chung để ghi log vào file."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

def _log_to_database(table_name, data):
    """Hàm chung để ghi log vào database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(data.values()))
        conn.commit()

# --- Hàm ghi log ---

def log_filesystem_change(action, file_info, log_dir="filesystem_changes"):
    """Ghi log thay đổi trong hệ thống file vào file và database."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = file_info['filename']
    size = file_info['size']
    hash = file_info['hash']
    permissions = file_info.get('permissions', '')

    previous_permissions = file_info.get('previous', {}).get('permissions', '')
    previous_size = file_info.get('previous', {}).get('size', -1)
    previous_hash = file_info.get('previous', {}).get('hash', '')

    log_entry = f"{timestamp} - {action}: {filename} (size: {size}, hash: {hash}, permissions: {permissions})"
    if action == "modified":
        log_entry += (f" - Previous (size: {previous_size}, hash: {previous_hash}, permissions: {previous_permissions})")

    _log_to_file(log_entry, os.path.join(log_dir, "filesystem_changes.log"))

    # Ghi vào database
    data = {
        'timestamp': timestamp,
        'action': action,
        'filename': filename,
        'size': size,
        'hash': hash,
        'permissions': permissions,
        'previous_permissions': previous_permissions,
        'previous_size': previous_size,
        'previous_hash': previous_hash
    }
    _log_to_database("filesystem_changes", data)
