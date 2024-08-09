# import os
# import subprocess
# import threading
# import sys
# from rich import print
# from rich.table import Table
# from rich.panel import Panel
# from rich.prompt import Prompt, Confirm
# from rich.progress import Progress, BarColumn, TextColumn
# from rich.text import Text
# from rich.align import Align
# from Create_File_and_Folder import start_Luaga, monitor_Luaga_log
# from bin import create_esx_bin
# from dev import create_esx_dev
# from etc import create_esx_etc
# from include_esxi import create_esx_include
# from lib_esxi import create_esx_lib
# from lib64_esxi import create_esx_lib64
# from opt import create_esx_opt
# from tardisks import create_esx_tardisks
# from tmp import create_esx_tmp
# from usr import create_esx_usr
# from var import create_esx_var
# from vmfs import create_esx_vmfs
# from Backup import main,create_backup_schedule
# from Other_folder import create_esx_config_files,create_esx_proc,create_esx_tardisks_noauto,create_esx_vmimages

# # Tên Docker network
# HONEYPOT_NETWORK = "honeypot_net"

# # Đường dẫn đến thư mục lưu trữ filesystem giả lập
# FILESYSTEM_ROOT = "/path/on/host"

# # Banner
# BANNER = """
# [bold green]___  ____  __  __  ____  _  _  ___  _____ 

# ██╗     ██╗   ██╗ █████╗  ██████╗  █████╗ 
# ██║     ██║   ██║██╔══██╗██╔════╝ ██╔══██╗
# ██║     ██║   ██║███████║██║  ███╗███████║
# ██║     ██║   ██║██╔══██║██║   ██║██╔══██║
# ███████╗╚██████╔╝██║  ██║╚██████╔╝██║  ██║
# ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
# ___  ____  __  __  ____  _  _  ___  _____ 

#         [bold yellow]Welcome to ESXi Honeypot![/]
# """

# def print_help():
#     table = Table(title="Available Commands")
#     table.add_column("Options", style="cyan", width=15)
#     table.add_column("Description", style="magenta")

#     table.add_row("-c, --create", "Create a new honeypot container")
#     table.add_row("-s, --start", "Start an existing honeypot container")
#     table.add_row("-st, --stop", "Stop a running honeypot container")
#     table.add_row("-r, --restart", "Restart a honeypot container")
#     table.add_row("-l, --logs", "Display logs of a honeypot container")
#     table.add_row("-S, --status", "Show status of all honeypot containers")
#     table.add_row("-h, --help", "Display this help message")
#     table.add_row("-g, --generate", "Generate ESXi filesystem")

#     print(table)

# def create_honeypot():
#     """Tạo honeypot mới."""
#     image = input("Docker Image (default: esxi-honeypot): ") or "esxi-honeypot"
#     ip_address = input("IP Address (default: 172.18.0.2): ") or "172.18.0.2"
#     hostname = input("Hostname (default: my-esxi-honeypot): ") or "my-esxi-honeypot"

#     # Tạo Docker network
#     subprocess.run(["docker", "network", "create", HONEYPOT_NETWORK], check=True)

#     # Chạy container
#     command = [
#         "docker", "run", "-d", "--name", hostname, "--net", HONEYPOT_NETWORK,
#         "--ip", ip_address, "-v", f"{FILESYSTEM_ROOT}:/app/data", image
#     ]
#     result = subprocess.run(command)

#     if result.returncode == 0:
#         print(f"[green]Honeypot '{hostname}' created successfully.[/]")
#     else:
#         print(f"[red]Error creating honeypot '{hostname}'.[/]")

# def start_honeypot():
#     """Khởi động honeypot."""
#     hostname = input("Honeypot Name: ")
#     result = subprocess.run(["docker", "start", hostname])
#     if result.returncode == 0:
#         print(f"[green]Honeypot '{hostname}' started successfully.[/]")
#     else:
#         print(f"[red]Error starting honeypot '{hostname}'.[/]")

# def stop_honeypot():
#     """Dừng honeypot."""
#     hostname = input("Honeypot Name: ")
#     result = subprocess.run(["docker", "stop", hostname])
#     if result.returncode == 0:
#         print(f"[green]Honeypot '{hostname}' stopped successfully.[/]")
#     else:
#         print(f"[red]Error stopping honeypot '{hostname}'.[/]")

# def restart_honeypot():
#     """Khởi động lại honeypot."""
#     hostname = input("Honeypot Name: ")
#     result = subprocess.run(["docker", "restart", hostname])
#     if result.returncode == 0:
#         print(f"[green]Honeypot '{hostname}' restarted successfully.[/]")
#     else:
#         print(f"[red]Error restarting honeypot '{hostname}'.[/]")

# def show_logs():
#     """Hiển thị log."""
#     hostname = input("Honeypot Name: ")
#     try:
#         subprocess.run(["docker", "logs", hostname], check=True)
#     except subprocess.CalledProcessError:
#         print(f"[red]Error retrieving logs for honeypot '{hostname}'.[/]")

# def show_status():
#     """Hiển thị trạng thái."""
#         # Liệt kê các container honeypot
#     result = subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, text=True)
#     honeypots = result.stdout.splitlines()

#     # Hiển thị trạng thái của từng honeypot
#     for honeypot in honeypots:
#         status_result = subprocess.run(["docker", "inspect", honeypot, "--format", "{{.State.Status}}"], capture_output=True, text=True)
#         ip_address_result = subprocess.run(["docker", "inspect", honeypot, "--format", "{{.NetworkSettings.Networks.honeypot_net.IPAddress}}"], capture_output=True, text=True)
#         status = status_result.stdout.strip()
#         ip_address = ip_address_result.stdout.strip()
#         print(f"Honeypot: {honeypot}, Status: {status}, IP Address: {ip_address}")

# def generate_esxi_filesystem():
#     """Tạo filesystem ESXi."""
#     esxi_choice = input("Chọn ESXi (ESXi_1, ESXi_2,...): ")
#     base_path = os.path.join(os.path.expanduser("~"), esxi_choice)

#     # Kiểm tra xem thư mục đã tồn tại chưa
#     if os.path.exists(base_path):
#         if Confirm.ask(f"Thư mục '{base_path}' đã tồn tại. Bạn có muốn ghi đè lên nó không?"):
#             os.rmdir(base_path)
#         else:
#             return

#     os.makedirs(base_path)

#     # Tạo các thư mục và file
#     create_esx_config_files(base_path)
#     create_esx_bin(base_path)
#     create_esx_dev(base_path)
#     create_esx_etc(base_path, config_type=esxi_choice)
#     create_esx_include(base_path)
#     create_esx_lib(base_path)
#     create_esx_lib64(base_path)
#     create_esx_opt(base_path)
#     create_esx_proc(base_path)
#     create_esx_tardisks(base_path)
#     create_esx_tardisks_noauto(base_path)
#     create_esx_tmp(base_path)
#     create_esx_usr(base_path)
#     create_esx_var(base_path)
#     create_esx_vmfs(base_path, esxi_choice, create_windows=True, create_kali_ubuntu=True,create_FreeBSD=True,create_window_server=True,create_MacOS=True,create_Kali_Centos=True, print_uuids=True)
#     create_esx_vmimages(base_path)

#     # Backup
#     main(base_path, 7)
#     create_backup_schedule(base_path, 7)

#     # Luaga
#     # start_Luaga()
#     # monitor_Luaga_log()
#     print(f"[green]Filesystem ESXi '{esxi_choice}' đã được tạo thành công![/]")

# def handle_flag(flag, arguments):
#     """Xử lý flag và arguments."""
#     if flag in ("-c", "--create"):
#         create_honeypot()
#     elif flag in ("-s", "--start"):
#         start_honeypot()
#     elif flag in ("-st", "--stop"):
#         stop_honeypot()
#     elif flag in ("-r", "--restart"):
#         restart_honeypot()
#     elif flag in ("-l", "--logs"):
#         show_logs()
#     elif flag in ("-S", "--status"):
#         show_status()
#     elif flag in ("-h", "--help"):
#         print_help()
#     elif flag in ("-g", "--generate"):
#         generate_esxi_filesystem()
#     else:
#         print(f"[bold red]Unknown flag: {flag}[/]")

# def main():
#     """Hàm main của console."""
#     banner_text = Text.from_markup(BANNER)
#     aligned_banner = Align.center(banner_text)

#     print(Panel(aligned_banner, title="[bold blue]Console[/]", expand=False))

#     if len(sys.argv) <= 1:
#         print_help()
#         return

#     # Phân tích arguments
#     args = sys.argv[1:]
#     while args:
#         flag = args.pop(0)
#         if flag.startswith("-"):
#             handle_flag(flag, args)
#         else:
#             print(f"[bold red]Invalid argument: {flag}[/]")

# if __name__ == "__main__":
#     main()

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
from Create_File_and_Folder import start_Luaga, monitor_Luaga_log
from bin import create_esx_bin
from dev import create_esx_dev
from etc import create_esx_etc
from include_esxi import create_esx_include
from lib_esxi import create_esx_lib
from lib64_esxi import create_esx_lib64
from opt import create_esx_opt
from tardisks import create_esx_tardisks
from tmp import create_esx_tmp
from usr import create_esx_usr
from var import create_esx_var
from vmfs import create_esx_vmfs
from Backup import main,create_backup_schedule
from Other_folder import create_esx_config_files,create_esx_proc,create_esx_tardisks_noauto,create_esx_vmimages

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
    table.add_row("-g, --generate", "Generate ESXi filesystem")

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

def generate_esxi_filesystem():
    """Tạo filesystem ESXi."""
    esxi_choice = input("Chọn ESXi (ESXi_1, ESXi_2,...): ")
    base_path = os.path.join(os.path.expanduser("~"), esxi_choice)

    # Kiểm tra xem thư mục đã tồn tại chưa
    if os.path.exists(base_path):
        if Confirm.ask(f"Thư mục '{base_path}' đã tồn tại. Bạn có muốn ghi đè lên nó không?"):
            os.rmdir(base_path)
        else:
            return

    os.makedirs(base_path)

    # Tạo các thư mục và file
    create_esx_config_files(base_path)
    create_esx_bin(base_path)
    create_esx_dev(base_path)
    create_esx_etc(base_path, config_type=esxi_choice)
    create_esx_include(base_path)
    create_esx_lib(base_path)
    create_esx_lib64(base_path)
    create_esx_opt(base_path)
    create_esx_proc(base_path)
    create_esx_tardisks(base_path)
    create_esx_tardisks_noauto(base_path)
    create_esx_tmp(base_path)
    create_esx_usr(base_path)
    create_esx_var(base_path)
    create_esx_vmfs(base_path, esxi_choice, create_windows=True, create_kali_ubuntu=True,create_FreeBSD=True,create_window_server=True,create_MacOS=True,create_Kali_Centos=True, print_uuids=True)
    create_esx_vmimages(base_path)

    # Backup
    main(base_path, 7)
    create_backup_schedule(base_path, 7)

    # Luaga
    # start_Luaga()
    # monitor_Luaga_log()
    print(f"[green]Filesystem ESXi '{esxi_choice}' đã được tạo thành công![/]")

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
    elif flag in ("-g", "--generate"):
        generate_esxi_filesystem()
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

    # Xét điều kiện để gọi các hàm
    if "-c" in sys.argv:
        create_honeypot()
    if "-s" in sys.argv:
        start_honeypot()
    if "-st" in sys.argv:
        stop_honeypot()
    if "-r" in sys.argv:
        restart_honeypot()
    if "-l" in sys.argv:
        show_logs()
    if "-S" in sys.argv:
        show_status()
    if "-g" in sys.argv:
        generate_esxi_filesystem()

if __name__ == "__main__":
    main()