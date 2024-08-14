# LUAGA

![image](https://github.com/user-attachments/assets/b4a8a659-0740-4ee9-9bf6-b664da382071)

## Welcome to LUAGA 
Official repository for LUAGA - VMWare ESXi Honeypot

## What is LUAGA 
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

##Requirements:

* Docker
* Python 3.9+
* Python Libraries: rich, paramiko, requests

##Learn more
