import time
import subprocess


from bin import create_esx_bin
from dev import create_esx_dev
from etc import create_esx_etc
from include_esxi import create_esx_include
from lib_esxi import create_esx_lib
from lib64_esxi import create_esx_lib64
from opt import create_esx_opt
from tardisks import create_esx_tardisks
from tmp import create_esx_tmp
from usr import create_esx_usr
from var import create_esx_var
from vmfs_1 import create_esx_vmfs
from Other_folder import create_esx_config_files,create_esx_proc,create_esx_tardisks_noauto,create_esx_vmimages


def start_Luaga():
    """Bắt đầu honeypot Luaga."""
    try:
        subprocess.Popen(["Luaga"])
        print("Luaga honeypot đang chạy...")
    except FileNotFoundError:
        print("Luaga không được cài đặt. Vui lòng cài đặt Luaga trước khi chạy.")

def monitor_Luaga_log():
    """Giám sát log của Luaga để phát hiện kết nối SSH."""
    log_file = "S:/ESXI 7/var/log/shell.log" #file log chứa dữ liệu để nhận bt ssh
    last_line = None
    while True:
        time.sleep(1)  # Kiểm tra log mỗi giây
        with open(log_file, "r") as f:
            for line in f:
                if line != last_line:
                    last_line = line
                    if "SSH" in line or "Client" in line:
                        # Phát hiện kết nối SSH từ Client
                        attacker_ip = line.split(" ")[4].strip()
                        print(f"Phát hiện kết nối SSH từ: {attacker_ip}")
                        # Xử lý khi attacker SSH từ ESXi 1 sang ESXi khác
                        if attacker_ip == "192.168.1.1":  # Địa chỉ ESXi 1
                            create_esx_config_files()
                            create_esx_bin()
                            create_esx_dev()
                            create_esx_etc(config_type="ESXI 2")
                            create_esx_include()
                            create_esx_lib()
                            create_esx_lib64()
                            create_esx_opt()
                            create_esx_proc()
                            create_esx_tardisks()
                            create_esx_tardisks_noauto()
                            create_esx_tmp()
                            create_esx_usr()
                            create_esx_var()
                            create_esx_vmfs()
                            create_esx_vmimages()
                            print("Tạo lại file cấu hình ESXi 7 với cấu hình khác.")
                        elif attacker_ip == "192.168.1.2":  # Địa chỉ ESXi 2
                            # create_esx_config_files(config_type="advanced")  # Tạo lại file cấu hình với cấu hình khác
                            create_esx_config_files()
                            create_esx_bin()
                            create_esx_dev()
                            create_esx_etc(config_type="ESXI 3")
                            create_esx_include()
                            create_esx_lib()
                            create_esx_lib64()
                            create_esx_opt()
                            create_esx_proc()
                            create_esx_tardisks()
                            create_esx_tardisks_noauto()
                            create_esx_tmp()
                            create_esx_usr()
                            create_esx_var()
                            create_esx_vmfs()
                            create_esx_vmimages()
                            print("Tạo lại file cấu hình ESXi 7 với cấu hình khác.")
                        elif attacker_ip == "192.168.1.162":  # Địa chỉ ESXi 3
                            create_esx_config_files()
                            create_esx_bin()
                            create_esx_dev()
                            create_esx_etc(config_type="ESXI 4")
                            create_esx_include()
                            create_esx_lib()
                            create_esx_lib64()
                            create_esx_opt()
                            create_esx_proc()
                            create_esx_tardisks()
                            create_esx_tardisks_noauto()
                            create_esx_tmp()
                            create_esx_usr()
                            create_esx_var()
                            create_esx_vmfs()
                            create_esx_vmimages()
                            print("Tạo lại file cấu hình ESXi 7 với cấu hình khác.")
                        elif attacker_ip == "192.168.1.16":  # Địa chỉ ESXi 4
                            create_esx_config_files()
                            create_esx_bin()
                            create_esx_dev()
                            create_esx_etc(config_type="ESXI 5")
                            create_esx_include()
                            create_esx_lib()
                            create_esx_lib64()
                            create_esx_opt()
                            create_esx_proc()
                            create_esx_tardisks()
                            create_esx_tardisks_noauto()
                            create_esx_tmp()
                            create_esx_usr()
                            create_esx_var()
                            create_esx_vmfs()
                            create_esx_vmimages()
                            print("Tạo lại file cấu hình ESXi 7 với cấu hình khác.")