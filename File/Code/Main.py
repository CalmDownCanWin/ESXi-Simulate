import os

from Create_File_and_Folder import start_Luaga
from Create_File_and_Folder import monitor_Luaga_log


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
from Backup import main,create_backup_schedule
from Other_folder import create_esx_config_files,create_esx_proc,create_esx_tardisks_noauto,create_esx_vmimages




if __name__ == "__main__":
    esxi_choice = input("Chọn ESXi (ESXi_1, ESXi_2,...): ")
    base_path = os.path.join(os.path.expanduser("~"), esxi_choice)  # Thay thế bằng đường dẫn thực tế


    create_esx_config_files(base_path)
    create_esx_bin(base_path)
    create_esx_dev(base_path)
    create_esx_etc( base_path,config_type= esxi_choice)
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

    main(base_path, 7)
    # Tạo lịch trình backup
    create_backup_schedule(base_path, 7)

    # start_Luaga()
    # monitor_Luaga_log()
    print("Các file cấu hình ESXi 7 đã được tạo thành công!")
