import os
import threading
import time
from queue import Queue
import json 
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Console
from rich.text import Text
from rich.align import Align

from config import HONEYPOT_ROOT, LOG_CONFIG, FILE_LOG_DIR
from ssh2 import run_ssh_server, sessions
from file_monitor import start_file_monitor, FileMonitorHandler
from event_logger import log_queue, log_event

console = Console()

# Biến toàn cục để lưu trữ dữ liệu
session_data = []
file_activity_data = []
service_activity_data = []
ransomware_data = []

# Khởi tạo bảng Session Monitor
session_table = Table(title="Session Monitor")
session_table.add_column("Session ID", style="cyan", width=12)
session_table.add_column("IP Address", style="magenta", width=15)
session_table.add_column("Username", style="yellow", width=10)
session_table.add_column("Start Time", style="green", width=18)
session_table.add_column("End Time", style="green", width=18)
session_table.add_column("Commands", style="cyan", width=20)
session_table.add_column("File Activity Summary", style="magenta", width=25)
session_table.add_column("Highest Severity", style="yellow", width=15)

# Khởi tạo bảng File Activity Monitor
file_activity_table = Table(title="File Activity Monitor")
file_activity_table.add_column("Timestamp", style="cyan", width=18)
file_activity_table.add_column("Session ID", style="magenta", width=12)
file_activity_table.add_column("Action", style="yellow", width=10)
file_activity_table.add_column("Filepath", style="green", width=30)
file_activity_table.add_column("Hash", style="cyan", width=20)
file_activity_table.add_column("Ransomware Name", style="magenta", width=20)
file_activity_table.add_column("Severity", style="yellow", width=10)

# Khởi tạo bảng Service Activity Monitor
service_activity_table = Table(title="Service Activity Monitor")
service_activity_table.add_column("Timestamp", style="cyan", width=18)
service_activity_table.add_column("Service", style="magenta", width=10)
service_activity_table.add_column("IP Address", style="yellow", width=15)
service_activity_table.add_column("Action", style="green", width=20)
service_activity_table.add_column("Details", style="cyan", width=30)
service_activity_table.add_column("Severity", style="yellow", width=10)
service_activity_table.add_column("Fail Count", style="magenta", width=12)

# Khởi tạo bảng Ransomware Detected
ransomware_table = Table(title="Ransomware Detected")
ransomware_table.add_column("Timestamp", style="cyan", width=18)
ransomware_table.add_column("Filepath", style="magenta", width=30)
ransomware_table.add_column("Ransomware Name", style="yellow", width=20)
ransomware_table.add_column("Session ID", style="green", width=12)

# Hàm cập nhật bảng Session Monitor
def update_session_table():
    global session_data, session_table
    session_table.clear_rows()
    for session in session_data:
        commands_str = ", ".join(session["commands"][-5:]) if session["commands"] else "N/A"
        file_activity = session.get("file_activity", {"highest_severity": "NORMAL"})
        highest_severity = file_activity.get("highest_severity", "NORMAL")
        session_table.add_row(
            session["session_id"],
            session["client_ip"],
            session["username"],
            session["start_time"],
            session["end_time"],
            commands_str,
            f"Accessed: {file_activity.get('accessed_count', 0)}, Modified: {file_activity.get('modified_count', 0)}, Deleted: {file_activity.get('deleted_count', 0)}",
            highest_severity
        )

# Hàm cập nhật bảng File Activity Monitor
def update_file_activity_table():
    global file_activity_data, file_activity_table
    file_activity_table.clear_rows()
    for activity in file_activity_data:
        file_activity_table.add_row(
            activity["timestamp"],
            activity["session_id"],
            activity["action"],
            activity["filepath"],
            activity["hash"],
            activity.get("ransomware_name", "N/A"),
            activity["severity"]
        )

# Hàm cập nhật bảng Service Activity Monitor
def update_service_activity_table():
    global service_activity_data, service_activity_table
    service_activity_table.clear_rows()
    for activity in service_activity_data:
        service_activity_table.add_row(
            activity["timestamp"],
            activity["service"],
            activity["client_ip"],
            activity["action"],
            activity.get("details", "N/A"),
            activity["severity"],
            str(activity.get("fail_count", 0))
        )

# Hàm cập nhật bảng Ransomware Detected
def update_ransomware_table():
    global ransomware_data, ransomware_table
    ransomware_table.clear_rows()
    for activity in ransomware_data:
        ransomware_table.add_row(
            activity["timestamp"],
            activity["filepath"],
            activity["ransomware_name"],
            activity.get("session_id", "N/A")
        )

# Hàm xử lý log event
def process_log_event(log_entry):
    global session_data, file_activity_data, service_activity_data, ransomware_data
    event_type = log_entry["event_type"]
    severity = log_entry["severity"]
    if event_type == "session_started":
        session_data.append(log_entry["session"])
        update_session_table()
    elif event_type == "session_closed":
        for i, session in enumerate(session_data):
            if session["session_id"] == log_entry["session"]["session_id"]:
                session_data[i] = log_entry["session"]
                update_session_table()
                break
    elif event_type == "command_executed":
        for session in session_data:
            if session["session_id"] == log_entry["session"]["session_id"]:
                session["commands"].append(log_entry["additional_info"]["command"])
                update_session_table()
                break
    elif event_type == "file_event":
        if event_type not in file_activity_data:
            file_activity_data.append(log_entry)
        update_file_activity_table()
        # Cập nhật bảng Session Monitor
        for session in session_data:
            if session["session_id"] == log_entry["session"]["session_id"]:
                if "file_activity" not in session:
                    session["file_activity"] = {"accessed_count": 0, "modified_count": 0, "deleted_count": 0, "highest_severity": "NORMAL"}
                if log_entry["action"] == "created":
                    session["file_activity"]["accessed_count"] += 1
                elif log_entry["action"] == "modified":
                    session["file_activity"]["modified_count"] += 1
                elif log_entry["action"] == "deleted":
                    session["file_activity"]["deleted_count"] += 1
                if severity > session["file_activity"]["highest_severity"]:
                    session["file_activity"]["highest_severity"] = severity
                update_session_table()
                break
    elif event_type == "ransomware_detected":
        ransomware_data.append(log_entry)
        update_ransomware_table()
    elif event_type == "suspicious_activity":
        # Cập nhật bảng Session Monitor
        for session in session_data:
            if session["session_id"] == log_entry["session"]["session_id"]:
                if "file_activity" not in session:
                    session["file_activity"] = {"highest_severity": "NORMAL"}
                if severity > session["file_activity"]["highest_severity"]:
                    session["file_activity"]["highest_severity"] = severity
                update_session_table()
                break
    elif event_type == "new_connection":
        service_activity_data.append(log_entry)
        update_service_activity_table()
    elif event_type == "login_attempt":
        for activity in service_activity_data:
            if activity["client_ip"] == log_entry["session"]["client_ip"]:
                activity["fail_count"] = activity.get("fail_count", 0) + 1
                update_service_activity_table()
                break
        else:
            service_activity_data.append(log_entry)
            update_service_activity_table()
    else:
        service_activity_data.append(log_entry)
        update_service_activity_table()

# Hàm xử lý log queue
def process_log_queue():
    while True:
        try:
            log_entry = log_queue.get(timeout=1)
            process_log_event(log_entry)
        except Queue.empty: # Sửa lại dòng này
            pass

# Hàm hiển thị bảng
def display_table(table):
    console.print(table)

# Hàm hiển thị bảng log
def display_logs():
    for severity, log_config in LOG_CONFIG.items():
        log_file = log_config["file_path"]
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                logs = [json.loads(line.strip()) for line in f]
            console.print(f"[bold blue]LOGS - {severity}[/]")
            table = Table(title="Log View")
            table.add_column("Timestamp", style="cyan", width=20)
            table.add_column("Service", style="magenta", width=10)
            table.add_column("Event Type", style="yellow", width=15)
            table.add_column("Message", style="green", width=50)
            table.add_column("Severity", style="yellow", width=10)
            for log in logs:
                table.add_row(
                    log["timestamp"],
                    log["service"],
                    log["event_type"],
                    log["message"],
                    log["severity"]
                )
            console.print(table)

# Hàm main của console
def main():
    banner_text = Text.from_markup(
        """
        [bold green]___  ____  __  __  ____  _  _  ___  _____ 

        ██╗     ██╗   ██╗ █████╗  ██████╗  █████╗ 
        ██║     ██║   ██║██╔══██╗██╔════╝ ██╔══██╗
        ██║     ██║   ██║███████║██║  ███╗███████║
        ██║     ██║   ██║██╔══██║██║   ██║██╔══██║
        ███████╗╚██████╔╝██║  ██║╚██████╔╝██║  ██║
        ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
        ___  ____  __  __  ____  _  _  ___  _____ 

                [bold yellow]Welcome to ESXi Honeypot![/]
        """
    )
    aligned_banner = Align.center(banner_text)

    console.print(Panel(aligned_banner, title="[bold blue]Console[/]", expand=False))

    while True:
        if Confirm.ask("[bold yellow]Continue?[/]"):
            choice = Prompt.ask(
                "[bold blue]Select an option[/]",
                choices=["1", "2", "3", "4"],
            )
        else:
            console.print("[green]Exiting console.[/]")
            break

        if choice == "1":
            # Khởi động SSH Server
            ip_address = ""  # Thay thế bằng IP address mong muốn
            ssh_server_thread = threading.Thread(target=run_ssh_server, args=(ip_address,))
            ssh_server_thread.daemon = True
            ssh_server_thread.start()

            # Khởi động File Monitor
            file_monitor_thread = threading.Thread(target=start_file_monitor, args=(HONEYPOT_ROOT,))
            file_monitor_thread.daemon = True
            file_monitor_thread.start()

            # Khởi động Log Processor
            log_processor_thread = threading.Thread(target=process_log_queue)
            log_processor_thread.daemon = True
            log_processor_thread.start()

            console.print("[green]Honeypot started successfully.[/]")

        elif choice == "2":
            # Hiển thị bảng
            console.print("[bold blue]MONITOR[/]")
            display_table(session_table)
            display_table(file_activity_table)
            display_table(service_activity_table)
            display_table(ransomware_table)

        elif choice == "3":
            # Hiển thị log
            display_logs()

        elif choice == "4":
            if Confirm.ask("[bold yellow]Are you sure you want to exit?[/]"):
                console.print("[green]Exiting console.[/]")
                break

if __name__ == "__main__":
    main()