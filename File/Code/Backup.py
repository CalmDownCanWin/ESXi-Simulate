# import os
# import datetime
# import zipfile

# from vmfs_1 import create_esx_vmfs

# def create_backup_structure(base_path):
#     """Tạo cấu trúc thư mục backup."""
#     backup_path = os.path.join(base_path, "backup")
#     os.makedirs(backup_path, exist_ok=True)
#     subfolders = ["App Backup", "DB Backup", "vm Backup"]
#     for folder in subfolders:
#         os.makedirs(os.path.join(backup_path, folder), exist_ok=True)
#     db_backup_path = os.path.join(backup_path, "DB Backup")
#     os.makedirs(os.path.join(db_backup_path, "DB_NAME"), exist_ok=True)
#     vm_backup_path = os.path.join(backup_path, "vm Backup")
#     os.makedirs(os.path.join(vm_backup_path, "VM_NAME"), exist_ok=True)
#     return backup_path

# def create_vm_backup(uuid_paths, vm_backup_path):
#     """Tạo file nén backup cho các UUID và lưu vào thư mục vm Backup."""
#     today = datetime.date.today().strftime("%Y%m%d")
#     for i, uuid_path in enumerate(uuid_paths):
#         backup_filename = f"{today}VMName_{i+1}.tar.gz"
#         backup_file = os.path.join(vm_backup_path, backup_filename)
#         # Sử dụng lệnh tar để nén thư mục (thay thế bằng zipfile nếu bạn muốn)
#         os.system(f"tar -czvf {backup_file} {uuid_path}")  

# if __name__ == "__main__":
#     base_path = "/ESXI 7/vmfs/volumes/Backup"# Thay thế bằng đường dẫn thực tế
#     esxi_choice = input("Chọn ESXi (ESXi_1, ESXi_2,...): ")
   
#     # Tạo cấu trúc ESXi và lấy đường dẫn đến các UUID cần backup
#     uuid_paths = create_esx_vmfs("/ESXI 7/", esxi_choice, create_windows=True, create_kali_ubuntu=True, print_uuids=True)

#     # Tạo cấu trúc thư mục backup
#     backup_path = create_backup_structure(base_path)

#     # Tạo file nén backup cho các UUID
#     vm_backup_path = os.path.join(backup_path, "vm Backup", "VM_NAME")
#     create_vm_backup(uuid_paths, vm_backup_path)



# import os
# import datetime
# import subprocess
# import zipfile
# import schedule
# import time

# def create_backup_structure(base_path):
#     """Tạo cấu trúc thư mục backup."""
#     backup_path = os.path.join(base_path, "backup")
#     os.makedirs(backup_path, exist_ok=True)
#     subfolders = ["App Backup", "DB Backup", "vm Backup"]
#     for folder in subfolders:
#         os.makedirs(os.path.join(backup_path, folder), exist_ok=True)
#     db_backup_path = os.path.join(backup_path, "DB Backup")
#     os.makedirs(os.path.join(db_backup_path, "DB_NAME"), exist_ok=True)
#     vm_backup_path = os.path.join(backup_path, "vm Backup")
#     os.makedirs(os.path.join(vm_backup_path, "VM_NAME"), exist_ok=True)
#     return backup_path

# def create_app_backup(app_backup_path):
#     """Tạo file nén backup cho ứng dụng web."""
#     today = datetime.date.today().strftime("%Y%m%d")
#     backup_filename = f"app_data_{today}.tar.gz"
#     backup_file = os.path.join(app_backup_path, backup_filename)
#     try:
#         # Tạo file nén
#         with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
#             # Duyệt qua thư mục ứng dụng web
#             for root, dirs, files in os.walk("/path/to/your/web/app"):
#                 for file in files:
#                     file_path = os.path.join(root, file)
#                     # Thêm file vào file nén
#                     zipf.write(file_path, os.path.relpath(file_path, "/path/to/your/web/app"))
#         print(f"Đã backup ứng dụng web vào {backup_file}")
#     except Exception as e:
#         print(f"Lỗi backup ứng dụng web: {e}")

# def create_db_backup(db_backup_path):
#     """Tạo file nén backup cho cơ sở dữ liệu MySQL."""
#     today = datetime.date.today().strftime("%Y%m%d")
#     backup_filename = f"db_backup_{today}.tar.gz"
#     backup_file = os.path.join(db_backup_path, backup_filename)
#     try:
#         # Tạo file nén
#         with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
#             # Duyệt qua thư mục cơ sở dữ liệu MySQL
#             for root, dirs, files in os.walk("/path/to/your/mysql/data"):
#                 for file in files:
#                     file_path = os.path.join(root, file)
#                     # Thêm file vào file nén
#                     zipf.write(file_path, os.path.relpath(file_path, "/path/to/your/mysql/data"))
#         print(f"Đã backup cơ sở dữ liệu MySQL vào {backup_file}")
#     except Exception as e:
#         print(f"Lỗi backup cơ sở dữ liệu MySQL: {e}")

# def create_vm_backup(vm_backup_path):
#     """Tạo file nén backup cho máy ảo Windows Server 2019."""
#     today = datetime.date.today().strftime("%Y%m%d")
#     backup_filename = f"{today}WinServer2019_.tar.gz"
#     backup_file = os.path.join(vm_backup_path, backup_filename)
#     try:
#         # Tạo file nén
#         with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
#             # Duyệt qua thư mục máy ảo Windows Server 2019
#             for root, dirs, files in os.walk("/path/to/your/vm/WinServer2019"):
#                 for file in files:
#                     file_path = os.path.join(root, file)
#                     # Thêm file vào file nén
#                     zipf.write(file_path, os.path.relpath(file_path, "/path/to/your/vm/WinServer2019"))
#         print(f"Đã backup máy ảo Windows Server 2019 vào {backup_file}")
#     except Exception as e:
#         print(f"Lỗi backup máy ảo Windows Server 2019: {e}")

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

# def restore_app_backup(app_backup_path):
#     """Restore dữ liệu từ file backup của ứng dụng web."""
#     today = datetime.date.today().strftime("%Y%m%d")
#     backup_file = os.path.join(app_backup_path, f"app_data_{today}.tar.gz")
#     try:
#         # Giải nén file backup
#         with zipfile.ZipFile(backup_file, 'r') as zipf:
#             zipf.extractall("/path/to/your/web/app")
#         print(f"Đã restore ứng dụng web từ file: {backup_file}")
#     except Exception as e:
#         print(f"Lỗi restore ứng dụng web: {e}")

# def restore_db_backup(db_backup_path):
#     """Restore dữ liệu từ file backup của cơ sở dữ liệu MySQL."""
#     today = datetime.date.today().strftime("%Y%m%d")
#     backup_file = os.path.join(db_backup_path, f"db_backup_{today}.tar.gz")
#     try:
#         # Giải nén file backup
#         with zipfile.ZipFile(backup_file, 'r') as zipf:
#             zipf.extractall("/path/to/your/mysql/data")
#         print(f"Đã restore cơ sở dữ liệu MySQL từ file: {backup_file}")
#     except Exception as e:
#         print(f"Lỗi restore cơ sở dữ liệu MySQL: {e}")

# def restore_vm_backup(vm_backup_path):
#     """Restore dữ liệu từ file backup của máy ảo Windows Server 2019."""
#     today = datetime.date.today().strftime("%Y%m%d")
#     backup_file = os.path.join(vm_backup_path, f"{today}WinServer2019_.tar.gz")
#     try:
#         # Giải nén file backup
#         with zipfile.ZipFile(backup_file, 'r') as zipf:
#             zipf.extractall("/path/to/your/vm/WinServer2019")
#         print(f"Đã restore máy ảo Windows Server 2019 từ file: {backup_file}")
#     except Exception as e:
#         print(f"Lỗi restore máy ảo Windows Server 2019: {e}")

# def main(base_path, days=7):
#     """Hàm chính để thực hiện backup."""
#     backup_path = create_backup_structure(base_path)
#     app_backup_path = os.path.join(backup_path, "App Backup")
#     db_backup_path = os.path.join(backup_path, "DB Backup", "DB_NAME")
#     vm_backup_path = os.path.join(backup_path, "vm Backup", "VM_NAME")
    
#     create_app_backup(app_backup_path)
#     create_db_backup(db_backup_path)
#     create_vm_backup(vm_backup_path)
#     delete_old_backups(backup_path, days)

#     # Thực hiện restore (thêm vào nếu cần)
#     restore_app_backup(app_backup_path)
#     restore_db_backup(db_backup_path)
#     restore_vm_backup(vm_backup_path)

# def create_backup_schedule(backup_path, days=7):
#     """Tạo lịch trình backup."""
#     schedule.every(days).days.at("00:00").do(lambda: main(backup_path, days))
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# if __name__ == "__main__":
#     base_path = "/path/to/your/backup/folder"
#     # Thực hiện backup ngay lập tức
#     main(base_path, 7)

#     # Tạo lịch trình backup
#     create_backup_schedule(base_path, 7)


import os
import datetime
import subprocess
import schedule
import time
import random

#  Import from ESXI_config.py
from ESXi_config import create_fake_file 

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
    create_vm_backup_structure(vm_backup_path)

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

def create_vm_backup_structure(vm_backup_path):
    """Tạo cấu trúc thư mục cho vm Backup."""
    esxi_hosts = ["ESXi 1", "ESXi 2"] # Thay thế bằng danh sách ESXi host thực tế
    for esxi_host in esxi_hosts:
        os.makedirs(os.path.join(vm_backup_path, esxi_host), exist_ok=True)

def create_app_backup(app_path, backup_folder, app_name):
    """Tạo file nén backup cho ứng dụng."""
    today = datetime.date.today().strftime("%Y%m%d")
    backup_filename = f"{today}_{app_name}_backup.tar.gz"
    backup_file = os.path.join(backup_folder, backup_filename)
    try:
        subprocess.run(["tar", "-czvf", backup_file, app_path])
        print(f"Đã backup ứng dụng: {app_name} vào {backup_file}")
    except Exception as e:
        print(f"Lỗi backup ứng dụng: {e}")

def create_db_backup(db_path, backup_folder, db_name, db_type):
    """Tạo file nén backup cho cơ sở dữ liệu."""
    today = datetime.date.today().strftime("%Y%m%d")
    backup_filename = f"{today}_{db_name}_backup.tar.gz"
    backup_file = os.path.join(backup_folder, backup_filename)
    try:
        if db_type == "MySQL":
            subprocess.run(["mysqldump", "-u", "username", "-p", "database_name", ">", backup_file])
        elif db_type == "PostgreSQL":
            subprocess.run(["pg_dump", "-h", "hostname", "-p", "port", "-U", "username", "database_name", ">", backup_file])
        else:
            print(f"Database type {db_type} not supported.")
        print(f"Đã backup cơ sở dữ liệu: {db_name} vào {backup_file}")
    except Exception as e:
        print(f"Lỗi backup cơ sở dữ liệu: {e}")

def create_vm_backup(backup_path, esxi_name, vm_name):
    """Tạo file nén backup cho máy ảo."""
    today = datetime.date.today().strftime("%Y%m%d")
    backup_filename = f"{today}_{vm_name}_backup.tar.gz"
    backup_file = os.path.join(backup_path, esxi_name, vm_name, backup_filename)
    vm_path = f"/vmfs/volumes/{esxi_name}/{vm_name}"  # Thay thế bằng đường dẫn thực tế
    try:
        subprocess.run(["tar", "-czvf", backup_file, vm_path])
        print(f"Đã backup máy ảo: {vm_name} trên {esxi_name} vào {backup_file}")

        # Tạo file giả mạo với kích thước lớn
        fake_backup_file = os.path.join(backup_path, esxi_name, vm_name, f"{today}_{vm_name}_backup_fake.tar.gz")
        create_fake_file(fake_backup_file, random.randint(10 * 1024 * 1024 * 1024, 100 * 1024 * 1024 * 1024))  # 10GB to 100GB
    except Exception as e:
        print(f"Lỗi backup máy ảo: {e}")

def delete_old_backups(backup_path, days=7):
    """Xóa các file backup cũ hơn `days` ngày."""
    try:
        for root, dirs, files in os.walk(backup_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_created_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
                if (datetime.datetime.now() - file_created_time).days > days:
                    os.remove(file_path)
                    print(f"Đã xóa file backup cũ: {file_path}")
    except Exception as e:
        print(f"Lỗi xóa backup: {e}")

def create_backup_schedule(backup_path, days=7):
    """Tạo lịch trình backup."""
    schedule.every().day.at("00:00").do(lambda: main(backup_path, days))
    while True:
        schedule.run_pending()
        time.sleep(1)

def get_vms_from_esxi(esxi_host):
    """Lấy danh sách các máy ảo trên ESXi."""
    vms = []
    try:
        # Sử dụng lệnh 'vim-cmd' để lấy danh sách máy ảo
        output = subprocess.check_output(["vim-cmd", "vimsvc", "/host:localhost", "getallvms"])
        vms = [line.strip().split(' ')[1] for line in output.decode('utf-8').splitlines() if line.strip()]
    except Exception as e:
        print(f"Lỗi lấy danh sách máy ảo: {e}")
    return vms

def restore_vm_backup(backup_path, esxi_host, vm_name):
    """Khôi phục backup máy ảo."""
    today = datetime.date.today().strftime("%Y%m%d")
    backup_file = os.path.join(backup_path, esxi_host, vm_name, f"{today}_{vm_name}_backup.tar.gz")
    vm_path = f"/vmfs/volumes/{esxi_host}/{vm_name}"  # Thay thế bằng đường dẫn thực tế
    try:
        subprocess.run(["tar", "-xzvf", backup_file, "-C", vm_path])
        print(f"Đã khôi phục backup máy ảo: {vm_name} trên {esxi_host} từ {backup_file}")
    except Exception as e:
        print(f"Lỗi khôi phục backup máy ảo: {e}")

def main(base_path, days=7):
    """Hàm chính để thực hiện backup."""
    backup_path = create_backup_structure(base_path)

    # Backup App
    app_backup_path = os.path.join(backup_path, "App Backup")
    # Backup hệ thống ảo hóa
    virtualization_path = os.path.join(app_backup_path,"Virtualization System")  # Thay thế bằng đường dẫn thực tế
    create_app_backup(virtualization_path, os.path.join(app_backup_path, "Virtualization System"), "vCenter")
    # Backup các ứng dụng kinh doanh
    business_app_path = os.path.join(app_backup_path, "Business Applications")
    create_app_backup(business_app_path, os.path.join(business_app_path, "DBMS"), "DBMSName")
    create_app_backup(business_app_path, os.path.join(business_app_path, "ERP"), "ERPName")
    create_app_backup(business_app_path, os.path.join(business_app_path, "CRM"), "CRMName")
    create_app_backup(business_app_path, os.path.join(business_app_path, "Accounting"), "AccountingName")
    create_app_backup(business_app_path, os.path.join(business_app_path, "Email"), "EmailName")
    create_app_backup(business_app_path, os.path.join(business_app_path, "Web"), "WebsiteName")
    # Backup các ứng dụng nội bộ
    internal_app_path = os.path.join(app_backup_path, "Internal Applications")
    create_app_backup(business_app_path, os.path.join(internal_app_path, "HR"), "HRName")
    create_app_backup(business_app_path, os.path.join(internal_app_path, "Project Management"), "ProjectManagementName")
    create_app_backup(business_app_path, os.path.join(internal_app_path, "Document Management"), "DocumentManagementName")
    create_app_backup(business_app_path, os.path.join(internal_app_path, "Network"), "NetworkName")
    create_app_backup(business_app_path, os.path.join(internal_app_path, "Security"), "SecurityName")
    # Backup các ứng dụng chuyên ngành
    create_app_backup(business_app_path, os.path.join(app_backup_path, "Specialized Applications"), "SpecializedAppName")
    # Backup các phần mềm hỗ trợ kỹ thuật
    create_app_backup(business_app_path, os.path.join(app_backup_path, "Technical Support Software"), "SupportSoftwareName")
    # Backup các ứng dụng khác
    create_app_backup(business_app_path, os.path.join(app_backup_path, "Others"), "OtherAppName")

    # Backup Data
    data_backup_path = os.path.join(backup_path, "Data Backup")
    # Backup hệ thống ảo hóa
    virtualization_db_path = os.path.join(data_backup_path,"Virtualization System")  # Thay thế bằng đường dẫn thực tế
    create_db_backup(virtualization_db_path, os.path.join(data_backup_path, "Virtualization System"), "vCenterDB", "MySQL")
    # Backup các ứng dụng kinh doanh
    business_app_path = os.path.join(data_backup_path, "Business Applications")
    create_db_backup("/path/to/your/MySQL", os.path.join(business_app_path, "DBMS"), "MySQL", "MySQL")
    create_db_backup("/path/to/your/PostgreSQL", os.path.join(business_app_path, "DBMS"), "PostgreSQL", "PostgreSQL")
    create_db_backup("/path/to/your/Oracle", os.path.join(business_app_path, "DBMS"), "Oracle", "Oracle")
    create_db_backup("/path/to/your/SQLServer", os.path.join(business_app_path, "DBMS"), "SQLServer", "SQLServer")
    create_db_backup("/path/to/your/ERP_DB", os.path.join(business_app_path, "ERP"), "ERPName_DB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup("/path/to/your/CRM_DB", os.path.join(business_app_path, "CRM"), "CRMName_DB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup("/path/to/your/Accounting_DB", os.path.join(business_app_path, "Accounting"), "AccountingName_DB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup("/path/to/your/Email_DB", os.path.join(business_app_path, "Email"), "EmailName_DB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup("/path/to/your/Website_DB", os.path.join(business_app_path, "Web"), "WebsiteName_DB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần
    # Backup các ứng dụng nội bộ
    internal_app_path = os.path.join(data_backup_path, "Internal Applications")
    create_db_backup("/path/to/your/HR_DB", os.path.join(internal_app_path, "HR"), "HRName_DB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup("/path/to/your/ProjectManagement_DB", os.path.join(internal_app_path, "Project Management"), "ProjectManagementName_DB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup("/path/to/your/DocumentManagement_DB", os.path.join(internal_app_path, "Document Management"), "DocumentManagementName_DB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup("/path/to/your/Network_DB", os.path.join(internal_app_path, "Network"), "NetworkName_DB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup("/path/to/your/Security_DB", os.path.join(internal_app_path, "Security"), "SecurityName_DB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần
    # Backup các ứng dụng chuyên ngành
    create_db_backup("/path/to/your/SpecializedApp_DB", os.path.join(data_backup_path, "Specialized Applications"), "SpecializedAppName_DB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần
    # Backup các phần mềm hỗ trợ kỹ thuật
    create_db_backup("/path/to/your/SupportSoftware_DB", os.path.join(data_backup_path, "Technical Support Software"), "SupportSoftwareName_DB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần
    # Backup các ứng dụng khác
    create_db_backup("/path/to/your/OtherApp_DB", os.path.join(data_backup_path, "Others"), "OtherAppName_DB", "MySQL")  # Thay thế loại cơ sở dữ liệu nếu cần

    # Backup VM
    vm_backup_path = os.path.join(backup_path, "vm Backup")
    # Danh sách các ESXi host
    esxi_hosts = ["ESXi 1", "ESXi 2"] # Thay thế bằng danh sách ESXi host thực tế

    for esxi_host in esxi_hosts:
        # Tạo thư mục cho ESXi host
        esxi_backup_path = os.path.join(vm_backup_path, esxi_host)
        os.makedirs(esxi_backup_path, exist_ok=True)

        # Lấy danh sách máy ảo trên ESXi host
        vms = get_vms_from_esxi(esxi_host)

        # Backup từng máy ảo
        for vm in vms:
            create_vm_backup(esxi_backup_path, esxi_host, vm)

    # Restore VM backup (one day before)
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    for esxi_host in esxi_hosts:
        # Tạo thư mục cho ESXi host
        esxi_backup_path = os.path.join(vm_backup_path, esxi_host)
        # Lấy danh sách máy ảo trên ESXi host
        vms = get_vms_from_esxi(esxi_host)
        # Restore từng máy ảo
        for vm in vms:
            restore_vm_backup(esxi_backup_path, esxi_host, vm)

    delete_old_backups(app_backup_path, days)
    delete_old_backups(data_backup_path, days)
    delete_old_backups(vm_backup_path, days)

if __name__ == "__main__":
    base_path = "/ESXI 7/"  # Thay thế bằng đường dẫn thực tế
    main(base_path, 7)

    # Tạo lịch trình backup
    create_backup_schedule(base_path, 7)