import datetime
import time
import random
import os
#File log fake auth.log
LOG_FILE = "logs/auth.log" 
# Danh sách thông báo
messages = [
    "Connection from {ip} port {port}",
    "Accepted keyboard-interactive/pam for root from {ip} port {port} ssh2",
    "pam_unix(sshd:session): session opened for user root by (uid=0)",
    "User 'root' running command '{command}'",
    "pam_unix(sshd:session): session closed for user root",
    "Connection closed by {ip} port {port} [preauth]"
]

# IP và port
ip_addresses = ["208.100.26.1", "192.168.1.100", "10.0.0.10"]
port = [54218, 2333] 

# Các command ngẫu nhiên
commands = [
    "ls -l /",
    "cat /etc/passwd",
    "whoami",
    "id",
    "date",
    "uname -a",
]

# Thời gian lặp lại (giây)
repeat_interval = 5  # 3 giờ = 1800 giây

# Thời gian bắt đầu
start_time = datetime.datetime.now()

# Vòng lặp chính
while True:
    # Chọn IP ngẫu nhiên
    ip_address = random.choice(ip_addresses)

    # Tạo timestamp chung cho cụm log
    timestamp = start_time + datetime.timedelta(seconds=random.randint(0, repeat_interval))
    timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    # Kiểm tra và tạo file log nếu chưa tồn tại
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            pass  # Tạo file rỗng

    # Ghi log vào file
    with open(LOG_FILE, "a") as f:
        for message in messages:
            # ... (Tạo timestamp, process ID, message)
            process_id = random.randint(1000, 99999)
            if "{command}" in message:
                message = message.format(command=random.choice(commands), ip=ip_address, port=port)
            else:
                message = message.format(ip=ip_address, port=port)
            print(f"{timestamp_str} sshd[{process_id}]: {message}")
            f.write(f"{timestamp_str} sshd[{process_id}]: {message}\n")

    # Chờ đến chu kỳ lặp lại tiếp theo
    time.sleep(repeat_interval)


