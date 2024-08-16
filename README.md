# **LUAGA**

```python
╭───────────────── Console ──────────────────╮
│                                            │
│ ___  ____  __  __  ____  _  _  ___  _____  │
│                                            │
│ ██╗     ██╗   ██╗ █████╗  ██████╗  █████╗  │
│ ██║     ██║   ██║██╔══██╗██╔════╝ ██╔══██╗ │
│ ██║     ██║   ██║███████║██║  ███╗███████║ │
│ ██║     ██║   ██║██╔══██║██║   ██║██╔══██║ │
│ ███████╗╚██████╔╝██║  ██║╚██████╔╝██║  ██║ │
│ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ │
│ ___  ____  __  __  ____  _  _  ___  _____  │
│                                            │
│         Welcome to ESXi Honeypot!          │
│                                            │
╰────────────────────────────────────────────╯
                     Available Commands                     
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Options         ┃ Description                            ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -c, --create    │ Create a new honeypot container        │
│ -s, --start     │ Start an existing honeypot container   │
│ -st, --stop     │ Stop a running honeypot container      │
│ -r, --restart   │ Restart a honeypot container           │
│ -l, --logs      │ Display logs of a honeypot container   │
│ -S, --status    │ Show status of all honeypot containers │
│ -h, --help      │ Display this help message              │
└─────────────────┴────────────────────────────────────────┘

```

## Welcome to **LUAGA** 
Official repository for LUAGA - VMWare ESXi Honeypot

## What is **LUAGA** 
LUAGA - ESXi Honeypot, a deceptive system designed to emulate a VMware ESXi server to attract and analyze ransomware attacks targeting this platform.

## Key Features 

- **Shell and Filesystem Emulation**: The honeypot emulates the ESXi shell and filesystem, providing simulated commands such as esxcli, vim-cmd, vmdumper, and more.
- **Attack Script Handling**: The honeypot can analyze and simulate the execution of attacker-provided shell scripts (.sh) and Python scripts (.py).
- **"Honey on honey" Mechanisms**: The honeypot leads attackers to other interactions within the system, encouraging them to reveal more of their TTPs.
- **Comprehensive Logging**: All attacker actions are meticulously logged, including IP address, timestamp, command, arguments, output, and results.
- **Docker Containerization**: The honeypot is packaged as a Docker container for easy deployment and isolation.

## Highlights

- **ESXi-Specific Focus**: The honeypot is specifically tailored for ESXi, accurately emulating commands and behavior.
- **Ransomware Detection**: The honeypot can identify common ESXi ransomware patterns and simulate attacks to gather intelligence on their operation.
- **Extensibility**: The modular design allows for easy addition of new commands and features.

## Requirements:

* Docker
* Python 3.9+
* Python Libraries: rich, paramiko, requests

## How to use 

- Download this source:
  ```cmd
  git clone https://github.com/TTSB3K30/ESXi-Simulate.git
  ```
- Go to folder `File/Code` and run `Main.py` to create Filesystem
- Make sure that you create SSH key-pair in `Src/Services` with:
  ```cmd
  ssh-keygen -t rsa
  ```
- Go to `Src` and build image with `Dockerfile`
- Run `console` to build your ESXI-Honeypot
