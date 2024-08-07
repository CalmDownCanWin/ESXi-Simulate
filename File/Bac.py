import os
import datetime
import subprocess
import schedule
import time
import random

#  Import from ESXI_config.py
from ESXi_config import create_fake_file

def create_backup_structure(base_path):
    """Create the backup directory structure."""
    backup_path = os.path.join(base_path, "backup")
    os.makedirs(backup_path, exist_ok=True)

    # Create "Data Backup" subdirectory
    data_backup_path = os.path.join(backup_path, "Data Backup")
    os.makedirs(data_backup_path, exist_ok=True)
    
    # Create "App Backup" subdirectory
    app_backup_path = os.path.join(backup_path, "App Backup")
    os.makedirs(app_backup_path, exist_ok=True)

    # Create subfolders for "Data Backup"
    subfolders = [
        "Virtualization System",
        "Business Applications",
        "Internal Applications",
        "Specialized Applications",
        "Technical Support Software",
        "Others"
    ]
    for folder in subfolders:
        os.makedirs(os.path.join(app_backup_path, folder), exist_ok=True)
    for folder in subfolders:
        os.makedirs(os.path.join(data_backup_path, folder), exist_ok=True)

    # Create subfolders for "Business Applications"
    business_app_path = os.path.join(app_backup_path, "Business Applications")
    business_data_path = os.path.join(data_backup_path, "Business Applications")
    business_subfolders = [
        "DBMS",
        "ERP",
        "CRM",
        "Accounting",
        "Email",
        "Web"
    ]
    for folder in business_subfolders:
        os.makedirs(os.path.join(business_app_path, folder), exist_ok=True)
    for folder in business_subfolders:
        os.makedirs(os.path.join(business_data_path, folder), exist_ok=True)

    # Create subfolders for "Internal Applications"
    internal_app_path = os.path.join(app_backup_path, "Internal Applications")
    internal_data_path = os.path.join(data_backup_path, "Internal Applications")
    internal_subfolders = [
        "HR",
        "Project Management",
        "Document Management",
        "Network",
        "Security"
    ]
    for folder in internal_subfolders:
        os.makedirs(os.path.join(internal_app_path, folder), exist_ok=True)
    for folder in internal_subfolders:
        os.makedirs(os.path.join(internal_data_path, folder), exist_ok=True)

    # Create "vm Backup" subdirectory
    vm_backup_path = os.path.join(backup_path, "vm Backup")
    os.makedirs(vm_backup_path, exist_ok=True)

    return data_backup_path, vm_backup_path

def create_app_backup_file(backup_path, folder_name, app_name):
    """Create a compressed backup file for the application."""
    today = datetime.date.today().strftime("%Y%m%d")
    backup_filename = f"{today}_{app_name}_backup.tar.gz"
    backup_file = os.path.join(backup_path, folder_name, backup_filename)

    # Use the tar command for compression
    # Replace with the appropriate command for the application type (e.g., mysqldump, vCenter backup)
    subprocess.run(["tar", "-czvf", backup_file, "/ESXI 7/vmfs/volumes/"])  # Replace with the actual path to the data to be backed up
    print(f"Backed up application {app_name} to {backup_file}")

def create_db_backup_file(backup_path, folder_name, db_name, db_type):
    """Create a compressed backup file for the database."""
    today = datetime.date.today().strftime("%Y%m%d")
    backup_filename = f"{today}_{db_name}_backup.tar.gz"
    backup_file = os.path.join(backup_path, folder_name, backup_filename)

    # Use the appropriate command for the database type (e.g., mysqldump, pg_dump)
    if db_type == "MySQL":
        subprocess.run(["mysqldump", "-u", "username", "-p", "database_name", ">", backup_file])
    elif db_type == "PostgreSQL":
        subprocess.run(["pg_dump", "-h", "hostname", "-p", "port", "-U", "username", "database_name", ">", backup_file])
    # Add commands for other database types
    else:
        print(f"Database type {db_type} not supported.")

def create_vm_backup(backup_path, esxi_name, vm_name):
    """Create a compressed backup file for the virtual machine."""
    today = datetime.date.today().strftime("%Y%m%d")
    backup_filename = f"{today}_{vm_name}_backup.tar.gz"
    backup_file = os.path.join(backup_path, esxi_name, vm_name, backup_filename)

    # Path to the directory containing VM data
    vm_data_path = f"/ESXI 7/vmfs/volumes/{vm_name}"  # Replace with the actual path
    
    # Use the tar command for compression
    subprocess.run(["tar", "-czvf", backup_file, vm_data_path])
    print(f"Backed up virtual machine {vm_name} on ESXi {esxi_name} to {backup_file}")

    # Create a fake file with large size
    fake_backup_file = os.path.join(backup_path, esxi_name, vm_name, f"{today}_{vm_name}_backup_fake.tar.gz")
    create_fake_file(fake_backup_file, random.randint(10 * 1024 * 1024 * 1024, 100 * 1024 * 1024 * 1024))  # 10GB to 100GB

def delete_old_backups(backup_path, days=7):
    """Delete backup files older than `days` days."""
    try:
        for root, dirs, files in os.walk(backup_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_created_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
                if (datetime.datetime.now() - file_created_time).days > days:
                    os.remove(file_path)
                    print(f"Deleted old backup file: {file_path}")
    except Exception as e:
        print(f"Error deleting backup: {e}")

def create_backup_schedule(backup_path, days=7):
    """Create a backup schedule."""
    schedule.every().days.at("00:00").do(lambda: main(backup_path, days))
    while True:
        schedule.run_pending()
        time.sleep(1)

def restore_vm_backup(backup_path, esxi_name, vm_name):
    """Restore a VM backup."""
    today = datetime.date.today().strftime("%Y%m%d")
    backup_file = os.path.join(backup_path, esxi_name, vm_name, f"{today}_{vm_name}_backup.tar.gz")
    vm_data_path = f"/ESXI 7/vmfs/volumes/{vm_name}"  # Replace with the actual path

    try:
        subprocess.run(["tar", "-xzvf", backup_file, "-C", vm_data_path])
        print(f"Restored virtual machine {vm_name} on ESXi {esxi_name} from {backup_file}")
    except Exception as e:
        print(f"Error restoring VM: {e}")

def main(base_path, days=7):
    """Main function to perform backup."""
    data_backup_path, vm_backup_path, app_backup_path = create_backup_structure(base_path)

    # Backup Hệ thống ảo hóa
    create_db_backup_file(data_backup_path, "Virtualization Systems", "vCenterDB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần

    # Backup Ứng dụng kinh doanh
    create_db_backup_file(data_backup_path, "Business Applications", "MySQL", "MySQL")
    create_db_backup_file(data_backup_path, "Business Applications", "PostgreSQL", "PostgreSQL")
    create_db_backup_file(data_backup_path, "Business Applications", "Oracle", "Oracle")  # Thêm các loại cơ sở dữ liệu khác nếu cần
    create_db_backup_file(data_backup_path, "Business Applications", "SQLServer", "SQLServer")  # Thêm các loại cơ sở dữ liệu khác nếu cần
    
    
    create_app_backup_file(app_backup_path, "Business Applications", "ERPName")
    create_app_backup_file(data_backup_path, "Business Applications", "CRMName")
    create_app_backup_file(data_backup_path, "Business Applications", "AccountingName")
    create_app_backup_file(data_backup_path, "Business Applications", "EmailName")
    create_app_backup_file(data_backup_path, "Business Applications", "WebsiteName")

    # Backup Ứng dụng nội bộ
    create_app_backup_file(data_backup_path, "Internal Applications", "HRName")
    create_app_backup_file(data_backup_path, "Internal Applications", "ProjectManagementName")
    create_app_backup_file(data_backup_path, "Internal Applications", "DocumentManagementName")
    create_app_backup_file(data_backup_path, "Internal Applications", "NetworkName")
    create_app_backup_file(data_backup_path, "Internal Applications", "SecurityName")

    # Backup Ứng dụng chuyên ngành
    create_app_backup_file(data_backup_path, "Specialized Applications", "SpecializedAppName")

    # Backup Phầm mềm hỗ trợ kỹ thuật
    create_app_backup_file(data_backup_path, "Technical Support Software", "SupportSoftwareName")

    # Backup Others
    create_app_backup_file(data_backup_path, "Others", "OtherAppName")

    # Backup VM
    # Get ESXi list
    esxi_list = ["ESXi_1", "ESXi_2","ESXI_3","ESXI_4","ESXI_5"]  # Replace with actual ESXi list

    for esxi_name in esxi_list:
        # Create directory for ESXi
        esxi_backup_path = os.path.join(vm_backup_path, esxi_name)
        os.makedirs(esxi_backup_path, exist_ok=True)

        # Get the list of virtual machines on ESXi
        # Use the appropriate command to list VMs on ESXi (e.g., `esxcli vm list`)
        vm_list = ["VM_Name1", "VM_Name2"]  # Replace with actual VM list

        for vm_name in vm_list:
            # Create directory for VM
            vm_backup_path = os.path.join(esxi_backup_path, vm_name)
            os.makedirs(vm_backup_path, exist_ok=True)

            # Perform virtual machine backup
            create_vm_backup(vm_backup_path, esxi_name, vm_name)

    # Restore VM backup (one day before)
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    for esxi_name in esxi_list:
        for vm_name in vm_list:
            restore_vm_backup(vm_backup_path, esxi_name, vm_name)

    # Delete old backup files
    delete_old_backups(data_backup_path, 30)
    delete_old_backups(vm_backup_path, 30)

if __name__ == "__main__":
    base_path = "/ESXI 7/vmfs/"  # Replace with the actual path
    # Perform backup immediately
    main(base_path, 7)

    # Create backup schedule
    create_backup_schedule(base_path, 7)


# import os
# import datetime
# import subprocess
# import zipfile
# import schedule
# import time
# import random

# def create_backup_structure(base_path):
#     """Tạo cấu trúc thư mục backup."""
#     backup_path = os.path.join(base_path, "backup")
#     os.makedirs(backup_path, exist_ok=True)

#     # Tạo thư mục "Data Backup"
#     data_backup_path = os.path.join(backup_path, "Data Backup")
#     os.makedirs(data_backup_path, exist_ok=True)

#     # Tạo các thư mục con của "Data Backup"
#     folders = [
#         "Hệ thống ảo hóa",
#         "Ứng dụng kinh doanh",
#         "Ứng dụng nội bộ",
#         "Ứng dụng chuyên ngành",
#         "Phầm mềm hỗ trợ kỹ thuật",
#         "Others"
#     ]

#     for folder in folders:
#         os.makedirs(os.path.join(data_backup_path, folder), exist_ok=True)

#     # Tạo các thư mục con của "Ứng dụng kinh doanh"
#     business_app_path = os.path.join(data_backup_path, "Ứng dụng kinh doanh")
#     os.makedirs(os.path.join(business_app_path, "DBMS"), exist_ok=True)
#     os.makedirs(os.path.join(business_app_path, "ERP"), exist_ok=True)
#     os.makedirs(os.path.join(business_app_path, "CRM"), exist_ok=True)
#     os.makedirs(os.path.join(business_app_path, "Accounting"), exist_ok=True)
#     os.makedirs(os.path.join(business_app_path, "Email"), exist_ok=True)
#     os.makedirs(os.path.join(business_app_path, "Web"), exist_ok=True)

#     # Tạo các thư mục con của "Ứng dụng nội bộ"
#     internal_app_path = os.path.join(data_backup_path, "Ứng dụng nội bộ")
#     os.makedirs(os.path.join(internal_app_path, "HR"), exist_ok=True)
#     os.makedirs(os.path.join(internal_app_path, "Project Management"), exist_ok=True)
#     os.makedirs(os.path.join(internal_app_path, "Document Management"), exist_ok=True)
#     os.makedirs(os.path.join(internal_app_path, "Network"), exist_ok=True)
#     os.makedirs(os.path.join(internal_app_path, "Security"), exist_ok=True)

#     # Tạo thư mục "vm Backup"
#     vm_backup_path = os.path.join(backup_path, "vm Backup")
#     os.makedirs(vm_backup_path, exist_ok=True)

#     return data_backup_path, vm_backup_path

# def create_app_backup(app_path, backup_folder, app_name):
#     """Tạo file nén backup cho ứng dụng."""
#     today = datetime.date.today().strftime("%Y%m%d")
#     backup_filename = f"{today}_{app_name}_backup.tar.gz"
#     backup_file = os.path.join(backup_folder, backup_filename)
#     try:
#         subprocess.run(["tar", "-czvf", backup_file, app_path])
#         print(f"Đã backup ứng dụng: {app_name} vào {backup_file}")
#     except Exception as e:
#         print(f"Lỗi backup ứng dụng: {e}")

# def create_db_backup(db_path, backup_folder, db_name, db_type):
#     """Tạo file nén backup cho cơ sở dữ liệu."""
#     today = datetime.date.today().strftime("%Y%m%d")
#     backup_filename = f"{today}_{db_name}_backup.tar.gz"
#     backup_file = os.path.join(backup_folder, backup_filename)
#     try:
#         if db_type == "MySQL":
#             subprocess.run(["mysqldump", "-u", "username", "-p", "database_name", ">", backup_file])
#         elif db_type == "PostgreSQL":
#             subprocess.run(["pg_dump", "-h", "hostname", "-p", "port", "-U", "username", "database_name", ">", backup_file])
#         else:
#             print(f"Loại cơ sở dữ liệu {db_type} không được hỗ trợ.")
#         print(f"Đã backup cơ sở dữ liệu: {db_name} vào {backup_file}")
#     except Exception as e:
#         print(f"Lỗi backup cơ sở dữ liệu: {e}")

# def create_vm_backup(esxi_host, vm_name, backup_folder):
#     """Tạo file nén backup cho máy ảo."""
#     today = datetime.date.today().strftime("%Y%m%d")
#     vm_path = f"/vmfs/volumes/{esxi_host}/{vm_name}"
#     backup_filename = f"{today}_{vm_name}_backup.tar.gz"
#     backup_file = os.path.join(backup_folder, backup_filename)
#     try:
#         subprocess.run(["tar", "-czvf", backup_file, vm_path])
#         print(f"Đã backup máy ảo: {vm_name} trên {esxi_host} vào {backup_file}")
#     except Exception as e:
#         print(f"Lỗi backup máy ảo: {e}")

# def delete_old_backups(backup_path, days=7):
#     """Xóa các file backup cũ hơn `days` ngày."""
#     try:
#         for root, dirs, files in os.walk(backup_path):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 file_created_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
#                 if (datetime.datetime.now() - file_created_time).days > days:
#                     os.remove(file_path)
#                     print(f"Đã xóa file backup cũ: {file_path}")
#     except Exception as e:
#         print(f"Lỗi xóa backup: {e}")

# def create_backup_schedule(backup_path, days=7):
#     """Tạo lịch trình backup."""
#     schedule.every().day.at("00:00").do(lambda: main(backup_path, days))
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# def get_vms_from_esxi(esxi_host):
#     """Lấy danh sách các máy ảo trên ESXi."""
#     vms = []
#     try:
#         # Sử dụng lệnh 'vim-cmd' để lấy danh sách máy ảo
#         output = subprocess.check_output(["vim-cmd", "vimsvc", "/host:localhost", "getallvms"])
#         vms = [line.strip().split(' ')[1] for line in output.decode('utf-8').splitlines() if line.strip()]
#     except Exception as e:
#         print(f"Lỗi lấy danh sách máy ảo: {e}")
#     return vms

# def main(base_path, days=7):
#     """Hàm chính để thực hiện backup."""
#     data_backup_path, vm_backup_path = create_backup_structure(base_path)

#     # Backup hệ thống ảo hóa
#     virtualization_path = "/path/to/your/virtualization/system"  # Thay thế bằng đường dẫn thực tế
#     create_app_backup(virtualization_path, os.path.join(backup_path, "Hệ thống ảo hóa"), "vCenter")
#     virtualization_db_path = "/path/to/your/vCenter/database"  # Thay thế bằng đường dẫn thực tế
#     create_db_backup(virtualization_db_path, os.path.join(data_backup_path, "Hệ thống ảo hóa"), "vCenterDB", "MySQL")

#     # Backup các ứng dụng kinh doanh
#     business_app_path = os.path.join(data_backup_path, "Ứng dụng kinh doanh")
#     create_db_backup("/path/to/your/MySQL", os.path.join(business_app_path, "DBMS"), "MySQL", "MySQL")
#     create_db_backup("/path/to/your/PostgreSQL", os.path.join(business_app_path, "DBMS"), "PostgreSQL", "PostgreSQL")
#     create_db_backup("/path/to/your/Oracle", os.path.join(business_app_path, "DBMS"), "Oracle", "Oracle")
#     create_db_backup("/path/to/your/SQLServer", os.path.join(business_app_path, "DBMS"), "SQLServer", "SQLServer")


#     create_app_backup("/path/to/your/ERP", os.path.join(business_app_path, "ERP"), "ERPName")
#     create_app_backup("/path/to/your/CRM", os.path.join(business_app_path, "CRM"), "CRMName")
#     create_app_backup("/path/to/your/Accounting", os.path.join(business_app_path, "Accounting"), "AccountingName")
#     create_app_backup("/path/to/your/Email", os.path.join(business_app_path, "Email"), "EmailName")
#     create_app_backup("/path/to/your/Website", os.path.join(business_app_path, "Web"), "WebsiteName")

#     # Backup các ứng dụng nội bộ
#     internal_app_path = os.path.join(data_backup_path, "Ứng dụng nội bộ")
#     create_app_backup("/path/to/your/HR", os.path.join(internal_app_path, "HR"), "HRName")
#     create_app_backup("/path/to/your/ProjectManagement", os.path.join(internal_app_path, "Project Management"), "ProjectManagementName")
#     create_app_backup("/path/to/your/DocumentManagement", os.path.join(internal_app_path, "Document Management"), "DocumentManagementName")
#     create_app_backup("/path/to/your/Network", os.path.join(internal_app_path, "Network"), "NetworkName")
#     create_app_backup("/path/to/your/Security", os.path.join(internal_app_path, "Security"), "SecurityName")

#     # Backup các ứng dụng chuyên ngành
#     create_app_backup("/path/to/your/SpecializedApp", os.path.join(backup_path, "Ứng dụng chuyên ngành"), "SpecializedAppName")

#     # Backup các phần mềm hỗ trợ kỹ thuật
#     create_app_backup("/path/to/your/SupportSoftware", os.path.join(backup_path, "Phầm mềm hỗ trợ kỹ thuật"), "SupportSoftwareName")

#     # Backup các ứng dụng khác
#     create_app_backup("/path/to/your/OtherApp", os.path.join(backup_path, "Others"), "OtherAppName")

#     # Backup VM
#     # Danh sách các ESXi host
#     esxi_hosts = ["ESXi 1", "ESXi 2"] # Thay thế bằng danh sách ESXi host thực tế

#     for esxi_host in esxi_hosts:
#         # Tạo thư mục cho ESXi host
#         esxi_backup_path = os.path.join(vm_backup_path, esxi_host)
#         os.makedirs(esxi_backup_path, exist_ok=True)

#         # Lấy danh sách máy ảo trên ESXi host
#         vms = get_vms_from_esxi(esxi_host)

#         # Backup từng máy ảo
#         for vm in vms:
#             vm_backup_path = os.path.join(esxi_backup_path, vm)
#             os.makedirs(vm_backup_path, exist_ok=True)
#             create_vm_backup(esxi_host, vm, vm_backup_path)

#     delete_old_backups(data_backup_path, days)
#     delete_old_backups(vm_backup_path, days)

# if __name__ == "__main__":
#     base_path = "/path/to/your/backup/directory"  # Thay thế bằng đường dẫn thực tế
#     main(base_path, 7)

#     # Tạo lịch trình backup
#     create_backup_schedule(base_path, 7)
