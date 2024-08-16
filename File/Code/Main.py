import os

# from Create_File_and_Folder import start_Luaga
# from Create_File_and_Folder import monitor_Luaga_log


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
# from Backup import Backup,create_backup_schedule
from Other_folder import create_esx_config_files,create_esx_proc,create_esx_tardisks_noauto,create_esx_vmimages




if __name__ == "__main__":
    esxi_choice = input("Select ESXI (ESXi_1, ESXi_2, ...): ")
    Ip = input("Select IP_Adress : ")
    # base_path = os.path.join(os.path.expanduser("~"), esxi_choice)  # Replace by actual path
    while True:
        path = input("Nhập đường dẫn (path) bạn muốn tạo file hệ thống (ví dụ: /home/user/ESXI_7): ")
        if os.path.exists(path):
            break
        else:
            print("Đường dẫn không hợp lệ. Vui lòng nhập lại.")
    base_path = os.path.join(path, esxi_choice)

    create_esx_config_files(base_path)
    create_esx_bin(base_path)
    create_esx_dev(base_path)
    create_esx_etc( base_path,Ip,esxi_choice)
    create_esx_include(base_path)
    create_esx_lib(base_path)
    create_esx_lib64(base_path)
    create_esx_opt(base_path)
    create_esx_proc(base_path)
    create_esx_tardisks(base_path)
    create_esx_tardisks_noauto(base_path)
    create_esx_tmp(base_path)
    create_esx_usr(base_path)
    create_esx_var(base_path)
    create_esx_vmfs(base_path, esxi_choice, create_windows=True, create_kali_ubuntu=True,create_FreeBSD=True,create_window_server=True,create_MacOS=True,create_Kali_Centos=True, print_uuids=True)
    create_esx_vmimages(base_path)

    #Backup(base_path, 7)
    # Create a backup schedule
    #create_backup_schedule(base_path, 7)

    # start_Luaga()
    # monitor_Luaga_log()
    print("Esxi configuration files have been successfully created!")
