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
    """New Honeypot."""

    #Filesystem
    while True:
        filesystem_path = Prompt.ask("ESXi_Filesystem path: ")
        if os.path.isdir(filesystem_path):
            print(f"[green]ESXi_Filesystem path set to: {filesystem_path}[/]")
            break
        else:
            print(f"[red]Invalid path: {filesystem_path}[/]")

    #Docker image
    while True:
        image = Prompt.ask("Docker Image (Format 'image:tag'): ")
        result = subprocess.run(["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"], capture_output=True, text=True)
        images = result.stdout.splitlines()
        if image in images: 
            print(f"[green]Image '{image}' found.[/]")
            break
        else:
            print(f"[red]Image '{image}' not found. Please enter a valid image name.[/]")

    # Honeypot name
    while True:
        hostname = Prompt.ask("ESXi_Name (default: ESXI7): ") or "ESXI7"
        result = subprocess.run(["docker", "ps", "-a","--format","{{.Names}}"],capture_output=True, text=True)
        existing_hostname = result.stdout.splitlines()
        if hostname not in existing_hostname:
            print(f"[green]Honeypot '{hostname}' created successfully!")
            break
        else:
            print(f"[red]Honeypot '{hostname}' already exists!")


    # Network name
    while True:
        network_name = Prompt.ask("ESXi_Network_Name (default: esxi-net)") or "esxi-net"

        # Network Exists or not
        result = subprocess.run(["docker", "network", "ls", "--format", "{{.Name}}"], capture_output=True, text=True)
        existing_networks = result.stdout.splitlines()
        if network_name in existing_networks:
            print(f"[red]Network '{network_name}' already exists. Please choose a different name.[/]")
        else:
            # Create Docker network
            result = subprocess.run(["docker", "network", "create", "--driver", "bridge", network_name], check=True, capture_output=True)
            if result.returncode == 0:
                print(f"[green]Network '{network_name}' created successfully.[/]")
                break
            else:
                print(f"[red]Error creating network '{network_name}'. Please try again.[/]")

    print(f"[bold yellow]View your IP address with status option after creating honeypot[/]")
    
    # Run container
    command = [
        "docker", "run", "-it", "--name", hostname, "--net", network_name,
        "-p", "2222:2222", "-p" "4227:4227", "-v", f"{filesystem_path}:/app/data", image
    ]
    try:
        print(f"[green]Honeypot '{hostname}' created successfully.[/]")
        subprocess.run(command)
    except subprocess.CalledProcessError:
        print(f"[red]Error creating honeypot '{hostname}'.[/]")



def start_honeypot():
    """Running!"""
    # Check name honeypot
    while True:
        hostname = Prompt.ask("Honeypot Name: ")
        result = subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, text=True)
        honeypot_processes = result.stdout.splitlines()
        if hostname in honeypot_processes:
            print(f"[green]Honeypot {hostname} found!")
        # Interactive
            if Confirm.ask(f"Interactive with honeypot {hostname}? "):
                interact_with_container(hostname)
                break
            else:
                result = subprocess.run(["docker", "start", hostname])
                if result.returncode == 0:
                    print(f"[green]Honeypot '{hostname}' started successfully.[/]")
                    break
                else:
                    print(f"[red]Error starting honeypot '{hostname}'.[/]")
        else:
            print(f"[red]Honeypot {hostname} not found!.[/]")

def stop_honeypot():
    """Stop Here!"""
    hostname = Prompt.ask("Honeypot Name: ")
    result = subprocess.run(["docker", "stop", hostname])
    if result.returncode == 0:
        print(f"[green]Honeypot '{hostname}' stopped successfully.[/]")
    else:
        print(f"[red]Error stopping honeypot '{hostname}'.[/]")

def restart_honeypot():
    """Here We Go Again"""
    hostname = Prompt.ask("Honeypot Name: ")
    result = subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, text=True)
    existing_containers = result.stdout.splitlines()
    if hostname in existing_containers:
        result = subprocess.run(["docker", "restart", hostname])
        if result.returncode == 0:
            print(f"[green]Honeypot '{hostname}' restarted successfully.[/]")
            if Confirm.ask(f"Connect to honeypot '{hostname}'?"):
                    interact_with_container(hostname)
        else:
            print(f"[red]Error restarting honeypot '{hostname}'.[/]")
    else:
        print(f"[red]Honeypot '{hostname}' not found.[/]")

def show_logs():
    """Let me see who is coming!"""
    print(f"[bold yellow]Want to see logs? Make sure that your honeypot is running")
    hostname = Prompt.ask("Honeypot Name: ")
    result = subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, text=True)
    honeypot_name = result.stdout.splitlines()
    
    if hostname in honeypot_name:
        hostname_status = subprocess.run(["docker", "inspect", hostname, "--format", "{{.State.Status}}"], capture_output=True, text=True)
        status = hostname_status.stdout.strip()
        if status == "running":
            log_file = Prompt.ask("Log File", choices=["attack_logs.json", "honeypot.log"], default="honeypot.log")
            try:
                subprocess.run(["docker", "exec", hostname, "cat", f"/app/Logs/{log_file}"], check=True)
            except subprocess.CalledProcessError:
                print(f"[red]Error retrieving logs from '{log_file}' for honeypot '{hostname}'.[/]")
        else:
            print(f"[red]Honeypot {hostname} is not running!")

def show_status():
    """How r u doing?"""
    # Container list
    result = subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, text=True)
    honeypots = result.stdout.splitlines()

    # Status
    for honeypot in honeypots:
        status_result = subprocess.run(["docker", "inspect", honeypot, "--format", "{{.State.Status}}"], capture_output=True, text=True)
        ip_address_result = subprocess.run(["docker", "inspect","--format", "{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}", honeypot], capture_output=True, text=True)
        status = status_result.stdout.strip()
        ip_address = ip_address_result.stdout.strip()
        print(f"Honeypot: {honeypot}, Status: {status}, IP Address: {ip_address}")


def get_IP_honeypot(hostname):
    """If u dont know, let me show u"""
    result = subprocess.run(
        ["docker", "inspect", "--format", "{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}", hostname],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def interact_with_container(container_name):
    """Iteractive if u want"""
    try:
        subprocess.run(f"docker start -i {container_name}", shell=True)
    except Exception as e:
        print(f"[red]Error interactive with honeypot: {e}[/]")


def handle_flag(flag, arguments):
    """Options"""
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
    """LUAGA"""
    banner_text = Text.from_markup(BANNER)
    aligned_banner = Align.center(banner_text)

    print(Panel(aligned_banner, title="[bold blue]Console[/]", expand=False))

    if len(sys.argv) <= 1:
        print_help()
        return
    
    args = sys.argv[1:]
    while args:
        flag = args.pop(0)
        if flag.startswith("-"):
            handle_flag(flag, args)
        else:
            print(f"[bold red]Invalid argument: {flag}[/]")

if __name__ == "__main__":
    main()