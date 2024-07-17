import datetime
import random
import time
import os
from configure import SHELL_LOG_FILE, SHELL_MESSAGES, SHELL_STATUSES, SHELL_COMMANDS, REPEAT_INTERVAL, DAYS_BACK

def generate_log_entry(message, timestamp, process_id, status=None, command=None):
    """Tạo một dòng log dựa trên message template."""
    message = message.format(
        id=process_id,
        status=status if status is not None else "",
        command=command if command is not None else "",
    )
    return timestamp, f"{timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z {message}"

def create_fake_shell_logs(quantity):
    """Tạo log giả mạo cho shell.log."""
    os.makedirs(os.path.dirname(SHELL_LOG_FILE), exist_ok=True)
    i = 0
    all_logs = []  # Danh sách để lưu trữ tất cả các log

    # Tạo dữ liệu log giả trong quá khứ
    for day in range(DAYS_BACK):
        start_time = datetime.datetime.now() - datetime.timedelta(days=day)
        for _ in range(random.randint(1, 5)):
            timestamp = start_time + datetime.timedelta(seconds=random.randint(0, 86400))
            
            # Dòng 1: Luôn in
            process_id = random.randint(1000, 99999)
            ssh_status = random.choice(SHELL_STATUSES)
            log_entry = generate_log_entry(SHELL_MESSAGES[0], timestamp, process_id, status=ssh_status)
            all_logs.append(log_entry)
            i += 1

            if ssh_status == "enabled":
                process_id = random.randint(1000, 99999)
                esxshell_status = random.choice(SHELL_STATUSES)
                log_entry = generate_log_entry(SHELL_MESSAGES[1], timestamp, process_id, status=esxshell_status)
                all_logs.append(log_entry)
                i += 1

                if esxshell_status == "enabled":
                    process_id = random.randint(1000, 99999)
                    log_entry = generate_log_entry(SHELL_MESSAGES[2], timestamp, process_id)
                    all_logs.append(log_entry)
                    i += 1

                    # Thực thi dòng 4 cho đến khi gặp command "exit" 
                    while i < quantity:
                        process_id = random.randint(1000, 99999)
                        command = random.choice(SHELL_COMMANDS)
                        log_entry = generate_log_entry(SHELL_MESSAGES[3], timestamp, process_id, command=command)
                        all_logs.append(log_entry)
                        i += 1
                        if command == "exit":
                            break
        if i >= quantity:
            break

    # Sắp xếp log theo timestamp
    all_logs.sort(key=lambda x: x[0])

    # Ghi log vào file
    with open(SHELL_LOG_FILE, "w") as f:
        for _, log_entry in all_logs:
            print(log_entry)  # In ra console
            f.write(log_entry + "\n")

    print(f"Đã tạo {i} log giả mạo vào file {SHELL_LOG_FILE}")