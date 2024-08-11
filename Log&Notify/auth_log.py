import datetime
import random
import time
import os
from configure import AUTH_LOG_FILE, AUTH_MESSAGES, AUTH_IP_ADDRESSES, AUTH_PORTS, SHELL_COMMANDS, REPEAT_INTERVAL

def generate_log_entry(timestamp_str, process_id, ip_address, port, command=None):
    """Tạo một dòng log ngẫu nhiên."""
    message = random.choice(AUTH_MESSAGES)
    if "{command}" in message:
        message = message.format(command=random.choice(SHELL_COMMANDS), ip=ip_address, port=port)
    else:
        message = message.format(ip=ip_address, port=random.choice(AUTH_PORTS))  # Chọn port ngẫu nhiên
    return f"{timestamp_str} sshd[{process_id}]: {message}"

def create_fake_auth_logs(quantity):
    """Tạo log giả mạo cho auth.log."""
    start_time = datetime.datetime.now()
    os.makedirs(os.path.dirname(AUTH_LOG_FILE), exist_ok=True)
    i = 0

    while i < quantity:
        ip_address = random.choice(AUTH_IP_ADDRESSES)
        timestamp = start_time + datetime.timedelta(seconds=random.randint(0, REPEAT_INTERVAL))
        timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        with open(AUTH_LOG_FILE, "a") as f:
            for message in AUTH_MESSAGES:
                process_id = random.randint(1000, 99999)
                log_entry = generate_log_entry(timestamp_str, process_id, ip_address, AUTH_PORTS)
                print(log_entry)
                f.write(log_entry + "\n")
                i += 1  

        time.sleep(REPEAT_INTERVAL)