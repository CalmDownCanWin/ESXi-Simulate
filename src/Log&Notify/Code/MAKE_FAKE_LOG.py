import random
import datetime
import os
import re

def generate_fake_logs(input_file, output_file, decoy_users=None, decoy_ips=None, decoy_chance=0.2):
    """Tạo log giả từ file log gốc, thêm thông tin mồi và yếu tố ngẫu nhiên."""
    decoy_users = decoy_users or ["root", "admin", "backup"]
    decoy_ips = decoy_ips or ["192.168.1.101", "10.0.0.5", "172.16.10.20"]
    log_levels = ["INFO", "WARNING", "ERROR"]
    dynamic_mo_types = ["vim.EsxCLI.storage.core.path", "vim.EsxCLI.network.vswitch.standard.port", "vim.EsxCLI.iscsi.software.target"]
    wsdl_names = ["VimEsxCLIstoragecorepath", "VimEsxCLInetworkvswitchstandardport", "VimEsxCLIiscsisoftwaretarget"]
    components = ["hostd", "vpxa", "vobd", "vpxd"]
    sub_components = ["Default", "Vimsvc.ha-eventmgr", "Solo.VmwareCLI"]

    timestamp_formats = [
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z",  # YYYY-MM-DDTHH:MM:SS.mmmZ
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",          # YYYY-MM-DD HH:MM:SS
    ]

    with open(input_file, "r", encoding="utf-8") as f_in, open(output_file, "a", encoding="utf-8") as f_out:
        for line in f_in:
            # Bỏ qua các dòng trống
            if not line.strip():
                continue

            # Xóa thông tin nhạy cảm nếu có
            line = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', lambda match: random.choice(decoy_ips), line)
            new_line = re.sub(r'user [a-zA-Z0-9]+', lambda match: f"user {random.choice(decoy_users)}", line)
            if new_line is not None:
                line = new_line

            # Tìm kiếm định dạng timestamp phù hợp
            timestamp_match = None
            for timestamp_format in timestamp_formats:
                timestamp_match = re.match(timestamp_format, line)
                if timestamp_match:
                    break

            if timestamp_match:
                try:
                    timestamp_str = timestamp_match.group(0)
                    timestamp = datetime.datetime.strptime(timestamp_str, timestamp_format)
                    timestamp += datetime.timedelta(seconds=random.randint(-60, 60))
                    new_timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

                    # Thêm log level nếu chưa có
                    if not any(line.startswith(level) for level in log_levels):
                        line = f"{new_timestamp_str} {random.choice(log_levels)} {line[len(timestamp_str):]}"
                    else:
                        line = new_timestamp_str + line[len(timestamp_str):]

                    # Thêm thông tin mồi nếu có thể
                    if random.random() < decoy_chance:
                        if "SSH session was opened" in line:
                            decoy_user = random.choice(decoy_users)
                            decoy_ip = random.choice(decoy_ips)
                            line = line.replace("root", decoy_user).replace("208.100.26.1", decoy_ip)
                        elif "Authentication" in line:
                            fail_types = ["failed", "succeeded"]
                            fail_type = random.choice(fail_types)
                            decoy_user = random.choice(decoy_users)
                            decoy_ip = random.choice(decoy_ips)
                            line = line.replace("failed", f"{fail_type} for user {decoy_user} from {decoy_ip}")
                        elif "Glibc malloc guards" in line:
                            pid = random.randint(60000, 70000)
                            origin = f"[Originator@{random.randint(6000, 7000)} sub=Default]"
                            states = ["disabled", "enabled"]
                            state = random.choice(states)
                            line = f"{new_timestamp_str} info -[{pid}] {origin} Glibc malloc guards {state}."
                        elif "CreateDynMoType" in line:
                            mo_type = random.choice(dynamic_mo_types)
                            wsdl_name = random.choice(wsdl_names)
                            line = f"{new_timestamp_str} info hostd[{random.randint(60000, 70000)}] [Originator@6876 sub=Solo.VmwareCLI] CreateDynMoType (Type {mo_type}) (Wsdl {wsdl_name}) (Version vim.version.version5)."
                        else:
                            component = random.choice(components)
                            sub_component = random.choice(sub_components)
                            new_line = line.split()
                            line = f"{new_timestamp_str} {new_line[1]} {component}[{random.randint(60000, 70000)}] [Originator@6876 sub={sub_component}] {' '.join(new_line[4:])}"

                except ValueError as e:
                    print(f"Lỗi xử lý dòng: {e} - Dòng gốc: {line}")

            f_out.write(line)  # Ghi lại dòng log (đã xử lý hoặc không)



# Đường dẫn đến file log gốc và file log giả
input_log_file = "logs/hostd.log_2024-06-30_23-06-21.txt" 
output_log_file = "hostd.log"

generate_fake_logs(input_log_file, output_log_file)
