# config.py

# config.py

# ESXi Root Directory
ESXI_ROOT = "D:\ZALO"

# Filesystem Monitoring Configuration
MONITOR_INTERVAL = 1  # Giây
FOLDER_LOG_FILE = "folder_changes.txt"
NUM_THREADS = 4

# Auth Log Configuration
AUTH_LOG_FILE = "logs/auth.log"
AUTH_MESSAGES = [
    "Connection from {ip} port {port}",
    "Accepted keyboard-interactive/pam for root from {ip} port {port} ssh2",
    "pam_unix(sshd:session): session opened for user root by (uid=0)",
    "User 'root' running command '{command}'",
    "pam_unix(sshd:session): session closed for user root",
    "Connection closed by {ip} port {port} [preauth]"
]
AUTH_IP_ADDRESSES = ["208.100.26.1", "192.168.1.100", "10.0.0.10"]
AUTH_PORTS = [54218, 2333]

# Shell Log Configuration
SHELL_LOG_FILE = "logs/shell.log"
SHELL_MESSAGES = [
    "SSH[{id}]: SSH login {status}",
    "ESXShell[{id}]: ESXi shell login {status}",
    "shell[{id}]: Interactive shell session started",
    "shell[{id}]: [root]: {command}",
]
SHELL_STATUSES = ["enabled", "disabled"]
SHELL_COMMANDS = [
    "ls -l /",
    "cat /etc/passwd",
    "whoami",
    "id",
    "date",
    "uname -a",
    "exit"
]

# General Configuration
REPEAT_INTERVAL = 5  # Giây
DAYS_BACK = 10  # Số ngày log giả trong quá khứ