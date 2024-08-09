import os
import datetime
import subprocess
import schedule
import time
import random

#  Import from ESXI_config.py
from ESXi_config import create_fake_file 
from vmfs import ESXI_UUIDS

def create_backup_structure(base_path):
    """Create backup directory structure."""
    backup_path = os.path.join(base_path, "backup")
    os.makedirs(backup_path, exist_ok=True)

    # Create subfolders
    folders = [
        "App Backup",
        "Data Backup",
        "vm Backup"
    ]

    for folder in folders:
        os.makedirs(os.path.join(backup_path, folder), exist_ok=True)

    # Create a structure for App Backup
    app_backup_path = os.path.join(backup_path, "App Backup")
    create_app_backup_structure(app_backup_path)

    # Create a structure for Data Backup
    data_backup_path = os.path.join(backup_path, "Data Backup")
    create_data_backup_structure(data_backup_path)

    return backup_path

def create_app_backup_structure(app_backup_path):
    """Create a folder structure for the Backup app."""
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
    """Create a folder structure for Data Backup."""
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
    """Create a backup file for the application."""
    for i in range(4):
        backup_date = (datetime.date.today() - datetime.timedelta(days=2)- datetime.timedelta(days=i*7)).strftime("%Y%m%d")
        backup_filename = f"{backup_date}_{app_name}_backup.tar.gz"
        backup_file = os.path.join(backup_folder, backup_filename)
        # # Create a fake file
        create_fake_file(backup_file, random.randint(10 * 1024 * 1024 * 1024, 30 * 1024 * 1024 * 1024))
    print(f"Backup database: {app_name} vào {backup_file}")

def create_db_backup(backup_folder, db_name):
    """Create a backup file for the database."""
    for i in range(4):
        backup_date = (datetime.date.today() - datetime.timedelta(days=2)- datetime.timedelta(days=i*7)).strftime("%Y%m%d")
        backup_filename = f"{backup_date}_{db_name}_backup.tar.gz"
        backup_file = os.path.join(backup_folder, backup_filename)
         # Create a fake file
        create_fake_file(backup_file, random.randint(20 * 1024 * 1024 * 1024, 40 * 1024 * 1024 * 1024))

    print(f"Backup database: {db_name} vào {backup_file}")

def create_vm_backup(backup_path, vm_name, uuid, backup_date):
    """Create a backup file for VM (fake capacity)."""
    for i in range(4):
        backup_date = (datetime.date.today() - datetime.timedelta(days=2)- datetime.timedelta(days=i*7)).strftime("%Y%m%d")
        backup_filename = f"{backup_date}_{vm_name}_backup.tar.gz"
        backup_file = os.path.join(backup_path, backup_filename)
    	# Create a fake backup file
        fake_backup_size = random.randint(20 * 1024 * 1024 * 1024, 30 * 1024 * 1024 * 1024)
        create_fake_file(backup_file, fake_backup_size)  # Create file with fake size
    
    print(f"Backup VM: {vm_name} up {backup_file} (Capacity of fake)")
        
def find_and_backup_vm(backup_path, vm_name, uuid, backup_date):
    """Find VM and create a Backup compressed file."""
    vm_path = os.path.join(backup_path,"vmfs","volumes", uuid, vm_name)
    if os.path.isdir(vm_path):
        create_vm_backup(backup_path,  vm_name, uuid, backup_date)

def delete_old_backups(backup_path):
    """Delete old backup files over 30 days."""
    for filename in os.listdir(backup_path):
        file_path = os.path.join(backup_path, filename)
        #Check if the file_path is a file and has a compressed file or not
        if os.path.isfile(file_path) and filename.endswith((".tar.gz", ".zip", ".7z")):  
            try:
                #Take time to create file
                creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
                # Check the creation time is greater than 30 days
                if (datetime.datetime.now() - creation_time).days > 30:
                    # Xóa file
                    os.remove(file_path)
                    print(f"Delete old backup file: {file_path}")
            except Exception as e:
                print(f"Error of deleting backup file: {e}")


def create_backup_schedule(backup_path, days=7):
    """Create a backup schedule."""
    schedule.every().day.at("00:00").do(lambda: Backup(backup_path, days))
    while True:
        schedule.run_pending()
        time.sleep(1)

def Backup(base_path, days=7):
    """The main function to perform the backup."""
    backup_path = create_backup_structure(base_path)

    # Backup App
    app_backup_path = os.path.join(backup_path, "App Backup")
    # Backup virtualization system
    create_app_backup(os.path.join(app_backup_path, "Virtualization System"), "vCenter")
    # Backup of business applications
    business_app_path = os.path.join(app_backup_path, "Business Applications")
    create_app_backup( os.path.join(business_app_path, "DBMS"), "DBMSName")
    create_app_backup( os.path.join(business_app_path, "ERP"), "ERPName")
    create_app_backup( os.path.join(business_app_path, "CRM"), "CRMName")
    create_app_backup( os.path.join(business_app_path, "Accounting"), "AccountingName")
    create_app_backup( os.path.join(business_app_path, "Email"), "EmailName")
    create_app_backup( os.path.join(business_app_path, "Web"), "WebsiteName")
    # Backup internal applications
    internal_app_path = os.path.join(app_backup_path, "Internal Applications")
    create_app_backup( os.path.join(internal_app_path, "HR"), "HRName")
    create_app_backup( os.path.join(internal_app_path, "Project Management"), "ProjectManagementName")
    create_app_backup( os.path.join(internal_app_path, "Document Management"), "DocumentManagementName")
    create_app_backup( os.path.join(internal_app_path, "Network"), "NetworkName")
    create_app_backup( os.path.join(internal_app_path, "Security"), "SecurityName")
    # Backup specialized applications
    create_app_backup( os.path.join(app_backup_path, "Specialized Applications"), "SpecializedAppName")
    # Backup technical support software
    create_app_backup( os.path.join(app_backup_path, "Technical Support Software"), "SupportSoftwareName")
    # Backup other applications
    create_app_backup( os.path.join(app_backup_path, "Others"), "OtherAppName")

    # Backup Data
    data_backup_path = os.path.join(backup_path, "Data Backup")
    #Backup virtualization system
    create_db_backup(os.path.join(data_backup_path, "Virtualization System"), "vCenterDB")
    # Backup of business applications
    business_app_path = os.path.join(data_backup_path, "Business Applications")
    create_db_backup(os.path.join(business_app_path, "DBMS"), "MySQL")
    create_db_backup(os.path.join(business_app_path, "DBMS"), "PostgreSQL")
    create_db_backup(os.path.join(business_app_path, "DBMS"), "Oracle")
    create_db_backup(os.path.join(business_app_path, "DBMS"), "SQLServer")
    create_db_backup(os.path.join(business_app_path, "ERP"), "ERPName_DB")  # Replace the type of database if needed
    create_db_backup(os.path.join(business_app_path, "CRM"), "CRMName_DB")  # Replace the type of database if needed
    create_db_backup(os.path.join(business_app_path, "Accounting"), "AccountingName_DB")  # Replace the type of database if needed
    create_db_backup(os.path.join(business_app_path, "Email"), "EmailName_DB")  # Replace the type of database if needed
    create_db_backup(os.path.join(business_app_path, "Web"), "WebsiteName_DB")  # Replace the type of database if needed
    # Backup internal applications
    internal_app_path = os.path.join(data_backup_path, "Internal Applications")
    create_db_backup(os.path.join(internal_app_path, "HR"), "HRName_DB")  # Replace the type of database if needed
    create_db_backup(os.path.join(internal_app_path, "Project Management"), "ProjectManagementName_DB")  # Replace the type of database if needed
    create_db_backup(os.path.join(internal_app_path, "Document Management"), "DocumentManagementName_DB")  # Replace the type of database if needed
    create_db_backup(os.path.join(internal_app_path, "Network"), "NetworkName_DB")  # Replace the type of database if needed
    create_db_backup(os.path.join(internal_app_path, "Security"), "SecurityName_DB")  # Replace the type of database if needed
    # Backup specialized applications
    create_db_backup(os.path.join(data_backup_path, "Specialized Applications"), "SpecializedAppName_DB")  # Replace the type of database if needed
    # Backup technical support software
    create_db_backup(os.path.join(data_backup_path, "Technical Support Software"), "SupportSoftwareName_DB")  # Replace the type of database if needed
    # Backup other applications
    create_db_backup(os.path.join(data_backup_path, "Others"), "OtherAppName_DB")  # Replace the type of database if needed

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
        # Check if there is any VM in this Esxi Host
        has_vm = False
        for uuid_key in ESXI_UUIDS[esxi_host]:
            if uuid_key.startswith("UUID"):
                uuid = ESXI_UUIDS[esxi_host][uuid_key]
                for vm_name in VM:
                    vm_path = os.path.join(backup_path,"vmfs","volumes", uuid, vm_name)
                    if os.path.isdir(vm_path):
                        has_vm = True
                        break
                if has_vm:
                    break

        if has_vm:
            # Create folders for ESXI Host
            esxi_backup_path = os.path.join(vm_backup_path, esxi_host)
            os.makedirs(esxi_backup_path, exist_ok=True)

            # Browse through VM
            for vm_name in VM:
                # Browse through the uuid key in eSxi_uuids [Esxi_host]
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

