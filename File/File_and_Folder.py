import random
import os
import uuid

from ESXi_config import generate_random_string
from ESXi_config import create_config_file
from ESXi_config import create_vmware_lic
from ESXi_config import create_vmdk_file
from ESXi_config import create_bin
from ESXi_config import create_dev
from ESXi_config import create_include
from ESXi_config import create_lib
from ESXi_config import create_lib64
from ESXi_config import create_opt
from ESXi_config import create_passwd_file
from ESXi_config import create_fake_datastore
from ESXi_config import create_hosts_file
from ESXi_config import create_ssh_keys
from ESXi_config import create_sshd_config
from ESXi_config import create_proc
from ESXi_config import create_usr
from ESXi_config import create_vmimages
from ESXi_config import create_vmx_file
from ESXi_config import create_tardisks
from ESXi_config import create_tardisks_noauto
from ESXi_config import create_log_file
from ESXi_config import create_flat_vmdk




def create_esx_config_files(base_path="/ESXI 7"):
    """Tạo các file cấu hình ESXi 7."""

#Tạo file trong thư mục chính 
    Databootbank_1 = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\VM\BOOTBANK1.txt"
    with open(Databootbank_1, 'r', encoding='utf-8') as f:
        boot_cfg_content_1 = f.read()  # Đọc nội dung file vào biến chuỗi
    create_config_file(base_path,"bootbank",boot_cfg_content_1)

    create_config_file(base_path,"altbootbank",generate_random_string(2))
    create_config_file(base_path,"bootpart.gz",generate_random_string(80))
    create_config_file(base_path,"bootpart4kn.gz",generate_random_string(70))
    create_config_file(base_path,"local.tgz",generate_random_string(15))
    create_config_file(base_path,"local.tgz.ve",generate_random_string(20))
    create_config_file(base_path,"locker",generate_random_string(2))
    create_config_file(base_path,"productLocker",generate_random_string(2))
    create_config_file(base_path,"sbin",generate_random_string(2))
    create_config_file(base_path,"scratch",generate_random_string(2))
    create_config_file(base_path,"store",generate_random_string(2))



# Thư mục /etc/vmware
    vmware_path = os.path.join(base_path, "etc", "vmware")

    # Tạo file esx.conf
    esx_conf_content = f"""
    # ESXi Configuration File
    hostname = "esxi-{random.randint(1, 10)}.example.com"
    hostname = "prod-esxi-02.domain.com"
    hostname = "esxi-{random.randint(1, 10)}.example.com"
    # Cấu hình mạng giả mạo
    /net/ipv4/interfaces/vmk0/ipAddress = "10.10.10.100"
    /net/ipv4/interfaces/vmk0/subnetMask = "255.255.255.0"
    /net/ipv4/gateway = "10.10.10.1"
    net.dns.servers = "1.1.1.1, 8.8.8.8"
    net.ipv4.tcp_syncookies = {random.randint(0, 1)}
    net.ipv4.tcp_timestamps = {random.randint(0, 1)}
    vmkernel.boot.diskUUID = "{generate_random_string(36)}"
    vmkernel.boot.diskDevice = "{generate_random_string(10)}"
    vmkernel.boot.diskType = "{random.choice(['disk', 'cdrom'])}"
    vmkernel.boot.diskPath = "{generate_random_string(20)}"
    # Phiên bản ESXi giả mạo (cũ hơn, có thể chứa lỗ hổng)
    /product/version = "6.7.0" 
    /product/build = "14320388"

    # Vô hiệu hóa SSH (hoặc thay đổi cổng)
    /system/services/ssh/enabled = "0" 
    # /system/services/ssh/port = "2222"

    # Cấu hình SNMP giả mạo
    /snmp/enabled = "1"
    /snmp/community = "public" 

    # Thêm thông tin giả mạo (có thể ẩn trong comment)
    # FAKE_FLAG = "Ransomware_Deception"
    # BACKUP_SERVER = "10.10.10.200"
    # ADMIN_PASSWORD = "password123"
    """
    create_config_file(vmware_path, "esx.conf", esx_conf_content)

    # Tạo file esx.xml
    esx_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <network>
            <dns>{generate_random_string(15)}</dns>
            <gateway>{generate_random_string(15)}</gateway>
        </network>
        <storage>
            <datastore>{generate_random_string(10)}</datastore>
            <disk>{generate_random_string(10)}</disk>
        </storage>
    </config>
    """
    create_config_file(vmware_path, "esx.xml", esx_xml_content)

    # Tạo file esx.json
    esx_json_content = f"""{{
        "network": {{
            "dns": [
                "{generate_random_string(15)}"
            ],
            "gateway": "{generate_random_string(15)}"
        }},
        "storage": {{
            "datastore": [
                "{generate_random_string(10)}"
            ],
            "disk": [
                "{generate_random_string(10)}"
            ]
        }}
    }}
    """
    create_config_file(vmware_path, "esx.json", esx_json_content)

    # Tạo file hostd/config.xml
    hostd_path = os.path.join(vmware_path, "hostd")
    hostd_config_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <network>
            <port>{random.randint(1024, 65535)}</port>
        </network>
        <storage>
            <path>{generate_random_string(10)}</path>
        </storage>
    </config>
    """
    create_config_file(hostd_path, "config.xml", hostd_config_xml_content)

    # Tạo file hostd/proxy.xml
    hostd_proxy_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <proxy>
            <enabled>{random.choice([True, False])}</enabled>
            <port>{random.randint(1024, 65535)}</port>
        </proxy>
    </config>
    """
    create_config_file(hostd_path, "proxy.xml", hostd_proxy_xml_content)

    # Tạo file hostd/vmInventory.xml
    hostd_vminventory_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <inventory>
            <vm name="{generate_random_string(10)}" uuid="{str(uuid.uuid4()).replace('-', '')}"/>
            <vm name="{generate_random_string(10)}" uuid="{str(uuid.uuid4()).replace('-', '')}"/>
        </inventory>
    </config>
    """
    create_config_file(hostd_path, "vmInventory.xml", hostd_vminventory_xml_content)

    # Tạo file hostd/vmAutoStart.xml
    hostd_vmautostart_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <autostart>
            <vm name="{generate_random_string(10)}" uuid="{str(uuid.uuid4()).replace('-', '')}"/>
            <vm name="{generate_random_string(10)}" uuid="{str(uuid.uuid4()).replace('-', '')}"/>
        </autostart>
    </config>
    """
    create_config_file(hostd_path, "vmAutoStart.xml", hostd_vmautostart_xml_content)

    # Tạo file vpxa/vpxa.cfg
    vpxa_path = os.path.join(vmware_path, "vpxa")
    vpxa_cfg_content = f"""
    # vCenter Agent Configuration
    vpxa.hostname = "{generate_random_string(10)}"
    vpxa.port = {random.randint(1024, 65535)}
    vpxa.ssl.enabled = {random.choice([True, False])}
    """
    create_config_file(vpxa_path, "vpxa.cfg", vpxa_cfg_content)

    # Tạo file vpxa/vpxa.xml
    vpxa_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <vpxa>
            <hostname>{generate_random_string(10)}</hostname>
            <port>{random.randint(1024, 65535)}</port>
            <ssl enabled="{random.choice([True, False])}"/>
        </vpxa>
    </config>
    """
    create_config_file(vpxa_path, "vpxa.xml", vpxa_xml_content)

    # Tạo file ssl/rui.crt
    ssl_path = os.path.join(vmware_path, "ssl")
    ssl_rui_crt_content = generate_random_string(1024)
    create_config_file(ssl_path, "rui.crt", ssl_rui_crt_content)

    # Tạo file ssl/rui.key
    ssl_rui_key_content = generate_random_string(1024)
    create_config_file(ssl_path, "rui.key", ssl_rui_key_content)

    # Tạo file ssl/server.crt
    ssl_server_crt_content = generate_random_string(1024)
    create_config_file(ssl_path, "server.crt", ssl_server_crt_content)

    # Tạo file ssl/server.key
    ssl_server_key_content = generate_random_string(1024)
    create_config_file(ssl_path, "server.key", ssl_server_key_content)

    # Tạo file vsan/vsan.conf
    vsan_path = os.path.join(vmware_path, "vsan")
    vsan_conf_content = f"""
    # vSAN Configuration File
    vsan.cluster.name = "{generate_random_string(10)}"
    vsan.cluster.id = {random.randint(1, 100)}
    vsan.storage.capacity = {random.randint(100, 1000)}
    """
    create_config_file(vsan_path, "vsan.conf", vsan_conf_content)

    # Tạo file vsan/vsan.xml
    vsan_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <vsan>
            <cluster name="{generate_random_string(10)}" id="{random.randint(1, 100)}"/>
            <storage capacity="{random.randint(100, 1000)}"/>
        </vsan>
    </config>
    """
    create_config_file(vsan_path, "vsan.xml", vsan_xml_content)

    # Tạo file vsan/vsan.json
    vsan_json_content = f"""{{
        "cluster": {{
            "name": "{generate_random_string(10)}",
            "id": {random.randint(1, 100)}
        }},
        "storage": {{
            "capacity": {random.randint(100, 1000)}
        }}
    }}
    """
    create_config_file(vsan_path, "vsan.json", vsan_json_content)

    # Tạo file firewall/firewall.xml
    firewall_path = os.path.join(vmware_path, "firewall")
    firewall_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <firewall>
            <enabled>{random.choice([True, False])}</enabled>
            <rule name="{generate_random_string(10)}" action="{random.choice(['allow', 'deny'])}" protocol="{random.choice(['tcp', 'udp'])}" port="{random.randint(1, 65535)}"/>
        </firewall>
    </config>
    """
    create_config_file(firewall_path, "firewall.xml", firewall_xml_content)

    # Tạo file vswitch.conf
    vswitch_conf_content = f"""
    # vSwitch Configuration
    vswitch.name = "{generate_random_string(10)}"
    vswitch.portgroup = "{generate_random_string(10)}"
    vswitch.network = "{generate_random_string(10)}"
    """
    create_config_file(vmware_path, "vswitch.conf", vswitch_conf_content)

    # Tạo file snmp.xml
    snmp_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <snmp>
            <enabled>{random.choice([True, False])}</enabled>
            <community>{generate_random_string(10)}</community>
            <port>{random.randint(161, 65535)}</port>
        </snmp>
    </config>
    """
    create_config_file(vmware_path, "snmp.xml", snmp_xml_content)

    # Tạo file locker.conf
    locker_conf_content = f"""
    # vSphere Locker Configuration
    locker.port = {random.randint(1024, 65535)}
    locker.enabled = {random.choice([True, False])}
    """
    create_config_file(vmware_path, "locker.conf", locker_conf_content)

    # Tạo file license.cfg
    license_cfg_content = f"""
    # ESXi License File
    <ConfigRoot>
        <epoc>"{generate_random_string(45)}"/5z+Dn9/"{generate_random_string(16)}"</epoc>
        <float>"{generate_random_string(90)}"=</float>
        <mode>eval</mode>
        <owner/>
    </ConfigRoot>
    """
    create_config_file(vmware_path, "license.cfg", license_cfg_content)

    # Tạo file vmware.lic
    vmware_path = os.path.join(base_path, "etc", "vmware")
    create_vmware_lic(vmware_path)

#Thư mục /etc
    # Tạo file /etc/hosts
    etc_path = os.path.join(base_path, "etc")
    create_hosts_file(etc_path)
    #Tạo cac file /etc/ssh/
    # Tạo file /etc/ssh/sshd_config và các key
    ssh_path = os.path.join(base_path, "etc", "ssh")
    key_path = os.path.join(ssh_path,"keys-root")
    create_ssh_keys(ssh_path)  # Tạo key trước khi tạo sshd_config
    fake_ssh_port = 2222 
    allowed_ips = ["10.0.0.1", "192.168.1.100"]  
    create_sshd_config(ssh_path, fake_ssh_port, allowed_ips)
    create_sshd_config(ssh_path)
    create_config_file(ssh_path,"moduli",generate_random_string(12))
    create_config_file(key_path,"authorized_keys",generate_random_string(10))
    create_config_file(ssh_path,".#ssh_host_ecdsa_key",generate_random_string(12))
    create_config_file(ssh_path,".#ssh_host_ecdsa_key.pub",generate_random_string(12))
    create_config_file(ssh_path,".#ssh_host_rsa_key",generate_random_string(12))
    create_config_file(ssh_path,".#ssh_host_rsa_key.pub",generate_random_string(12))

    #các file trong thư mục etc
    Datashadow = "S:\Summer2024\IAP491_G2\Code\Luaga\File_Example\shadow"
    with open(Datashadow, 'r', encoding='utf-8') as f:
        content_shadow = f.read()  # Đọc nội dung file vào biến chuỗi 
    create_config_file(etc_path,"shadow",content_shadow)
    create_config_file(etc_path,"rc.local",generate_random_string(50))

    #Tạo /bin
    bin_path = os.path.join(base_path,"bin")
    create_bin(bin_path)

    #Tạo /dev
    dev_path = os.path.join(base_path,"dev")
    create_dev(dev_path)

    #Tạo /include
    include_path = os.path.join(base_path,"include")
    create_include(include_path)

    #Tạo /lib
    lib_path = os.path.join(base_path,"lib")
    create_lib(lib_path)

    #Tạo /lib64
    lib64_path = os.path.join(base_path,"lib64")
    create_lib64(lib64_path)

    #Tạo /opt
    opt_path = os.path.join(base_path,"opt")
    create_opt(opt_path)

    #Tạo /proc
    proc_path = os.path.join(base_path,"proc")
    create_proc(proc_path)

    #Tạo /usr
    usr_path = os.path.join(base_path,"usr")
    create_usr(usr_path)
    # create_config_file(usr_path,"bin",)

    #Tạo /vmimages
    vmimages_path = os.path.join(base_path,"vmimages")
    create_vmimages(vmimages_path)
    # Tạo /tardisks
    tardisks_path = os.path.join(base_path, "tardisks")
    create_tardisks(tardisks_path)

    # Tạo /tardisks.noauto
    tardisks_noauto_path = os.path.join(base_path, "tardisks.noauto")
    create_tardisks_noauto(tardisks_noauto_path)

    # Tạo datastore giả mạo
    create_fake_datastore(base_path, "NVmeDataStore",80 )

    # Tạo file vmkiscsid/iscsid.conf
    vmkiscsid_path = os.path.join(vmware_path, "vmkiscsid")
    iscsid_conf_content = f"""
    # iSCSI Configuration File
    node.name = "{generate_random_string(10)}"
    discovery.sendtargets.all = yes
    discovery.sendtargets.port = 3260
    """
    create_config_file(vmkiscsid_path, "iscsid.conf", iscsid_conf_content)

    # Tạo file vmkiscsid/initiatorname.iscsi
    initiatorname_iscsi_content = f"""
    # iSCSI Initiator Name
    initiatorname = "{generate_random_string(10)}"
    """
    create_config_file(vmkiscsid_path, "initiatorname.iscsi", initiatorname_iscsi_content)

    # Tạo file network/vnet.conf
    network_path = os.path.join(vmware_path, "network")
    vnet_conf_content = f"""
    # Virtual Network Configuration
    vnet.name = "{generate_random_string(10)}"
    vnet.vswitch = "{generate_random_string(10)}"
    vnet.network = "{generate_random_string(10)}"
    """
    create_config_file(network_path, "vnet.conf", vnet_conf_content)

    # Tạo file network/vmxnet3.conf
    vmxnet3_conf_content = f"""
    # vmxnet3 Network Configuration
    vmxnet3.name = "{generate_random_string(10)}"
    vmxnet3.vswitch = "{generate_random_string(10)}"
    vmxnet3.network = "{generate_random_string(10)}"
    """
    create_config_file(network_path, "vmxnet3.conf", vmxnet3_conf_content)

    # Tạo file network/vnic.conf
    vnic_conf_content = f"""
    # Virtual NIC Configuration
    vnic.name = "{generate_random_string(10)}"
    vnic.vswitch = "{generate_random_string(10)}"
    vnic.network = "{generate_random_string(10)}"
    """
    create_config_file(network_path, "vnic.conf", vnic_conf_content)

    # Tạo file passwd
    vmware_path = os.path.join(base_path, "etc", "vmware")
    create_passwd_file(etc_path)

    # Tạo file system/custom_config.xml
    system_path = os.path.join(vmware_path, "system")
    custom_config_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <customConfig>
            <setting name="{generate_random_string(10)}" value="{generate_random_string(10)}"/>
        </customConfig>
    </config>
    """
    create_config_file(system_path, "custom_config.xml", custom_config_xml_content)

    # Tạo file autostart.xml
    autostart_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <autostart>
            <vm name="{generate_random_string(10)}" uuid="{str(uuid.uuid4()).replace('-', '')}"/>
            <vm name="{generate_random_string(10)}" uuid="{str(uuid.uuid4()).replace('-', '')}"/>
        </autostart>
    </config>
    """
    create_config_file(vmware_path, "autostart.xml", autostart_xml_content)

    # Tạo file vmkboot.xml
    vmkboot_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <vmkboot>
            <device type="{random.choice(['disk', 'cdrom'])}" uuid="{str(uuid.uuid4()).replace('-', '')}"/>
        </vmkboot>
    </config>
    """
    create_config_file(vmware_path, "vmkboot.xml", vmkboot_xml_content)

    # Tạo file datastore.xml
    datastore_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <datastore>
            <name>{generate_random_string(10)}</name>
            <uuid>{str(uuid.uuid4()).replace('-', '')}</uuid>
        </datastore>
    </config>
    """
    create_config_file(vmware_path, "datastore.xml", datastore_xml_content)

    # Tạo file vsanmgmtd.conf
    vsanmgmtd_conf_content = f"""
    # vSAN Management Configuration
    vsanmgmtd.port = {random.randint(1024, 65535)}
    vsanmgmtd.enabled = {random.choice([True, False])}
    """
    create_config_file(vmware_path, "vsanmgmtd.conf", vsanmgmtd_conf_content)

# Thư mục vmfs
    # Thư mục vmfs/volumes/bootbank
    bootbank_path = os.path.join(base_path, "vmfs", "volumes")
    Databootbank_1 = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\VM\BOOTBANK1.txt"
    with open(Databootbank_1, 'r', encoding='utf-8') as f:
        boot_cfg_content_1 = f.read()  # Đọc nội dung file vào biến chuỗi
    Databootbank_2 = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\VM\BOOTBANK2.txt"
    with open(Databootbank_2, 'r', encoding='utf-8') as f:
        boot_cfg_content_2 = f.read()  # Đọc nội dung file vào biến chuỗi
    create_config_file(bootbank_path, "BOOTBANK1", boot_cfg_content_1)
    create_config_file(bootbank_path, "BOOTBANK2", boot_cfg_content_2)

    #Tạo OSDATA
    OSDA = "S:\Summer2024\IAP491_G2\Code\Luaga\File_Example\OSDATA.txt"
    with open(OSDA, 'r', encoding='utf-8') as f:
        content = f.read()  # Đọc nội dung file vào biến chuỗi
    create_config_file(bootbank_path,f"OSDATA-{str(uuid.uuid4())}",content)

    #Tạo các folder với tên uuid 


    #Thư mục vmfs/devices
    device_path = os.path.join(base_path,"vmfs")
    devices_content = "S:\Summer2024\IAP491_G2\Code\Luaga\File_Example\device.txt"
    with open(devices_content, 'r', encoding='utf-8') as f:
        data_devices_content = f.read()  # Đọc nội dung file vào biến chuỗi
    create_config_file(device_path,"devices",data_devices_content)

    # Thư mục /var/log/vmware
    var_log_vmware_path = os.path.join(base_path, "var", "log", "vmware")
    create_config_file(var_log_vmware_path, "hostd.log", "")
    create_config_file(var_log_vmware_path, "vpxa.log", "")


    # Tạo cấu trúc máy ảo Windows, Kali-Linux và Ubuntu
    domain = "example.com"
    for _ in range(10):
        # Chọn ngẫu nhiên loại máy ảo
        vm_type = random.choice(["Windows", "Kali-Linux","Ubuntu"])
        # vm_type = "Window"
        vm_name = f"{vm_type}"
        version_window = random.choice(["7","8","10","11"])
        number = f"{version_window}"
        vm_name_Window = f"{vm_type}_{number}"
        name = "vmware"

        # Tạo thư mục VM
        if vm_type == "Window":
            Datawindow = "S:\Summer2024\IAP491_G2\Code\Luaga\File_Example\Window 10.vmx"
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



        elif vm_type == "Kali-Linux":
            DataLinux = "S:\Summer2024\IAP491_G2\Code\Luaga\File_Example\Window 10.vmx"
            with open(DataLinux, 'r', encoding='utf-8') as f:
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
            #Tạo file vmx.lck
            create_config_file(vm_path, f"{vm_name}.vmx.lck", vmx_content)
            #Tạo file .nvram 
            create_config_file(vm_path,f"{vm_name}.nvram",generate_random_string(1024))
            #Tạo file vmsd
            create_config_file(vm_path,f"{vm_name}.vmsd",generate_random_string(1024))
            #Tạo file vswp
            create_config_file(vm_path,f"{vm_name}-{generate_random_string(5)}.vswp",generate_random_string(1024))




        elif vm_type == "Ubuntu":
            DataUbuntu = "S:\Summer2024\IAP491_G2\Code\Luaga\File_Example\Window 10.vmx"
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
            


    # Thư mục /tmp
    tmp_path = os.path.join(base_path, "tmp")
    tmp_content = generate_random_string(1024)
    create_config_file(tmp_path, "tmp_file.txt", tmp_content)

    # Thư mục /var/db/vmware
    var_db_vmware_path = os.path.join(base_path, "var", "db", "vmware")
    create_config_file(var_db_vmware_path, "vmInventory.db", "")
    create_config_file(var_db_vmware_path, "vpxd.db", "")


if __name__ == "__main__":
    create_esx_config_files()
    print("Các file cấu hình ESXi 7 đã được tạo thành công!")
    # while True:
    #     lua_chon = input("Bạn có muốn chạy chương trình? (Yes/No): ").lower()
    #     if lua_chon in ["Y","y"]:
    #         create_esx_config_files()
    #         print("Các file cấu hình ESXi 7 đã được tạo thành công!")
    #         break  # Thoát khỏi vòng lặp sau khi chạy
    #     elif lua_chon in ["N", "n"]:
    #         print("Đã hủy chạy chương trình.")
    #         break  # Thoát khỏi vòng lặp
    #     else:
    #         print("Lựa chọn không hợp lệ. Vui lòng nhập 'có' hoặc 'không'.")