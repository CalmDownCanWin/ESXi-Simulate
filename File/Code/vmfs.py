import os
import random
import uuid

from ESXi_config import create_config_file
from ESXi_config import create_vmx_file
from ESXi_config import create_vmdk_file
from ESXi_config import create_fake_datastore
from ESXi_config import create_flat_vmdk
from ESXi_config import create_log_file
from ESXi_config import generate_random_string


def create_esx_vmfs(base_path="/ESXI 7"):
    # Thư mục vmfs
    # Tạo datastore giả mạo
    create_fake_datastore(base_path, "NVmeDataStore",80 )
    # Thư mục vmfs/volumes/bootbank
    bootbank_path = os.path.join(base_path, "vmfs", "volumes")
    Databootbank_1 = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\BOOTBANK1.txt"
    with open(Databootbank_1, 'r', encoding='utf-8') as f:
        boot_cfg_content_1 = f.read()  # Đọc nội dung file vào biến chuỗi
    Databootbank_2 = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\BOOTBANK2.txt"
    with open(Databootbank_2, 'r', encoding='utf-8') as f:
        boot_cfg_content_2 = f.read()  # Đọc nội dung file vào biến chuỗi
    create_config_file(bootbank_path, "BOOTBANK1", boot_cfg_content_1)
    create_config_file(bootbank_path, "BOOTBANK2", boot_cfg_content_2)

    #Tạo OSDATA
    OSDA = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\OSDATA.txt"
    with open(OSDA, 'r', encoding='utf-8') as f:
        content = f.read()  # Đọc nội dung file vào biến chuỗi
    # Kiểm tra xem đã có file OSDATA trong thư mục hay chưa
    for filename in os.listdir(bootbank_path):
        if filename.startswith("OSDATA"):
            return  # Nếu có file OSDATA rồi thì thoát khỏi hàm
    create_config_file(bootbank_path,f"OSDATA-{str(uuid.uuid4())}",content)
 
    #Thư mục vmfs/devices
    device_path = os.path.join(base_path,"vmfs")
    devices_content = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\device.txt"
    with open(devices_content, 'r', encoding='utf-8') as f:
        data_devices_content = f.read()  # Đọc nội dung file vào biến chuỗi
    create_config_file(device_path,"devices",data_devices_content)

    # Tạo cấu trúc máy ảo Windows, Kali-Linux và Ubuntu
    domain = "example.com"
# Window
    for _ in range(5):
        version_window = random.choice(["7","8","10","11"])
        number = f"{version_window}"
        vm_name_Window = f"Window_{number}"
        name = "vmware"
        Datawindow = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\Window 10.vmx"
        with open(Datawindow, 'r', encoding='utf-8') as f:
            vmx_content = f.read()  # Đọc nội dung file vào biến chuỗi
        vm_path = os.path.join(base_path, 'vmfs', 'volumes','NVmeDataStore', vm_name_Window)
        os.makedirs(vm_path, exist_ok=True)
        # Tạo file VMX
        vmx_file = create_vmx_file(domain, vm_path, vm_name_Window)
        create_config_file(vm_path, f"{vm_name_Window}.vmx", vmx_content)
        print(f"File VMX giả mạo cho {vm_name_Window} đã được tạo: {vmx_file}")
        # Tạo file log
        create_log_file(vm_path,name + ".log")
        # Tạo file VMDK
        create_vmdk_file(vm_path, vm_name_Window)
        # Tạo file flat.VMDK
        create_flat_vmdk(vm_path, vm_name_Window, size_gb= 100)
        # Tạo file .vmx.bak (có thể được sử dụng trong quá trình restore)
        create_config_file(vm_path, f"{vm_name_Window}.vmx.bak", vmx_content)
        #Tạo file .nvram 
        create_config_file(vm_path,f"{vm_name_Window}.nvram",generate_random_string(1024))
        #Tạo file vmsd
        create_config_file(vm_path,f"{vm_name_Window}.vmsd",generate_random_string(1024))
        #Tạo file vmsn
        create_config_file(vm_path,f"{vm_name_Window}.vmsn",generate_random_string(1024))
        #Tạo file vmtx
        create_config_file(vm_path,f"{vm_name_Window}.vmtx",generate_random_string(1024))
        #Tạo file vmxf
        create_config_file(vm_path,f"{vm_name_Window}.vmxf",generate_random_string(1024))

#Kali or Ubuntu
    for _ in range(5):
        # Chọn ngẫu nhiên loại máy ảo
        vm_type = random.choice(["Kali-Linux","Ubuntu"])
        vm_name = f"{vm_type}"
        name = "vmware"
        # Tạo thư mục VM
        if vm_type == "Kali-Linux":
            DataLinux = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\Window 10.vmx"
            with open(DataLinux, 'r', encoding='utf-8') as f:
                vmx_content = f.read()  # Đọc nội dung file vào biến chuỗi
            vm_path = os.path.join(base_path, 'vmfs', 'volumes','NVmeDataStore', vm_name)
            os.makedirs(vm_path, exist_ok=True)
            # Tạo file VMX
            vmx_file = create_vmx_file(domain, vm_path, vm_name)
            create_config_file(vm_path, f"{vm_name}.vmx", vmx_content)
            # Tạo file log
            create_log_file(vm_path,name + ".log")
            # Tạo file VMDK
            create_vmdk_file(vm_path, vm_name)
            # Tạo file flat.VMDK
            create_flat_vmdk(vm_path, vm_name, size_gb= 100)
            #Tạo file vmx.lck
            create_config_file(vm_path, f"{vm_name}.vmx.lck", vmx_content)
            #Tạo file .nvram 
            create_config_file(vm_path,f"{vm_name}.nvram",generate_random_string(1024))
            #Tạo file vmsd
            create_config_file(vm_path,f"{vm_name}.vmsd",generate_random_string(1024))
            #Tạo file vswp
            create_config_file(vm_path,f"{vm_name}-{generate_random_string(5)}.vswp",generate_random_string(1024))
            #Tạo file vmsn
            create_config_file(vm_path,f"{vm_name}.vmsn",generate_random_string(1024))
            #Tạo file vmtx
            create_config_file(vm_path,f"{vm_name}.vmtx",generate_random_string(1024))
            #Tạo file vmxf
            create_config_file(vm_path,f"{vm_name}.vmxf",generate_random_string(1024))




        elif vm_type == "Ubuntu":
            DataUbuntu = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\Window 10.vmx"
            with open(DataUbuntu, 'r', encoding='utf-8') as f:
                vmx_content = f.read()  # Đọc nội dung file vào biến chuỗi
            vm_path = os.path.join(base_path, 'vmfs', 'volumes','NVmeDataStore', vm_name)
            os.makedirs(vm_path, exist_ok=True)
            # Tạo file VMX
            vmx_file = create_vmx_file(domain, vm_path, vm_name)
            create_config_file(vm_path, f"{vm_name}.vmx", vmx_content)
            print(f"File VMX giả mạo cho {vm_name} đã được tạo: {vmx_file}")
            # Tạo file log
            create_log_file(vm_path,name + ".log")
            # Tạo file VMDK
            create_vmdk_file(vm_path, vm_name)
            # Tạo file flat.VMDK
            create_flat_vmdk(vm_path, vm_name, size_gb= 100)
            #Tạo file .nvram 
            create_config_file(vm_path,f"{vm_name}.nvram",generate_random_string(1024))
            #Tạo file vmsd
            create_config_file(vm_path,f"{vm_name}.vmsd",generate_random_string(1024))
            #Tạo file vmsn
            create_config_file(vm_path,f"{vm_name}.vmsn",generate_random_string(1024))
            #Tạo file vmtx
            create_config_file(vm_path,f"{vm_name}.vmtx",generate_random_string(1024))
            #Tạo file vmxf
            create_config_file(vm_path,f"{vm_name}.vmxf",generate_random_string(1024))