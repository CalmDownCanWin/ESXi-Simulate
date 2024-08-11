import os
import subprocess
import threading
import sys
from rich import print
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text
from rich.align import Align


# Tên Docker network
HONEYPOT_NETWORK = "honeypot_net"

# Đường dẫn đến thư mục lưu trữ filesystem giả lập
FILESYSTEM_ROOT = "/path/on/host"

# Banner
BANNER = """
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

def print_help():
    table = Table(title="Available Commands")
    table.add_column("Options", style="cyan", width=15)
    table.add_column("Description", style="magenta")

    table.add_row("-c, --create", "Create a new honeypot container")
    table.add_row("-s, --start", "Start an existing honeypot container")
    table.add_row("-st, --stop", "Stop a running honeypot container")
    table.add_row("-r, --restart", "Restart a honeypot container")
    table.add_row("-l, --logs", "Display logs of a honeypot container")
    table.add_row("-S, --status", "Show status of all honeypot containers")
    table.add_row("-h, --help", "Display this help message")

    print(table)

def create_honeypot():
    """Tạo honeypot mới."""
    image = input("Docker Image (default: esxi-honeypot): ") or "esxi-honeypot"
    ip_address = input("IP Address (default: 172.18.0.2): ") or "172.18.0.2"
    hostname = input("Hostname (default: my-esxi-honeypot): ") or "my-esxi-honeypot"

    # Tạo Docker network
    subprocess.run(["docker", "network", "create", HONEYPOT_NETWORK], check=True)

    # Chạy container
    command = [
        "docker", "run", "-d", "--name", hostname, "--net", HONEYPOT_NETWORK,
        "--ip", ip_address, "-v", f"{FILESYSTEM_ROOT}:/app/data", image
    ]
    result = subprocess.run(command)

    if result.returncode == 0:
        print(f"[green]Honeypot '{hostname}' created successfully.[/]")
    else:
        print(f"[red]Error creating honeypot '{hostname}'.[/]")

def start_honeypot():
    """Khởi động honeypot."""
    hostname = input("Honeypot Name: ")
    result = subprocess.run(["docker", "start", hostname])
    if result.returncode == 0:
        print(f"[green]Honeypot '{hostname}' started successfully.[/]")
    else:
        print(f"[red]Error starting honeypot '{hostname}'.[/]")

def stop_honeypot():
    """Dừng honeypot."""
    hostname = input("Honeypot Name: ")
    result = subprocess.run(["docker", "stop", hostname])
    if result.returncode == 0:
        print(f"[green]Honeypot '{hostname}' stopped successfully.[/]")
    else:
        print(f"[red]Error stopping honeypot '{hostname}'.[/]")

def restart_honeypot():
    """Khởi động lại honeypot."""
    hostname = input("Honeypot Name: ")
    result = subprocess.run(["docker", "restart", hostname])
    if result.returncode == 0:
        print(f"[green]Honeypot '{hostname}' restarted successfully.[/]")
    else:
        print(f"[red]Error restarting honeypot '{hostname}'.[/]")

def show_logs():
    """Hiển thị log."""
    hostname = input("Honeypot Name: ")
    try:
        subprocess.run(["docker", "logs", hostname], check=True)
    except subprocess.CalledProcessError:
        print(f"[red]Error retrieving logs for honeypot '{hostname}'.[/]")

def show_status():
    """Hiển thị trạng thái."""
        # Liệt kê các container honeypot
    result = subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, text=True)
    honeypots = result.stdout.splitlines()

    # Hiển thị trạng thái của từng honeypot
    for honeypot in honeypots:
        status_result = subprocess.run(["docker", "inspect", honeypot, "--format", "{{.State.Status}}"], capture_output=True, text=True)
        ip_address_result = subprocess.run(["docker", "inspect", honeypot, "--format", "{{.NetworkSettings.Networks.honeypot_net.IPAddress}}"], capture_output=True, text=True)
        status = status_result.stdout.strip()
        ip_address = ip_address_result.stdout.strip()
        print(f"Honeypot: {honeypot}, Status: {status}, IP Address: {ip_address}")

def handle_flag(flag, arguments):
    """Xử lý flag và arguments."""
    if flag in ("-c", "--create"):
        create_honeypot()
    elif flag in ("-s", "--start"):
        start_honeypot()
    elif flag in ("-st", "--stop"):
        stop_honeypot()
    elif flag in ("-r", "--restart"):
        restart_honeypot()
    elif flag in ("-l", "--logs"):
        show_logs()
    elif flag in ("-S", "--status"):
        show_status()
    elif flag in ("-h", "--help"):
        print_help()
    else:
        print(f"[bold red]Unknown flag: {flag}[/]")

def main():
    """Hàm main của console."""
    banner_text = Text.from_markup(BANNER)
    aligned_banner = Align.center(banner_text)

    print(Panel(aligned_banner, title="[bold blue]Console[/]", expand=False))

    if len(sys.argv) <= 1:
        print_help()
        return

    # Phân tích arguments
    args = sys.argv[1:]
    while args:
        flag = args.pop(0)
        if flag.startswith("-"):
            handle_flag(flag, args)
        else:
            print(f"[bold red]Invalid argument: {flag}[/]")

if __name__ == "__main__":
    main()