import datetime
import random
import time
import os

# Cấu hình
LOG_FILE = "var/log/auth.log"
MESSAGES = [
    "Connection from {ip} port {port}",
    "Accepted keyboard-interactive/pam for root from {ip} port {port} ssh2",
    "pam_unix(sshd:session): session opened for user root by (uid=0)",
    "User 'root' running command '{command}'",
    "pam_unix(sshd:session): session closed for user root",
    "Connection closed by {ip} port {port} [preauth]"
]
IP_ADDRESSES = ["208.100.26.1", "192.168.1.100", "10.0.0.10"]
ports = [54218, 2333]
COMMANDS = [
    "ls -l /",
    "cat /etc/passwd",
    "whoami",
    "id",
    "date",
    "uname -a",
]
REPEAT_INTERVAL = 5

# Hàm tạo dòng log
def generate_log_entry(timestamp_str, process_id, ip_address, port, command=None):
    """Tạo một dòng log ngẫu nhiên."""
    message = random.choice(MESSAGES)
    if "{command}" in message:
        message = message.format(command=random.choice(COMMANDS), ip=ip_address, port=port)
    else:
        message = message.format(ip=ip_address, port=random.choice(port))  # Chọn port ngẫu nhiên
    return f"{timestamp_str} sshd[{process_id}]: {message}"

# --- Chương trình chính ---
if __name__ == "__main__":
    start_time = datetime.datetime.now()
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    quantity = int(input("Nhập số lượng log giả muốn tạo: "))  # Nhập số lượng log
    i = 0

    # Vòng lặp chính
    while i < quantity:
        ip_address = random.choice(IP_ADDRESSES)
        timestamp = start_time + datetime.timedelta(seconds=random.randint(0, REPEAT_INTERVAL))
        timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        with open(LOG_FILE, "a") as f:
            for message in MESSAGES:
                process_id = random.randint(1000, 99999)
                log_entry = generate_log_entry(timestamp_str, process_id, ip_address, ports)
                print(log_entry)
                f.write(log_entry + "\n")
                i += 1  # Tăng biến đếm sau khi tạo mỗi log

        time.sleep(REPEAT_INTERVAL)