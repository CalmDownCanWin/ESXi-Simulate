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
from vmfs import create_esx_vmfs
from Other_folder import create_esx_config_files,create_esx_proc,create_esx_tardisks_noauto,create_esx_vmimages


def start_Luaga():
    """Start Honeypot Luaga."""
    try:
        subprocess.Popen(["Luaga"])
        print("Luaga Honeypot is running...")
    except FileNotFoundError:
        print("Luaga is not installed.Please install Luaga before running.")

def monitor_Luaga_log():
    """Luaga's log monitor to detect SSH connection."""
    log_file = "S:/ESXI 7/var/log/shell.log" #file log contains data to receive bt ssh
    last_line = None
    while True:
        time.sleep(1)  # Check log every second
        with open(log_file, "r") as f:
            for line in f:
                if line != last_line:
                    last_line = line
                    if "SSH" in line or "Client" in line:
                        # Detect SSH connection from client
                        attacker_ip = line.split(" ")[4].strip()
                        print(f"Detect SSH connection from: {attacker_ip}")
                        # Processing when Attacker SSH from ESXI 1 to ESXI
                        if attacker_ip == "192.168.1.1":  #Address ESXI 1
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
                            print("Create ESXI 7 configuration file with another configuration.")
                        elif attacker_ip == "192.168.1.2":  # Esxi 2 address
                            # Create_esx_config_files (Config_type = "Advanced") # Retend the configuration file with another configuration
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
                            print("Create ESXI 7 configuration file with another configuration.")
                        elif attacker_ip == "192.168.1.162":  # Address ESXI 3
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
                            print("Create ESXI 7 configuration file with another configuration.")
                        elif attacker_ip == "192.168.1.16":  # Address ESXI 4
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
                            print("Create ESXI 7 configuration file with another configuration.")