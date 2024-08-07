import os
import datetime
import subprocess
import schedule
import time
import random

#  Import from ESXI_config.py
from ESXi_config import create_fake_file 
from vmfs_1 import ESXI_UUIDS

def create_backup_structure(base_path):
    """Tạo cấu trúc thư mục backup."""
    backup_path = os.path.join(base_path, "backup")
    os.makedirs(backup_path, exist_ok=True)

    # Tạo các thư mục con
    folders = [
        "App Backup",
        "Data Backup",
        "vm Backup"
    ]

    for folder in folders:
        os.makedirs(os.path.join(backup_path, folder), exist_ok=True)

    # Tạo cấu trúc cho App Backup
    app_backup_path = os.path.join(backup_path, "App Backup")
    create_app_backup_structure(app_backup_path)

    # Tạo cấu trúc cho Data Backup
    data_backup_path = os.path.join(backup_path, "Data Backup")
    create_data_backup_structure(data_backup_path)

    # Tạo cấu trúc cho vm Backup
    vm_backup_path = os.path.join(backup_path, "vm Backup")
    # create_vm_backup_structure(vm_backup_path)

    return backup_path

def create_app_backup_structure(app_backup_path):
    """Tạo cấu trúc thư mục cho App Backup."""
    folders = [
        "Virtualization System",
        "Business Applications",
        "Internal Applications",
        "Specialized Applications",
        "Technical Support Software",
        "Others"
    ]
    for folder in folders:
        os.makedirs(os.path.join(app_backup_path, folder), exist_ok=True)

    business_app_path = os.path.join(app_backup_path, "Business Applications")
    os.makedirs(os.path.join(business_app_path, "DBMS"), exist_ok=True)
    os.makedirs(os.path.join(business_app_path, "ERP"), exist_ok=True)
    os.makedirs(os.path.join(business_app_path, "CRM"), exist_ok=True)
    os.makedirs(os.path.join(business_app_path, "Accounting"), exist_ok=True)
    os.makedirs(os.path.join(business_app_path, "Email"), exist_ok=True)
    os.makedirs(os.path.join(business_app_path, "Web"), exist_ok=True)

    internal_app_path = os.path.join(app_backup_path, "Internal Applications")
    os.makedirs(os.path.join(internal_app_path, "HR"), exist_ok=True)
    os.makedirs(os.path.join(internal_app_path, "Project Management"), exist_ok=True)
    os.makedirs(os.path.join(internal_app_path, "Document Management"), exist_ok=True)
    os.makedirs(os.path.join(internal_app_path, "Network"), exist_ok=True)
    os.makedirs(os.path.join(internal_app_path, "Security"), exist_ok=True)

def create_data_backup_structure(data_backup_path):
    """Tạo cấu trúc thư mục cho Data Backup."""
    folders = [
        "Virtualization System",
        "Business Applications",
        "Internal Applications",
        "Specialized Applications",
        "Technical Support Software",
        "Others"
    ]
    for folder in folders:
        os.makedirs(os.path.join(data_backup_path, folder), exist_ok=True)

    business_app_path = os.path.join(data_backup_path, "Business Applications")
    os.makedirs(os.path.join(business_app_path, "DBMS"), exist_ok=True)
    os.makedirs(os.path.join(business_app_path, "ERP"), exist_ok=True)
    os.makedirs(os.path.join(business_app_path, "CRM"), exist_ok=True)
    os.makedirs(os.path.join(business_app_path, "Accounting"), exist_ok=True)
    os.makedirs(os.path.join(business_app_path, "Email"), exist_ok=True)
    os.makedirs(os.path.join(business_app_path, "Web"), exist_ok=True)

    internal_app_path = os.path.join(data_backup_path, "Internal Applications")
    os.makedirs(os.path.join(internal_app_path, "HR"), exist_ok=True)
    os.makedirs(os.path.join(internal_app_path, "Project Management"), exist_ok=True)
    os.makedirs(os.path.join(internal_app_path, "Document Management"), exist_ok=True)
    os.makedirs(os.path.join(internal_app_path, "Network"), exist_ok=True)
    os.makedirs(os.path.join(internal_app_path, "Security"), exist_ok=True)

def create_app_backup( backup_folder, app_name):
    """Tạo file nén backup cho ứng dụng."""
    for i in range(4):
        backup_date = (datetime.date.today() - datetime.timedelta(days=2)- datetime.timedelta(days=i*7)).strftime("%Y%m%d")
        backup_filename = f"{backup_date}_{app_name}_backup.tar.gz"
        backup_file = os.path.join(backup_folder, backup_filename)
        # # Tạo file giả mạo
        create_fake_file(backup_file, random.randint(10 * 1024 * 1024 * 1024, 30 * 1024 * 1024 * 1024))  # 10GB to 100GB
    print(f"Đã backup cơ sở dữ liệu: {app_name} vào {backup_file}")

def create_db_backup(backup_folder, db_name):
    """Tạo file nén backup cho cơ sở dữ liệu."""
    for i in range(4):
        backup_date = (datetime.date.today() - datetime.timedelta(days=2)- datetime.timedelta(days=i*7)).strftime("%Y%m%d")
        backup_filename = f"{backup_date}_{db_name}_backup.tar.gz"
        backup_file = os.path.join(backup_folder, backup_filename)
         # Tạo file giả mạo
        create_fake_file(backup_file, random.randint(20 * 1024 * 1024 * 1024, 40 * 1024 * 1024 * 1024))  # 10GB to 100GB

    print(f"Đã backup cơ sở dữ liệu: {db_name} vào {backup_file}")

def create_vm_backup(backup_path, vm_name, uuid, backup_date):
    """Tạo file nén backup cho VM (dung lượng giả mạo)."""
    for i in range(4):
        backup_date = (datetime.date.today() - datetime.timedelta(days=2)- datetime.timedelta(days=i*7)).strftime("%Y%m%d")
        backup_filename = f"{backup_date}_{vm_name}_backup.tar.gz"
        backup_file = os.path.join(backup_path, backup_filename)
    	# Tạo file backup giả mạo 
        fake_backup_size = random.randint(20 * 1024 * 1024 * 1024, 30 * 1024 * 1024 * 1024)  # 10GB (chỉnh sửa kích thước theo ý muốn)
        create_fake_file(backup_file, fake_backup_size)  # Tạo file với kích thước giả mạo
    
    print(f"Đã backup VM: {vm_name} trên vào {backup_file} (dung lượng giả mạo)")
        
def find_and_backup_vm(backup_path, vm_name, uuid, backup_date):
    """Tìm VM và tạo file nén backup."""
    vm_path = os.path.join(os.path.expanduser("~"), "ESXI 7","vmfs","volumes", uuid, vm_name)
    if os.path.isdir(vm_path):
        create_vm_backup(backup_path,  vm_name, uuid, backup_date)

def delete_old_backups(backup_path):
    """Xóa các file backup cũ hơn 30 ngày."""
    for filename in os.listdir(backup_path):
        file_path = os.path.join(backup_path, filename)
        # Kiểm tra xem file_path có phải là file và có đuôi là file nén hay không
        if os.path.isfile(file_path) and filename.endswith((".tar.gz", ".zip", ".7z")):  
            try:
                # Lấy thời gian tạo file
                creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
                # Kiểm tra thời gian tạo có lớn hơn 30 ngày không
                if (datetime.datetime.now() - creation_time).days > 30:
                    # Xóa file
                    os.remove(file_path)
                    print(f"Đã xóa file backup cũ: {file_path}")
            except Exception as e:
                print(f"Lỗi xóa file backup: {e}")


def create_backup_schedule(backup_path, days=7):
    """Tạo lịch trình backup."""
    schedule.every().day.at("00:00").do(lambda: main(backup_path, days))
    while True:
        schedule.run_pending()
        time.sleep(1)

def main(base_path, days=7):
    """Hàm chính để thực hiện backup."""
    backup_path = create_backup_structure(base_path)

    # Backup App
    app_backup_path = os.path.join(backup_path, "App Backup")
    # Backup hệ thống ảo hóa
    create_app_backup(os.path.join(app_backup_path, "Virtualization System"), "vCenter")
    # Backup các ứng dụng kinh doanh
    business_app_path = os.path.join(app_backup_path, "Business Applications")
    create_app_backup( os.path.join(business_app_path, "DBMS"), "DBMSName")
    create_app_backup( os.path.join(business_app_path, "ERP"), "ERPName")
    create_app_backup( os.path.join(business_app_path, "CRM"), "CRMName")
    create_app_backup( os.path.join(business_app_path, "Accounting"), "AccountingName")
    create_app_backup( os.path.join(business_app_path, "Email"), "EmailName")
    create_app_backup( os.path.join(business_app_path, "Web"), "WebsiteName")
    # Backup các ứng dụng nội bộ
    internal_app_path = os.path.join(app_backup_path, "Internal Applications")
    create_app_backup( os.path.join(internal_app_path, "HR"), "HRName")
    create_app_backup( os.path.join(internal_app_path, "Project Management"), "ProjectManagementName")
    create_app_backup( os.path.join(internal_app_path, "Document Management"), "DocumentManagementName")
    create_app_backup( os.path.join(internal_app_path, "Network"), "NetworkName")
    create_app_backup( os.path.join(internal_app_path, "Security"), "SecurityName")
    # Backup các ứng dụng chuyên ngành
    create_app_backup( os.path.join(app_backup_path, "Specialized Applications"), "SpecializedAppName")
    # Backup các phần mềm hỗ trợ kỹ thuật
    create_app_backup( os.path.join(app_backup_path, "Technical Support Software"), "SupportSoftwareName")
    # Backup các ứng dụng khác
    create_app_backup( os.path.join(app_backup_path, "Others"), "OtherAppName")

    # Backup Data
    data_backup_path = os.path.join(backup_path, "Data Backup")
    # Backup hệ thống ảo hóa
    create_db_backup(os.path.join(data_backup_path, "Virtualization System"), "vCenterDB")
    # Backup các ứng dụng kinh doanh
    business_app_path = os.path.join(data_backup_path, "Business Applications")
    create_db_backup(os.path.join(business_app_path, "DBMS"), "MySQL")
    create_db_backup(os.path.join(business_app_path, "DBMS"), "PostgreSQL")
    create_db_backup(os.path.join(business_app_path, "DBMS"), "Oracle")
    create_db_backup(os.path.join(business_app_path, "DBMS"), "SQLServer")
    create_db_backup(os.path.join(business_app_path, "ERP"), "ERPName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(os.path.join(business_app_path, "CRM"), "CRMName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(os.path.join(business_app_path, "Accounting"), "AccountingName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(os.path.join(business_app_path, "Email"), "EmailName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(os.path.join(business_app_path, "Web"), "WebsiteName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    # Backup các ứng dụng nội bộ
    internal_app_path = os.path.join(data_backup_path, "Internal Applications")
    create_db_backup(os.path.join(internal_app_path, "HR"), "HRName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(os.path.join(internal_app_path, "Project Management"), "ProjectManagementName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(os.path.join(internal_app_path, "Document Management"), "DocumentManagementName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(os.path.join(internal_app_path, "Network"), "NetworkName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(os.path.join(internal_app_path, "Security"), "SecurityName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    # Backup các ứng dụng chuyên ngành
    create_db_backup(os.path.join(data_backup_path, "Specialized Applications"), "SpecializedAppName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    # Backup các phần mềm hỗ trợ kỹ thuật
    create_db_backup(os.path.join(data_backup_path, "Technical Support Software"), "SupportSoftwareName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    # Backup các ứng dụng khác
    create_db_backup(os.path.join(data_backup_path, "Others"), "OtherAppName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần

    # Backup VM
    vm_backup_path = os.path.join(backup_path, "vm Backup")
    VM = [
        "Window_Server_2016",
        "Window_Server_2006",
        "Window_Server_2012",
        "Window_Server_2019",
        "Window_10", 
        "Window_7", 
        "Kali-Linux",
        "Window_11",
        "Window_8", 
        "Ubuntu",
        "Kali",
        "Centos",
        "MacOS_10",
        "MacOS_10.5",
        "MacOS_10.9",
        "MacOS_10.15",
        "MacOS_11",
        "MacOS_12",
        "FreeBSD_11",
        "FreeBSD_Pre-11",
        "FreeBSD_12",
        "FreeBSD_13",
    ]

    # Backup VM
    for esxi_host in ESXI_UUIDS:
        # Kiểm tra xem có VM nào trong ESXi host này không
        has_vm = False
        for uuid_key in ESXI_UUIDS[esxi_host]:
            if uuid_key.startswith("UUID"):
                uuid = ESXI_UUIDS[esxi_host][uuid_key]
                for vm_name in VM:
                    vm_path = os.path.join(os.path.expanduser("~"), "ESXI 7","vmfs","volumes", uuid, vm_name)
                    if os.path.isdir(vm_path):
                        has_vm = True
                        break
                if has_vm:
                    break

        if has_vm:
            # Tạo thư mục cho ESXi host
            esxi_backup_path = os.path.join(vm_backup_path, esxi_host)
            os.makedirs(esxi_backup_path, exist_ok=True)

            # Duyệt qua các VM
            for vm_name in VM:
                # Duyệt qua các key UUID trong ESXI_UUIDS[esxi_host]
                for uuid_key in ESXI_UUIDS[esxi_host]:
                    if uuid_key.startswith("UUID"):
                        uuid = ESXI_UUIDS[esxi_host][uuid_key]
                        for i in range(4):
                            backup_date = (datetime.date.today() - datetime.timedelta(days)).strftime("%Y%m%d")
                            if "UUID4" in ESXI_UUIDS[esxi_host]:
                                find_and_backup_vm(esxi_backup_path, vm_name, ESXI_UUIDS[esxi_host]["UUID4"], backup_date)
                            if "UUID3" in ESXI_UUIDS[esxi_host]:
                                find_and_backup_vm(esxi_backup_path, vm_name, ESXI_UUIDS[esxi_host]["UUID3"], backup_date)
                            if "UUID5" in ESXI_UUIDS[esxi_host]:
                                find_and_backup_vm(esxi_backup_path, vm_name, ESXI_UUIDS[esxi_host]["UUID5"], backup_date)

    delete_old_backups(app_backup_path)
    delete_old_backups(data_backup_path)
    delete_old_backups(vm_backup_path)

if __name__ == "__main__":
    base_path = os.path.join(os.path.expanduser("~"), "ESXI 7")  # Thay thế bằng đường dẫn thực tế
    main(base_path, 7)

    # Tạo lịch trình backup
    create_backup_schedule(base_path, 7)
