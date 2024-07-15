import datetime
import random
import time
import os

# Cấu hình
LOG_FILE = "logs/shell.log"
MESSAGES = [
    "SSH[{id}]: SSH login {status}",
    "ESXShell[{id}]: ESXi shell login {status}",
    "shell[{id}]: Interactive shell session started",
    "shell[{id}]: [root]: {command}",
]
STATUSES = ["enabled", "disabled"]
COMMANDS = [
    "ls -l /",
    "cat /etc/passwd",
    "whoami",
    "id",
    "date",
    "uname -a",
]
REPEAT_INTERVAL = 5

def generate_log_entry(message, timestamp_str, process_id, status=None, command=None):
    """Tạo một dòng log dựa trên message template."""
    message = message.format(
        id=process_id,
        status=status if status is not None else "",  # Tránh lỗi KeyError
        command=command if command is not None else "",
    )
    return f"{timestamp_str} {message}"

# --- Chương trình chính ---
if __name__ == "__main__":
    start_time = datetime.datetime.now()
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    while True:
        timestamp = start_time + datetime.timedelta(seconds=random.randint(0, REPEAT_INTERVAL))
        timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        with open(LOG_FILE, "a") as f:
            # Dòng 1: Luôn in
            process_id = random.randint(1000, 99999)
            ssh_status = random.choice(STATUSES)
            log_entry = generate_log_entry(MESSAGES[0], timestamp_str, process_id, status=ssh_status)
            print(log_entry)
            f.write(log_entry + "\n")

            # Dòng 2, 3, 4: Chỉ in theo điều kiện
            if ssh_status == "enabled":
                process_id = random.randint(1000, 99999)
                esxshell_status = random.choice(STATUSES)
                log_entry = generate_log_entry(MESSAGES[1], timestamp_str, process_id, status=esxshell_status)
                print(log_entry)
                f.write(log_entry + "\n")

                if esxshell_status == "enabled":
                    process_id = random.randint(1000, 99999)
                    log_entry = generate_log_entry(MESSAGES[2], timestamp_str, process_id)
                    print(log_entry)
                    f.write(log_entry + "\n")

                    for _ in range(random.randint(1, 10)):
                        process_id = random.randint(1000, 99999)
                        log_entry = generate_log_entry(MESSAGES[3], timestamp_str, process_id, command=random.choice(COMMANDS))
                        print(log_entry)
                        f.write(log_entry + "\n")

        time.sleep(REPEAT_INTERVAL)