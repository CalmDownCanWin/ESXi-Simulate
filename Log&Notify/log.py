import datetime
import os
import sqlite3
from db import DB_FILE

# --- Hàm hỗ trợ ---

def _log_to_file(log_entry, log_file):
    """Hàm chung để ghi log vào file."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

def _log_to_database(sql, values):
    """Hàm chung để ghi log vào database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()

# --- Hàm ghi log ---

def log_access(client_ip, method, path, query_params, log_dir="http_logs"):
    """Ghi log truy cập HTTP vào file và database."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {client_ip} - {method} {path} - {query_params}"
    log_file = os.path.join(log_dir, path.lstrip("/").replace("/", "_") + ".log")

    _log_to_file(log_entry, log_file)
    _log_to_database(
        """INSERT INTO http_logs (timestamp, client_ip, method, path, query_params) 
           VALUES (?, ?, ?, ?, ?)""",
        (timestamp, client_ip, method, path, str(query_params))
    )

def log_ssh_command(client_ip, command, log_dir="ssh_logs"):
    """Ghi log command SSH vào file và database."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {client_ip} - {command}"
    log_file = os.path.join(log_dir, "ssh_commands.log")

    _log_to_file(log_entry, log_file)
    _log_to_database(
        "INSERT INTO ssh_logs (timestamp, client_ip, command) VALUES (?, ?, ?)",
        (timestamp, client_ip, command)
    )

def log_telnet_command(client_ip, command, log_dir="telnet_logs"):
    """Ghi log command Telnet vào file và database."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {client_ip} - {command}"
    log_file = os.path.join(log_dir, "telnet_commands.log")

    _log_to_file(log_entry, log_file)
    _log_to_database(
        "INSERT INTO telnet_logs (timestamp, client_ip, command) VALUES (?, ?, ?)",
        (timestamp, client_ip, command)
    )

def log_dcui_interaction(client_ip, username, password, command, log_dir="dcui_logs"):
    """Ghi log tương tác DCUI vào file và database."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {client_ip} - Username: {username}, Password: {password}, Command: {command}"
    log_file = os.path.join(log_dir, "dcui_interactions.log")

    _log_to_file(log_entry, log_file)
    _log_to_database(
        "INSERT INTO dcui_logs (timestamp, client_ip, username, password, command) VALUES (?, ?, ?, ?, ?)",
        (timestamp, client_ip, username, password, command)
    )

def log_syslog_message(client_ip, message, log_dir="syslog_logs"):
    """Ghi log message syslog vào file và database."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {client_ip} - {message}"
    log_file = os.path.join(log_dir, "syslog_messages.log")

    _log_to_file(log_entry, log_file)
    _log_to_database(
        "INSERT INTO syslog_logs (timestamp, client_ip, message) VALUES (?, ?, ?)",
        (timestamp, client_ip, message)
    )

def log_vmotion_connection(client_ip, log_dir="vmotion_logs"):
    """Ghi log kết nối vMotion vào file và database."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {client_ip} - Connection attempt"
    log_file = os.path.join(log_dir, "vmotion_connections.log")

    _log_to_file(log_entry, log_file)
    _log_to_database(
        "INSERT INTO vmotion_logs (timestamp, client_ip) VALUES (?, ?)",
        (timestamp, client_ip)
    )

def log_iscsi_connection(client_ip, log_dir="iscsi_logs"):
    """Ghi log kết nối iSCSI vào file và database."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {client_ip} - Connection attempt"
    log_file = os.path.join(log_dir, "iscsi_connections.log")

    _log_to_file(log_entry, log_file)
    _log_to_database(
        "INSERT INTO iscsi_logs (timestamp, client_ip) VALUES (?, ?)",
        (timestamp, client_ip)
    )

def log_esxcli_command(client_ip, command, log_dir="esxcli_logs"):
    """Ghi log command esxcli vào file và database."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {client_ip} - {command}"

    _log_to_file(log_entry, os.path.join(log_dir, "esxcli_commands.log"))
    _log_to_database(
        "INSERT INTO esxcli_logs (timestamp, client_ip, command) VALUES (?, ?, ?)",
        (timestamp, client_ip, command)
    )

def log_vimcmd_command(client_ip, command, log_dir="vimcmd_logs"):
    """Ghi log command vim-cmd vào file và database."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {client_ip} - {command}"

    _log_to_file(log_entry, os.path.join(log_dir, "vimcmd_commands.log"))
    _log_to_database(
        "INSERT INTO vimcmd_logs (timestamp, client_ip, command) VALUES (?, ?, ?)",
        (timestamp, client_ip, command)
    )

def log_vmdumper_command(client_ip, command, log_dir="vmdumper_logs"):
    """Ghi log command vmdumper vào file và database."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {client_ip} - {command}"

    _log_to_file(log_entry, os.path.join(log_dir, "vmdumper_commands.log"))
    _log_to_database(
        "INSERT INTO vmdumper_logs (timestamp, client_ip, command) VALUES (?, ?, ?)",
        (timestamp, client_ip, command)
    )

def log_filesystem_change(action, file_info, log_dir="filesystem_changes"):
    """Ghi log thay đổi trong hệ thống file vào file và database."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = file_info['filename']
    size = file_info['size']
    hash = file_info['hash']
    permissions = file_info['permissions']

    # Lấy thông tin trước đó (nếu có)
    previous_permissions = file_info.get('previous', {}).get('permissions', '')
    previous_size = file_info.get('previous', {}).get('size', -1)
    previous_hash = file_info.get('previous', {}).get('hash', '')

    log_entry = f"{timestamp} - {action}: {filename} (size: {size}, hash: {hash}, permissions: {permissions})"

    if action == "modified":
        log_entry += (f" - Previous (size: {previous_size}, hash: {previous_hash}, permissions: {previous_permissions})")

    _log_to_file(log_entry, os.path.join(log_dir, "filesystem_changes.log"))
    _log_to_database(
        """INSERT INTO filesystem_changes (timestamp, action, filename, size, hash, permissions, 
                                       previous_permissions, previous_size, previous_hash) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (timestamp, action, filename, size, hash, permissions, previous_permissions, previous_size, previous_hash)
    )