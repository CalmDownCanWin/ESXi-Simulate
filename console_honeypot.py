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


# Path to fs
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
    """New Honeypot."""
    image = Prompt.ask("Docker Image (default: esxi-honeypot): ") or "esxi-honeypot"
    ip_address = Prompt.ask("IP Address: ")
    hostname = Prompt.ask("Hostname (default: ESXI7): ") or "ESXI7"
    network_name = Prompt.ask("Network Name (default: esxi-net)") or "esxi-net"

    # Create Docker network
    subprocess.run(["docker", "network", "create", network_name], check=True, capture_output=True)

    # Run container
    command = [
        "docker", "run", "-d", "--name", hostname, "--net", network_name,
        "-v", f"{FILESYSTEM_ROOT}:/app/data", image
    ]
    result = subprocess.run(command, capture_output=True)

    if not ip_address:
        ip_address = get_IP_honeypot(hostname)

    if result.returncode == 0:
        print(f"[green]Honeypot '{hostname}' created successfully.[/]")
        print(f"[bold green]Container ID:[/]  {result.stdout.strip()}")
        print(f"[bold green]IP Address:[/]  {ip_address}")
    else:
        print(f"[red]Error creating honeypot '{hostname}'.[/]")

    # List Honeypot Process
    honeypot_processes[hostname] = result.stdout.strip()

def start_honeypot():
    """Running!"""
    hostname = Prompt.ask("Honeypot Name: ")

    # Check name honeypot
    if hostname in honeypot_processes:
        cotainer_name = honeypot_processes[hostname]

    # Interactive
        if Confirm.ask(f"Interactive with honeypot {hostname}? "):
            interact_with_container(cotainer_name)
        else:
            result = subprocess.run(["docker", "start", hostname])
            if result.returncode == 0:
                print(f"[green]Honeypot '{hostname}' started successfully.[/]")
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
    result = subprocess.run(["docker", "restart", hostname])
    if result.returncode == 0:
        print(f"[green]Honeypot '{hostname}' restarted successfully.[/]")
    else:
        print(f"[red]Error restarting honeypot '{hostname}'.[/]")

def show_logs():
    """Let me see who is coming!"""
    hostname = Prompt.ask("Honeypot Name: ")
    try:
        subprocess.run(["docker", "logs","-f", hostname], check=True)
    except subprocess.CalledProcessError:
        print(f"[red]Error retrieving logs for honeypot '{hostname}'.[/]")

def show_status():
    """How r u doing?"""
    # Container list
    result = subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, text=True)
    honeypots = result.stdout.splitlines()

    # Status
    for honeypot in honeypots:
        status_result = subprocess.run(["docker", "inspect", honeypot, "--format", "{{.State.Status}}"], capture_output=True, text=True)
        ip_address_result = subprocess.run(["docker", "inspect", honeypot, "--format", "{{.NetworkSettings.Networks.honeypot_net.IPAddress}}"], capture_output=True, text=True)
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
        subprocess.run(f"docker start -i {container_name} bash", shell=True)
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

honeypot_processes = {}

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