import os
import random
import stat
import subprocess
import datetime

from ESXi_config import create_config_file
from ESXi_config import create_vmdk_file
from ESXi_config import create_flat_vmdk
from ESXi_config import create_log_file
from ESXi_config import generate_random_string
from ESXi_config import create_fake_file
# from ESXi_config import create_symlinks
from ESXi_config import create_directory

# Definition of Uuid configuration and link for each ESXI
ESXI_UUIDS = {
    "ESXi_1": {
        "UUID1": "486b39d0-3b4db665-e593-83a193fc5192",  # Change UUID1
        "UUID2": "6673e14e-8e17af66-4ae8-000c299cb5ed",  # Change UUID2
        "UUID3": "669d1bdb-d91fa63f-ef8b-000c299cb5ed",  # Change UUID3
        "UUID4": "669d1bfa-fc27fe78-39a3-000c299cb5ed",  # Change UUID4
        "UUID5": "6676885b-da7c8fb4-8ca7-000c299cb5ed",  # Change UUID5
        "UUID6": "f9d5c73b-6342cf19-18aa-76fbe3100cb8",  # Change UUID6
    },
    "ESXi_2": {
        "UUID1": "486b-708e3598436286a4adde-c5192",
        "UUID2": "6676-8300117f4e12aaff50c1-cb5ed",
        "UUID3": "669d-fe4cb16245ce99f245b9-cb5ed",
        "UUID6": "f9d5-e05d79ff40feb05b9d42-0cb8",
    },
    "ESXi_3": {
        "UUID1": "e79016ab-fa46ca36-a6a0-db9dd4db1000",
        "UUID2": "731b6b79-b7432603-9eaa-1eb25ea07ab5",
        "UUID3": "6698bca7-8d3ba4c8-2d63-000c290cc9ff",
        "UUID4": "6696448c-5885-4c7f-8fc3-000c290cc9ff",
        "UUID6": "6696448c-599fcf6f-fd9b-000c290cc9ff",
    },
    "ESXi_4": {
        "UUID1": "3270b94c-cbc3-4e32-be2d-20b4afacaedd",
        "UUID2": "52871857-a0aa-4970-8220-14442ad2c6fc",
        "UUID3": "54b1d0f3-be6d-4c53-9d70-52a5d004d291",
        "UUID4": "54b1b94c-cbc3-4e32-be2d-20b4afacd291",
        "UUID6": "f574f01f-5885-4c7f-8fc3-a2a509f6b39c",
    },
    "ESXi_5": {
        "UUID1": "34edc64f-87a1-42b9-bdc3-8080bcb83552",
        "UUID2": "785b7424-be6d-45f1-8823-69fc5011098a",
        "UUID3": "63a570c0-a082-4a04-9d61-7f9dd4311340",
        "UUID6": "c44033d8-ea55-440d-b2af-4a78d36af04e",
    },
}

def create_esx_vmfs(base_path, esxi_name, create_windows=True, create_kali_ubuntu=True,create_FreeBSD=True,create_window_server=True,create_MacOS=True,create_Kali_Centos=True, print_uuids=True):
    """Create an ESXI simulation folder structure with separate uuid and configuration options."""

    # Get Uuid configuration and link for specific ESXI
    esxi_config = ESXI_UUIDS.get(esxi_name)
    if not esxi_config:
        print(f"Error: No configuration for ESXI '{esxi_name}'.")
        return

    # Definition Symlink depends on the name ESXI
    if esxi_name == "ESXi_1":
        esxi_config["SYMLINKS"] = {
            "BOOTBANK1": esxi_config["UUID1"],
            "BOOTBANK2": esxi_config["UUID6"],
            "DevOpsDataStore": esxi_config["UUID3"],  # Change name DataStore cho ESXi_1
            "SREDataStore": esxi_config["UUID4"],  # Change name DataStore cho ESXi_1
            "TeamDataStore": esxi_config["UUID5"],  # Change name DataStore cho ESXi_1
            f"OSDATA-{esxi_config['UUID2']}": esxi_config["UUID2"],
        }
    elif esxi_name == "ESXi_2":
        esxi_config["SYMLINKS"] = {
            "BOOTBANK1": esxi_config["UUID1"],
            "BOOTBANK2": esxi_config["UUID6"],
            "ProjectDataStore": esxi_config["UUID3"],  # Change name DataStore cho ESXi_2
            f"OSDATA-{esxi_config['UUID2']}": esxi_config["UUID2"],
        }
    elif esxi_name == "ESXi_3":
        esxi_config["SYMLINKS"] = {
            "BOOTBANK1": esxi_config["UUID1"],
            "BOOTBANK2": esxi_config["UUID6"],
            "DataCenter": esxi_config["UUID3"],  # Change name DataStore cho ESXi_3
            "DataHub": esxi_config["UUID4"],  # Change name DataStore cho ESXi_3
            f"OSDATA-{esxi_config['UUID2']}": esxi_config["UUID2"],
        }
    elif esxi_name == "ESXi_4":
        esxi_config["SYMLINKS"] = {
            "BOOTBANK1": esxi_config["UUID1"],
            "BOOTBANK2": esxi_config["UUID6"],
            "ProjectAlphaDataStore": esxi_config["UUID3"],  # Change name DataStore cho ESXi_4
            "BetaCluster": esxi_config["UUID4"],  # Change name DataStore cho ESXi_4
            f"OSDATA-{esxi_config['UUID2']}": esxi_config["UUID2"],
        }
    elif esxi_name == "ESXi_5":
        esxi_config["SYMLINKS"] = {
            "BOOTBANK1": esxi_config["UUID1"],
            "BOOTBANK2": esxi_config["UUID6"],
            "ProductionDataStore": esxi_config["UUID3"],  # Change name DataStore cho ESXi_5
            f"OSDATA-{esxi_config['UUID2']}": esxi_config["UUID2"],
        }
    else:
        print(f"Error: No support for ESXI '{esxi_name}'.")
        return

    # Folder vmfs
    vmfs_path = os.path.join(base_path, "vmfs")
    os.makedirs(vmfs_path, exist_ok=True)

    # Folder vmfs/volumes
    volumes_path = os.path.join(vmfs_path, "volumes")
    os.makedirs(volumes_path, exist_ok=True)

    create_config_file(vmfs_path,"devices",generate_random_string(10))

    # device_symlinks = {"devices": "/dev/"}
    # create_symlinks(vmfs_path,device_symlinks)

    # Create Folder cho các UUID
    for uuid_name, uuid_str in esxi_config.items():
        if uuid_name.startswith("UUID"):
            uuid_path = os.path.join(volumes_path, uuid_str)
            os.makedirs(uuid_path, exist_ok=True)
            
            # Set permission for UUID folder
            os.chmod(uuid_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

            # Add custom file/folder to each uuid
            if uuid_name == "UUID1":
                bootbank1_files = {
                    "atlantic.v00": 1414,
                    "basemisc.tgz": 11430,
                    "bnxtnet.v00": 919,
                    "brcmfcoe.v00": 2227,
                    "crx.v00": 2227,
                    "elxnet.v00": 2227,
                    "i40en.v00": 2227,
                    "icen.v00": 2227,
                    "igbn.v00": 2227,
                    "imgdb.tgz": 2227,
                    "ionic_en.v00": 2227,
                    "iser.v00": 2227,
                    "ixgben.v00": 2227,
                    "lsi_mr3.v00": 2227,
                    "lsi_msgp.v00": 2227,
                    "lsi_msgp.v01": 2227,
                    "lsi_msgp.v02": 2227,
                    "lsuv2_hp.v00": 2227,
                    "lsuv2_in.v00": 2227,
                    "lsuv2_ls.v00": 2227,
                    "lsuv2_nv.v00": 2227,
                    "lsuv2_oe.v00": 2227,
                    "ionic_en.v01": 2227,
                    "ionic_en.v02": 2227,
                    "nmlx4_co.v00": 2227,
                    "nmlx4_en.v00": 2227,
                    "elx_esx_.v00": 2317,
                    "elxiscsi.v00": 565,
                    "esx_ui.v00": 22641,
                    "esxupdt.v00": 2292,
                    "iavmd.v00": 742,
                    "gc.v00": 1024,
                    "irdman.v00": 1024,
                    "loadesx.v00": 3586,
                    "lpfc.v00": 3009,
                    "lpnic.v00": 635,
                    "vmkata.v00": 163431,
                    "vmkata.v00": 202,
                    "vmw_ahci.v00": 348,
                    "vmware_e.v00": 199,
                    "vmx.v00": 122337,
                    "vsan.v00": 41470,
                    "vsanheal.v00": 8356,
                    "vsanmgmt.v00": 26437,
                    "weaselin.v00": 2701,
                    "xorg.v00": 3438,
                }
                for filename, size in bootbank1_files.items():
                    create_config_file(uuid_path, filename, generate_random_string(size))
            elif uuid_name == "UUID2":
                file = {
                    ".fbb.sf",
                    ".fdc.sf",
                    ".jbc.sf",
                    ".pb2.sf",
                    ".pbc.sf",  
                    ".sbc.sf",  
                    ".vh.sf",  
                }
                for filen in file:
                    create_config_file(uuid_path,filen,generate_random_string(12))
                create_directory(os.path.join(uuid_path,".sdd.sf"))

                UUID2_Folder = {
                    "cache",
                    "core",
                    "downloads",
                    "store",
                    "tmp",
                    "healthd",
                    "locker",
                    "var",
                    "vdtc",
                    "vmkdump",
                    "vmware",
                }
                for uuidn in UUID2_Folder:
                    create_directory(os.path.join(uuid_path,uuidn))

            elif uuid_name == "UUID6":
                create_config_file(uuid_path, "boot.cfg", generate_random_string(12))
            elif uuid_name == "UUID3" and (create_windows or create_kali_ubuntu or create_FreeBSD or create_Kali_Centos or create_MacOS or create_window_server):
                file = {
                    ".fbb.sf",
                    ".fdc.sf",
                    ".jbc.sf",
                    ".pb2.sf",
                    ".pbc.sf",  
                    ".sbc.sf",  
                    ".vh.sf",  
                }
                for filen in file:
                    create_config_file(uuid_path,filen,generate_random_string(12))
                create_directory(os.path.join(uuid_path,".sdd.sf"))
                if create_kali_ubuntu:  
                    create_kali_ubuntu_vms(base_path, 1, uuid_str)
                if create_window_server:
                    create_window_server_vms(base_path, 2, uuid_str)
                if create_Kali_Centos:  
                    create_Kali_Centos_vms(base_path, 2, uuid_str)
                if create_FreeBSD:
                    create_FreeBSD_vms(base_path, 3, uuid_str)
                if create_MacOS:  
                    create_MacOS_vms(base_path, 1, uuid_str)
            elif uuid_name == "UUID4" and (create_windows or create_kali_ubuntu or create_FreeBSD or create_Kali_Centos or create_MacOS or create_window_server):
                file = {
                    ".fbb.sf",
                    ".fdc.sf",
                    ".jbc.sf",
                    ".pb2.sf",
                    ".pbc.sf",  
                    ".sbc.sf",  
                    ".vh.sf",  
                }
                for filen in file:
                    create_config_file(uuid_path,filen,generate_random_string(12))
                create_directory(os.path.join(uuid_path,".sdd.sf"))
                if create_windows:
                    create_windows_vms(base_path, 1, uuid_str)
                if create_window_server:
                    create_window_server_vms(base_path, 2, uuid_str)
                if create_Kali_Centos:  
                    create_Kali_Centos_vms(base_path, 3, uuid_str)
                if create_FreeBSD:
                    create_FreeBSD_vms(base_path, 2, uuid_str)
                if create_MacOS:  
                    create_MacOS_vms(base_path, 2, uuid_str)
            elif uuid_name == "UUID5" and (create_windows or create_kali_ubuntu or create_FreeBSD or create_Kali_Centos or create_MacOS or create_window_server):
                file = {
                    ".fbb.sf",
                    ".fdc.sf",
                    ".jbc.sf",
                    ".pb2.sf",
                    ".pbc.sf",  
                    ".sbc.sf",  
                    ".vh.sf",  
                }
                for filen in file:
                    create_config_file(uuid_path,filen,generate_random_string(12))
                create_directory(os.path.join(uuid_path,".sdd.sf"))
                if create_windows:
                    create_windows_vms(base_path, 2, uuid_str)
                if create_kali_ubuntu:  
                    create_kali_ubuntu_vms(base_path, 3, uuid_str)
                if create_window_server:
                    create_window_server_vms(base_path, 2, uuid_str)
                if create_Kali_Centos:  
                    create_Kali_Centos_vms(base_path, 2, uuid_str)
                if create_FreeBSD:
                    create_FreeBSD_vms(base_path, 2, uuid_str)
                    
    
    # Create symbolic link
    # create_symlinks(volumes_path, esxi_config["SYMLINKS"])
    
    # Print out LS -LA results
    if print_uuids:
        print(f"LS -LA results for ESXI '{esxi_name}':")
        result = subprocess.run(['ls', '-la', volumes_path], capture_output=True, text=True)

        # Processing LS -LA results
        for line in result.stdout.splitlines():
            if "->" in line:  # Only symbolic link processing
                parts = line.split("->")
                link_name = parts[0].strip().split()[-1]
                target_uuid = esxi_config["SYMLINKS"][link_name]
                line = line.replace(parts[1].strip(), target_uuid)

                # Check if the target uuid exists in eSxi_config or not
                if target_uuid in esxi_config: 
                    line = line.replace(parts[1].strip(), esxi_config[target_uuid])

            print(line) 

    # Print out uuid if required
    if print_uuids:
        print(f"Uuid for ESXI '{esxi_name}':")
        for uuid_name, uuid_str in esxi_config.items():
            if uuid_name.startswith("UUID"):
                print(f"{uuid_name}: {uuid_str}")
                

def create_windows_vms(base_path, num_vms, target_uuid):
    """Create virtual Windows machine."""
    vmx_content = """# Content of .vmx file for Windows"""
    for _ in range(num_vms):
        version_window = random.choice(["7","8","10","11"])
        number = f"{version_window}"
        vm_name_Window = f"Window_{number}"
        name = "vmware"
        vm_path = os.path.join(base_path, 'vmfs', 'volumes', target_uuid, vm_name_Window)
        os.makedirs(vm_path, exist_ok=True)
        # Create file VMX
        create_config_file(vm_path, f"{vm_name_Window}.vmx", vmx_content)
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmx"),1024 * 1024 * 1024 * 10)
        # Create file log
        create_log_file(vm_path,name + ".log")
        create_fake_file(os.path.join(vm_path,f"{name}.log"),1024 * 1024 * 1024 * 8)
        # Create file VMDK
        create_vmdk_file(vm_path, vm_name_Window)
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmdk"),1024 * 1024 * 1024 * 30)
        # Create file flat.VMDK
        create_flat_vmdk(vm_path, vm_name_Window, size_gb= 90)
        create_config_file(vm_path, f"{vm_name_Window}.vmx.bak", vmx_content)
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmx.bak"),1024 * 1024 * 1024 * 10)
        #Create file .nvram 
        create_config_file(vm_path,f"{vm_name_Window}.nvram",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.nvram"),1024 * 1024 * 1024 * 10)
        #Create file vmsd
        create_config_file(vm_path,f"{vm_name_Window}.vmsd",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmsd"),1024 * 1024 * 1024 * 10)
        #Create file vmsn
        create_config_file(vm_path,f"{vm_name_Window}.vmsn",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmsn"),1024 * 1024 * 1024 * 10)
        #Create file vmtx
        create_config_file(vm_path,f"{vm_name_Window}.vmtx",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmtx"),1024 * 1024 * 1024 * 10)
        #Create file vmxf
        create_config_file(vm_path,f"{vm_name_Window}.vmxf",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmxf"),1024 * 1024 * 1024 * 10)

        print(" Create folder " + vm_name_Window)

def create_window_server_vms(base_path, num_vms, target_uuid):
    """Create virtual Windows machine.""" 
    vmx_content = """#Content Of Vmx File For Windows Server """
    for _ in range(num_vms):
        version_window = random.choice(["2006","2016","2019","2012"])
        number = f"{version_window}"
        vm_name_Window = f"Window_Server_{number}"
        name = "vmware"
        vm_path = os.path.join(base_path, 'vmfs', 'volumes', target_uuid, vm_name_Window)
        os.makedirs(vm_path, exist_ok=True)
        # Create file VMX
        create_config_file(vm_path, f"{vm_name_Window}.vmx", vmx_content)
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmx"),1024 * 1024 * 1024 * 10)
        # Create file log
        create_log_file(vm_path,name + ".log")
        create_fake_file(os.path.join(vm_path,f"{name}.log"),1024 * 1024 * 1024 * 20)
        # Create file VMDK
        create_vmdk_file(vm_path, vm_name_Window)
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmdk"),1024 * 1024 * 1024 * 60)
        # Create file flat.VMDK
        create_flat_vmdk(vm_path, vm_name_Window, size_gb= 80)
        create_config_file(vm_path, f"{vm_name_Window}.vmx.bak", vmx_content)
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmx.bak"),1024 * 1024 * 1024 * 20)
        #Create file .nvram 
        create_config_file(vm_path,f"{vm_name_Window}.nvram",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.nvram"),1024 * 1024 * 1024 * 10)
        #Create file vmsd
        create_config_file(vm_path,f"{vm_name_Window}.vmsd",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmsd"),1024 * 1024 * 1024 * 5)
        #Create file vmsn
        create_config_file(vm_path,f"{vm_name_Window}.vmsn",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmsn"),1024 * 1024 * 1024 * 8)
        #Create file vmtx
        create_config_file(vm_path,f"{vm_name_Window}.vmtx",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmtx"),1024 * 1024 * 1024 * 1)
        #Create file vmxf
        create_config_file(vm_path,f"{vm_name_Window}.vmxf",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmxf"),1024 * 1024 * 1024 * 2)

        print(" Create folder " + vm_name_Window)

def create_kali_ubuntu_vms(base_path, num_vms, target_uuid):
    vmx_content = """# Content of .vmx file for Kali-Linux/ubuntu"""
    #Kali or Ubuntu
    for _ in range(num_vms):
        # Randomly select the type of virtual machine
        vm_type = random.choice(["Kali-Linux","Ubuntu",])
        vm_name = f"{vm_type}"
        name = "vmware"
        # Create Folder VM
        if vm_type == "Kali-Linux":
            vm_path = os.path.join(base_path, 'vmfs', 'volumes', target_uuid, vm_name)
            os.makedirs(vm_path, exist_ok=True)
            # Create file VMX
            create_config_file(vm_path, f"{vm_name}.vmx", vmx_content)
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vmx"),1024 * 1024 * 1024 * 9)
            # Create file log
            create_log_file(vm_path,name + ".log")
            create_fake_file(os.path.join(vm_path,f"{name}.log"),1024 * 1024 * 1024 * 10)
            # Create file VMDK
            create_vmdk_file(vm_path, vm_name)
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vmdk"),1024 * 1024 * 1024 * 30)
            # Create file flat.VMDK
            create_flat_vmdk(vm_path, vm_name, size_gb= 70)
            #Create file vmx.lck
            create_config_file(vm_path, f"{vm_name}.vmx.lck", vmx_content)
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vmx.lck"),1024 * 1024 * 1024 * 9)
            #Create file .nvram 
            create_config_file(vm_path,f"{vm_name}.nvram",generate_random_string(1024))
            create_fake_file(os.path.join(vm_path,f"{vm_name}.nvram"),1024 * 1024 * 1024 * 3)
            #Create file vmsd
            create_config_file(vm_path,f"{vm_name}.vmsd",generate_random_string(1024))
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vmsd"),1024 * 1024 * 1024 * 9)
            #Create file vswp
            create_config_file(vm_path,f"{vm_name}-{generate_random_string(5)}.vswp",generate_random_string(1024))
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vswp"),1024 * 1024 * 1024 * 9)
            create_config_file(vm_path,"vmx-"f"{vm_name}-{generate_random_string(20)}.vswp",generate_random_string(1024))
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vswp"),1024 * 1024 * 1024 * 10)
            #Create file vmsn
            create_config_file(vm_path,f"{vm_name}.vmsn",generate_random_string(1024))
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vmsn"),1024 * 1024 * 1024 * 6)
            #Create file vmtx
            create_config_file(vm_path,f"{vm_name}.vmtx",generate_random_string(1024))
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vmtx"),1024 * 1024 * 1024 * 1)
            #Create file vmxf
            create_config_file(vm_path,f"{vm_name}.vmxf",generate_random_string(1024))
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vmxf"),1024 * 1024 * 1024 * 1)

            print(" Create folder " + vm_name)


        elif vm_type == "Ubuntu":
            vm_path = os.path.join(base_path, 'vmfs', 'volumes',target_uuid, vm_name)
            os.makedirs(vm_path, exist_ok=True)
            # Create file VMX
            create_config_file(vm_path, f"{vm_name}.vmx", vmx_content)
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vmx"),1024 * 1024 * 1024 * 9)
            # Create file log
            create_log_file(vm_path,name + ".log")
            create_fake_file(os.path.join(vm_path,f"{name}.log"),1024 * 1024 * 1024 * 10)
            # Create file VMDK
            create_vmdk_file(vm_path, vm_name)
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vmdk"),1024 * 1024 * 1024 * 27)
            # Create file flat.VMDK
            create_flat_vmdk(vm_path, vm_name, size_gb= 60)
            #Create file .nvram 
            create_config_file(vm_path,f"{vm_name}.nvram",generate_random_string(1024))
            create_fake_file(os.path.join(vm_path,f"{vm_name}.nvram"),1024 * 1024 * 1024 * 3)
            #Create file vmsd
            create_config_file(vm_path,f"{vm_name}-{generate_random_string(5)}.vmsd",generate_random_string(1024))
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vmsd"),1024 * 1024 * 1024 * 9)
            create_config_file(vm_path,"vmx-"f"{vm_name}-{generate_random_string(20)}.vswp",generate_random_string(1024))
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vswp"),1024 * 1024 * 1024 * 10)
            #Create file vmsn
            create_config_file(vm_path,f"{vm_name}.vmsn",generate_random_string(1024))
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vmsn"),1024 * 1024 * 1024 * 9)
            #Create file vmtx
            create_config_file(vm_path,f"{vm_name}.vmtx",generate_random_string(1024))
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vmtx"),1024 * 1024 * 1024 * 1)
            #Create file vmxf
            create_config_file(vm_path,f"{vm_name}.vmxf",generate_random_string(1024))
            create_fake_file(os.path.join(vm_path,f"{vm_name}.vmxf"),1024 * 1024 * 1024 * 1)

            print(" Create folder " + vm_name)
            
def create_Kali_Centos_vms(base_path, num_vms, target_uuid):
    vmx_content = """# Content of .vmx file for Kali/Centos"""
    #Kali or Ubuntu
    for _ in range(num_vms):
        # Randomly select the type of virtual machine
        vm_type = random.choice(["Kali","Centos"])
        vm_name = f"{vm_type}"
        name = "vmware"
        # Create Folder VM
        vm_path = os.path.join(base_path, 'vmfs', 'volumes', target_uuid, vm_name)
        os.makedirs(vm_path, exist_ok=True)
        # Create file VMX
        create_config_file(vm_path, f"{vm_name}.vmx", vmx_content)
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmx"),1024 * 1024 * 1024 * 9)
        # Create file log
        create_log_file(vm_path,name + ".log")
        create_fake_file(os.path.join(vm_path,f"{name}.log"),1024 * 1024 * 1024 * 10)
        # Create file VMDK
        create_vmdk_file(vm_path, vm_name)
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmdk"),1024 * 1024 * 1024 * 30)
        # Create file flat.VMDK
        create_flat_vmdk(vm_path, vm_name, size_gb= 73)
        #Create file vmx.lck
        create_config_file(vm_path, f"{vm_name}.vmx.lck", vmx_content)
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmx.lck"),1024 * 1024 * 1024 * 9)
        #Create file .nvram 
        create_config_file(vm_path,f"{vm_name}.nvram",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.nvram"),1024 * 1024 * 1024 * 3)
        #Create file vmsd
        create_config_file(vm_path,f"{vm_name}.vmsd",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmsd"),1024 * 1024 * 1024 * 9)
        #Create file vswp
        create_config_file(vm_path,f"{vm_name}-{generate_random_string(5)}.vswp",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vswp"),1024 * 1024 * 1024 * 9)
        create_config_file(vm_path,"vmx-"f"{vm_name}-{generate_random_string(20)}.vswp",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vswp"),1024 * 1024 * 1024 * 10)
        #Create file vmsn
        create_config_file(vm_path,f"{vm_name}.vmsn",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmsn"),1024 * 1024 * 1024 * 7)
        #Create file vmtx
        create_config_file(vm_path,f"{vm_name}.vmtx",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmtx"),1024 * 1024 * 1024 * 1)
        #Create file vmxf
        create_config_file(vm_path,f"{vm_name}.vmxf",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmxf"),1024 * 1024 * 1024 * 1)

        print(" Create folder " + vm_name)

def create_MacOS_vms(base_path, num_vms, target_uuid):
    vmx_content = """# Content of .vmx file for MacOS"""
    #Kali or Ubuntu
    for _ in range(num_vms):
        version_window = random.choice(["12","10.5","10.9","10.15","10","11"])
        number = f"{version_window}"
        vm_name = f"MacOS_{number}"
        name = "vmware"
        vm_path = os.path.join(base_path, 'vmfs', 'volumes',target_uuid, vm_name)
        os.makedirs(vm_path, exist_ok=True)
        # Create file VMX
        create_config_file(vm_path, f"{vm_name}.vmx", vmx_content)
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmx"),1024 * 1024 * 1024 * 9)
        # Create file log
        create_log_file(vm_path,name + ".log")
        create_fake_file(os.path.join(vm_path,f"{name}.log"),1024 * 1024 * 1024 * 10)
        # Create file VMDK
        create_vmdk_file(vm_path, vm_name)
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmdk"),1024 * 1024 * 1024 * 27)
        # Create file flat.VMDK
        create_flat_vmdk(vm_path, vm_name, size_gb= 68)
        #Create file .nvram 
        create_config_file(vm_path,f"{vm_name}.nvram",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.nvram"),1024 * 1024 * 1024 * 3)
        #Create file vmsd
        create_config_file(vm_path,f"{vm_name}-{generate_random_string(5)}.vmsd",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmsd"),1024 * 1024 * 1024 * 9)
        create_config_file(vm_path,"vmx-"f"{vm_name}-{generate_random_string(20)}.vswp",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vswp"),1024 * 1024 * 1024 * 10)
        #Create file vmsn
        create_config_file(vm_path,f"{vm_name}.vmsn",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmsn"),1024 * 1024 * 1024 * 6)
        #Create file vmtx
        create_config_file(vm_path,f"{vm_name}.vmtx",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmtx"),1024 * 1024 * 1024 * 1)
        #Create file vmxf
        create_config_file(vm_path,f"{vm_name}.vmxf",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmxf"),1024 * 1024 * 1024 * 1)

        print(" Create folder " + vm_name)

def create_FreeBSD_vms(base_path, num_vms, target_uuid):
    vmx_content = """# Content of .vmx file for FreeBSD"""
    #Kali or Ubuntu
    for _ in range(num_vms):
        version_window = random.choice(["12","13","Pre-11","11"])
        number = f"{version_window}"
        vm_name = f"FreeBSD_{number}"
        name = "vmware"
        vm_path = os.path.join(base_path, 'vmfs', 'volumes',target_uuid, vm_name)
        os.makedirs(vm_path, exist_ok=True)
        # Create file VMX
        create_config_file(vm_path, f"{vm_name}.vmx", vmx_content)
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmx"),1024 * 1024 * 1024 * 10)
        # Create file log
        create_log_file(vm_path,name + ".log")
        create_fake_file(os.path.join(vm_path,f"{name}.log"),1024 * 1024 * 1024 * 20)
        # Create file VMDK
        create_vmdk_file(vm_path, vm_name)
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmdk"),1024 * 1024 * 1024 * 50)
        # Create file flat.VMDK
        create_flat_vmdk(vm_path, vm_name, size_gb= 75)
        #Create file .nvram 
        create_config_file(vm_path,f"{vm_name}.nvram",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.nvram"),1024 * 1024 * 1024 * 3)
        #Create file vmsd
        create_config_file(vm_path,f"{vm_name}-{generate_random_string(5)}.vmsd",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmsd"),1024 * 1024 * 1024 * 9)
        create_config_file(vm_path,"vmx-"f"{vm_name}-{generate_random_string(20)}.vswp",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vswp"),1024 * 1024 * 1024 * 5)
        #Create file vmsn
        create_config_file(vm_path,f"{vm_name}.vmsn",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmsn"),1024 * 1024 * 1024 * 5)
        #Create file vmtx
        create_config_file(vm_path,f"{vm_name}.vmtx",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmtx"),1024 * 1024 * 1024 * 1)
        #Create file vmxf
        create_config_file(vm_path,f"{vm_name}.vmxf",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name}.vmxf"),1024 * 1024 * 1024 * 1)

        print(" Create folder " + vm_name)
