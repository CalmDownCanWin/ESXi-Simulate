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

# def create_vm_backup_structure(vm_backup_path):
#     """Tạo cấu trúc thư mục cho vm Backup."""
#     esxi_hosts = ["ESXi 1", "ESXi 2"] # Thay thế bằng danh sách ESXi host thực tế
#     for esxi_host in esxi_hosts:
#         os.makedirs(os.path.join(vm_backup_path, esxi_host), exist_ok=True)

def create_app_backup(app_path, backup_folder, app_name):
    """Tạo file nén backup cho ứng dụng."""
    today = datetime.date.today().strftime("%Y%m%d")
    backup_filename = f"{today}_{app_name}_backup.tar.gz"
    backup_file = os.path.join(backup_folder, backup_filename)
    # # Tạo file giả mạo
    # fake_app_backup_file = os.path.join(backup_folder, f"{today}_{app_name}_backup.tar.gz")
    # create_fake_file(fake_app_backup_file, random.randint(10 * 1024 * 1024 * 1024, 100 * 1024 * 1024 * 1024)) 
    try:
        subprocess.run(["tar", "-czvf", backup_file, app_path])
        print(f"Đã backup ứng dụng: {app_name} vào {backup_file}")
         # Tạo file giả mạo
        fake_backup_file = os.path.join(backup_folder, f"{today}_{app_name}_backup.tar.gz")
        create_fake_file(fake_backup_file, random.randint(10 * 1024 * 1024 * 1024, 100 * 1024 * 1024 * 1024))  # 10GB to 100GB

    except Exception as e:
        print(f"Lỗi backup ứng dụng: {e}")

def create_db_backup(db_path, backup_folder, db_name):
    """Tạo file nén backup cho cơ sở dữ liệu."""
    today = datetime.date.today().strftime("%Y%m%d")
    backup_filename = f"{today}_{db_name}_backup.tar.gz"
    backup_file = os.path.join(backup_folder, backup_filename)
    # Tạo file giả mạo
    fake_backup_file = os.path.join(backup_folder, f"{today}_{db_name}_backup.tar.gz")
    create_fake_file(fake_backup_file, random.randint(10 * 1024 * 1024 * 1024, 100 * 1024 * 1024 * 1024))
    try:
        subprocess.run(["tar", "-czvf", backup_file, db_path])
        print(f"Đã backup cơ sở dữ liệu: {db_name} vào {backup_file}")
        #  # Tạo file giả mạo
        # fake_backup_file = os.path.join(backup_folder, f"{today}_{db_name}_backup_fake.tar.gz")
        # create_fake_file(fake_backup_file, random.randint(10 * 1024 * 1024 * 1024, 100 * 1024 * 1024 * 1024))  # 10GB to 100GB

    except Exception as e:
        print(f"Lỗi backup cơ sở dữ liệu: {e}")

def create_vm_backup(backup_path, esxi_name, vm_name):
    """Tạo file nén backup cho máy ảo."""
    today = datetime.date.today().strftime("%Y%m%d")
    backup_filename = f"{today}_{vm_name}_backup.tar.gz"
    backup_file = os.path.join(backup_path, esxi_name, vm_name, backup_filename)
    vm_path = f"/vmfs/volumes/{esxi_name}/{vm_name}"  # Thay thế bằng đường dẫn thực tế
    # # Tạo file giả mạo với kích thước lớn
    # create_fake_file(fake_backup_file, random.randint(10 * 1024 * 1024 * 1024, 100 * 1024 * 1024 * 1024))  # 10GB to 100GB
    # fake_backup_file = os.path.join(backup_path, esxi_name, vm_name, f"{today}_{vm_name}_backup.tar.gz")
    try:
        subprocess.run(["tar", "-czvf", backup_file, vm_path])
        print(f"Đã backup máy ảo: {vm_name} trên {esxi_name} vào {backup_file}")
        # Tạo file giả mạo với kích thước lớn
        fake_backup_file = os.path.join(backup_path, esxi_name, vm_name, f"{today}_{vm_name}_backup_fake.tar.gz")
        create_fake_file(fake_backup_file, random.randint(10 * 1024 * 1024 * 1024, 100 * 1024 * 1024 * 1024))  # 10GB to 100GB
    except Exception as e:
        print(f"Lỗi backup máy ảo: {e}")

def create_data_backup_for_vm(backup_path, esxi_name, vm_name, uuid):
    """Tạo file nén backup cho data của VM."""
    today = datetime.date.today().strftime("%Y%m%d")
    backup_filename = f"{today}_{vm_name}_DB_backup.tar.gz"
    backup_file = os.path.join(backup_path, esxi_name, vm_name, backup_filename)
    data_path = f"/vmfs/volumes/{esxi_name}/{uuid}"  # Thay thế bằng đường dẫn thực tế
    try:
        subprocess.run(["tar", "-czvf", backup_file, data_path])
        print(f"Đã backup data của VM: {vm_name} trên {esxi_name} vào {backup_file}")
    except Exception as e:
        print(f"Lỗi backup data VM: {e}")


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
        time.sleep(60)

def get_vms_from_esxi(esxi_host):
    """Lấy danh sách các máy ảo từ ESXI_UUIDS."""
    vms = []
    for uuid in ESXI_UUIDS[esxi_host]:
        vm_name = f"VM_{uuid}"  # Giả sử tên VM được tạo từ UUID
        vms.append(vm_name)
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
    create_db_backup(virtualization_db_path, os.path.join(data_backup_path, "Virtualization System"), "vCenterDB")
    # Backup các ứng dụng kinh doanh
    business_app_path = os.path.join(data_backup_path, "Business Applications")
    create_db_backup(data_backup_path, os.path.join(business_app_path, "DBMS"), "MySQL")
    create_db_backup(data_backup_path, os.path.join(business_app_path, "DBMS"), "PostgreSQL")
    create_db_backup(data_backup_path, os.path.join(business_app_path, "DBMS"), "Oracle")
    create_db_backup(data_backup_path, os.path.join(business_app_path, "DBMS"), "SQLServer")
    create_db_backup(data_backup_path, os.path.join(business_app_path, "ERP"), "ERPName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(data_backup_path, os.path.join(business_app_path, "CRM"), "CRMName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(data_backup_path, os.path.join(business_app_path, "Accounting"), "AccountingName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(data_backup_path, os.path.join(business_app_path, "Email"), "EmailName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(data_backup_path, os.path.join(business_app_path, "Web"), "WebsiteName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    # Backup các ứng dụng nội bộ
    internal_app_path = os.path.join(data_backup_path, "Internal Applications")
    create_db_backup(data_backup_path, os.path.join(internal_app_path, "HR"), "HRName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(data_backup_path, os.path.join(internal_app_path, "Project Management"), "ProjectManagementName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(data_backup_path, os.path.join(internal_app_path, "Document Management"), "DocumentManagementName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(data_backup_path, os.path.join(internal_app_path, "Network"), "NetworkName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    create_db_backup(data_backup_path, os.path.join(internal_app_path, "Security"), "SecurityName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    # Backup các ứng dụng chuyên ngành
    create_db_backup(data_backup_path, os.path.join(data_backup_path, "Specialized Applications"), "SpecializedAppName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    # Backup các phần mềm hỗ trợ kỹ thuật
    create_db_backup(data_backup_path, os.path.join(data_backup_path, "Technical Support Software"), "SupportSoftwareName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần
    # Backup các ứng dụng khác
    create_db_backup(data_backup_path, os.path.join(data_backup_path, "Others"), "OtherAppName_DB")  # Thay thế loại cơ sở dữ liệu nếu cần

    # Backup VM
    vm_backup_path = os.path.join(backup_path, "vm Backup")

    for esxi_host in ESXI_UUIDS:
        # Tạo thư mục cho ESXi host
        esxi_backup_path = os.path.join(vm_backup_path, esxi_host)
        os.makedirs(esxi_backup_path, exist_ok=True)

        # Lấy danh sách máy ảo trên ESXi host
        vms = get_vms_from_esxi(esxi_host)

        # Backup từng máy ảo
        for vm in vms:
            create_vm_backup(esxi_backup_path, esxi_host, vm)

            # Backup data của VM
            for uuid in ESXI_UUIDS[esxi_host]:
                create_data_backup_for_vm(data_backup_path, esxi_host, vm, ESXI_UUIDS[esxi_host][uuid])

    # Restore VM backup (one day before)
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    for esxi_host in ESXI_UUIDS:
        # Tạo thư mục cho ESXi host
        esxi_backup_path = os.path.join(vm_backup_path, esxi_host)
        # Lấy danh sách máy ảo trên ESXi host
        vms = get_vms_from_esxi(esxi_host)
        # Restore từng máy ảo
        for vm in vms:
            restore_vm_backup(esxi_backup_path, esxi_host, vm)

    delete_old_backups(app_backup_path, 30)
    delete_old_backups(data_backup_path, 30)
    delete_old_backups(vm_backup_path, 30)

if __name__ == "__main__":
    base_path = "/ESXI 7"  # Thay thế bằng đường dẫn thực tế
    main(base_path, 7)

    # Tạo lịch trình backup
    create_backup_schedule(base_path, 7)