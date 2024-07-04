import random
import os
import uuid
import datetime

from ESXi_config import generate_random_string
from ESXi_config import create_config_file
from ESXi_config import create_vmware_lic
from ESXi_config import create_vmdk_file
from ESXi_config import create_passwd_file
from ESXi_config import create_fake_datastore
from ESXi_config import create_hosts_file
from ESXi_config import create_ssh_keys
from ESXi_config import create_sshd_config
from ESXi_config import create_vmx_file
from ESXi_config import create_log_file
from ESXi_config import create_flat_vmdk
from ESXi_config import create_directory

def create_esx_bin(base_path="/ESXI 7/bin"):
    bin_file = {
        "[": 45,
        "[[": 4,
        "ash": 86,
        "amldump": 86,
        "apiForwarder": 454786,
        "apply-host-profiles": 4763,
        "applyHostProfile": 964,
        "applyHostProfileWrapper": 964,
        "authd": 964,
        "auto-backup": 964,
        "backup-check.sh": 964,
        "backup.sh": 964,
        "BootModuleConfig.sh": 964,
        "chardevlogger": 964,
        "check_serial": 964,
        "chkconfig": 964,
        "cim_host_powerops": 964,
        "cim-diagnostic.sh": 964,
        "cmmds-tool": 964,
        "crx-cli": 964,
        "crypto-util": 964,
        "dcbd": 964,
        "dcui": 964,
        "dcuiweasel": 964,
        "df": 964,
        "dhclient-uw": 964,
        "dmesg": 45,
        "doat": 248,
        "dosfsck": 14,
        "enum_instances": 426,
        "esxcfg-advcfg": 64,
        "esxcfg-dumppart": 913,
        "esxcfg-info": 28,
        "esxcfg-init": 46,
        "esxcfg-ipsec": 123,
        "esxcfg-module": 486,
        "mpath": 746,
        "esxcli.py": 964,
        "esxhpcli": 54,
        "esxhpedit": 524,
        "esxupdate": 456,
        "firmwareConfig.py": 964,
        "generate-certificates": 426,
        "getAccessToken": 123,
        "grabCIMData": 453,
        "host_reboot.sh": 530,
        "host_shutdown.sh": 264,
        "hostd-probe.sh": 432,
        "init-launcher": 44,
        "initSystemStorage": 145,
        "initterm.sh": 1768,
        "install": 34,
        "lldpnetmap": 43,
        "loadESXEnable": 176,
        "lockfile": 425,
        "netdbg.py": 2351,
        "nologin": 453,
        "pmemGC": 453,
        "powerOffVms": 12,
        "schedsnapshot": 335,
        "services.sh": 452,
        "sharedStorageHostProfile.sh": 52,
        "shutdown.sh": 12,
        "slpd": 954,
        "smartd": 921,
        "sntp": 453,
        "storageRM": 454,
        "summarize-dvfilter": 243,
        "techsupport.sh": 453,
        "tmpwatch.py": 475,
        "vm-support": 452,
        "vmfs-support": 452,
        "vmfsfilelockinfo": 4,
        "VmfsLatencyStats.py": 964,
        "vmware-autostart.sh": 94,
        "vmware-vimdump": 64,
        "vmx": 58,
        "vmx-buildtype": 96,
        "vprobe": 527,
        "watchdog.sh": 964,
    }

    for name, size in bin_file.items():
        create_config_file(base_path,name,generate_random_string(size))



def create_esx_dev(base_path="/ESXI 7/dev"):
    cbt_path = os.path.join(base_path,"cbt")
    create_config_file(cbt_path,"control",generate_random_string(15))

    cdrom_path = '/ESXI 7/dev/cdrom/'
    create_directory(cdrom_path)

    char_devmgr_path = '/ESXI 7/dev/char/devmgr/'
    char_mem_path = '/ESXI 7/dev/char/mem/'
    char_pty_path = '/ESXI 7/dev/char/pty/'
    char_scsi_trace_path = '/ESXI 7/dev/char/scsi-trace/'
    char_serial_path = '/ESXI 7/dev/char/serial/'
    char_tty_path = '/ESXI 7/dev/char/tty/'
    char_vmkdriver_path = '/ESXI 7/dev/char/vmkdriver/'
    char_vob_path = '/ESXI 7/dev/char/vob/'
    char_vscsi_filters_path = '/ESXI 7/dev/char/vscsi-filters/'
    char_vsoc_path = '/ESXI 7/dev/char/vsoc/'
    create_directory(char_devmgr_path)
    create_directory(char_mem_path)
    create_directory(char_pty_path)
    create_directory(char_scsi_trace_path)
    create_directory(char_serial_path)
    create_directory(char_tty_path)
    create_directory(char_vmkdriver_path)
    create_directory(char_vob_path)
    create_directory(char_vscsi_filters_path)
    create_directory(char_vsoc_path)

    deltadisks_path = os.path.join(base_path,"deltadisks")
    create_config_file(deltadisks_path,"control",generate_random_string(15))

    disks_path = os.path.join(base_path,"disks")
    Disks = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\dev_disks.txt"
    with open(Disks, 'r', encoding='utf-8') as f:
        disks_content = f.read()  # Đọc nội dung file vào biến chuỗi
    create_config_file(disks_path,"disks",disks_content)

    PMemDisk_path = '/ESXI 7/dev/PMemDisk'
    PMemDS_path = '/ESXI 7/dev/PMemDS'
    PMemNamespaces_path = '/ESXI 7/dev/PMemNamespaces'
    PMemVolumes_path = '/ESXI 7/dev/PMemVolumes'
    vflash_path = '/ESXI 7/dev/vflash'
    create_directory(PMemDisk_path)
    create_directory(PMemDS_path)
    create_directory(PMemNamespaces_path)
    create_directory(PMemVolumes_path)
    create_directory(vflash_path)

def create_esx_etc(base_path="/ESXI 7"):
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
    Datashadow = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\shadow"
    with open(Datashadow, 'r', encoding='utf-8') as f:
        content_shadow = f.read()  # Đọc nội dung file vào biến chuỗi 
    create_config_file(etc_path,"shadow",content_shadow)
    create_config_file(etc_path,"rc.local",generate_random_string(50))

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

def create_esx_include(base_path="/ESXI 7/include"):
    include_path = os.path.join(base_path,"python3.8")
    create_config_file(include_path,"pyconfig.h",generate_random_string(1024))

def create_esx_lib(security_path="/ESXI 7/lib/security"):
    create_directory(security_path)

def create_esx_lib64():
    pcsc_path = '/ESXI 7/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/'
    pcsc_linux_path = '/ESXI 7/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Linux/'
    create_config_file(pcsc_path,"Info.plist",generate_random_string(1024))
    create_config_file(pcsc_linux_path,"libccid.so",generate_random_string(1024))

    python3_5_path = '/ESXI 7/lib64/python3.5/site-packages/loadesxLive/borautils/'
    create_config_file(python3_5_path,"elfbin.pyc",generate_random_string(14))
    create_config_file(python3_5_path,"exception.pyc",generate_random_string(1))
    create_config_file(python3_5_path,"libelf.so",generate_random_string(130))

    python_load_path = '/ESXI 7/lib64/python3.5/site-packages/loadesxLive/'
    create_config_file(python_load_path,"__init__.pyc",generate_random_string(1024))
    create_config_file(python_load_path,"bootInfo.pyc",generate_random_string(1024))
    create_config_file(python_load_path,"common.pyc",generate_random_string(1024))
    create_config_file(python_load_path,"device.pyc",generate_random_string(1024))
    create_config_file(python_load_path,"driverList.pyc",generate_random_string(1024))
    create_config_file(python_load_path,"kernel.pyc",generate_random_string(1024))
    create_config_file(python_load_path,"runLoadEsx.pyc",generate_random_string(1024))
    create_config_file(python_load_path,"secureBoot.pyc",generate_random_string(1024))
    create_config_file(python_load_path,"stmCompList.pyc",generate_random_string(1024))
    create_config_file(python_load_path,"utils.pyc",generate_random_string(1024))
    create_config_file(python_load_path,"vimutils.pyc",generate_random_string(1024))

    python_vmware_path = '/ESXI 7/lib64/python3.5/site-packages/vmware/'
    create_config_file(python_vmware_path,"esximage",generate_random_string(1024))
    
def create_esx_opt():
    opt_nvme = '/ESXI 7/opt/vmware/nvme/'
    create_config_file(opt_nvme,"esxcli-nvme-plugin",generate_random_string(1024))

    opt_vmware = '/ESXI 7/opt/vmware/vpxa/vpx/'
    create_config_file(opt_vmware,"bundleversion.xml",generate_random_string(1024))
    create_config_file(opt_vmware,"vpxResultFilter.xml",generate_random_string(1024))

def create_esx_proc(proc="/ESXI 7/proc/"):
    create_directory(proc)


def create_esx_tardisks(tardisks_path='/ESXI 7/tardisks/'):
    """Tạo thư mục và file giả mạo trong /tardisks."""
    os.makedirs(tardisks_path, exist_ok=True)

    # File metadata giả mạo
    metadata_content = f"""
    {{
        "created": "{datetime.datetime.now().isoformat()}",
        "patches": [
            {{
                "name": "fake-patch-1",
                "version": "1.2.3",
                "status": "installed"
            }},
            {{
                "name": "fake-patch-2",
                "version": "4.5.6",
                "status": "staged"
            }}
        ]
    }}
    """
    create_config_file(tardisks_path, "metadata.json", metadata_content)
    # File patch giả mạo
    create_config_file(tardisks_path, "fake-patch-1.vib", generate_random_string(1024))

    # Các file giả mạo ESXi
    esxi_files = {
        "atlantic.v00": 1414,
        "basemisc.tgz": 11430,
        "bnxtnet.v00": 919,
        "brcmfcoe.v00": 2227,
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
    for filename, size in esxi_files.items():
        create_config_file(tardisks_path, filename, generate_random_string(size))

def create_esx_tardisks_noauto(base_path="/ESXI 7"):
    noauto = '/ESXI 7/tardisks_noauto/'
    create_directory(noauto)

def create_esx_tmp():
    tmp_folder = {
        '/ESXI 7/tmp/vmware-root/',
        '/ESXI 7/tmp/vmware-root_68260-1619746241/',
        '/ESXI 7/tmp/vmware-uid_0/',
        '/ESXI 7/tmp/vmware-root_85464_5645446546/',
        '/ESXI 7/tmp/vmware-root_54545_8454548451/',
    }
    for path in tmp_folder:
        create_directory(path)


def create_esx_usr(usr ="/ESXI 7/usr"):
    create_config_file(usr,"bin",generate_random_string(561))
    create_config_file(usr,"sbin",generate_random_string(561))

    lib64 = '/ESXI 7/usr/lib64/'
    create_directory(lib64)

    libexec = '/ESXI 7/usr/libexec/'
    create_directory(libexec)


    share = '/ESXI 7/usr/share/'
    create_directory(share)



    lib = os.path.join(usr,"lib")
    create_config_file(lib,"libboost_zlib-gcc48-mt-1_55.so.1.55.0",generate_random_string(1024))
    create_config_file(lib,"libboost_zlib-gcc48-mt-d-1_55.so.1.55.0",generate_random_string(1024))

    lib_ssl = os.path.join(usr,"lib","ssl")
    create_config_file(lib_ssl,"cert.pem",generate_random_string(2541))
    create_config_file(lib_ssl,"certs",generate_random_string(2541))
    create_config_file(lib_ssl,"openssl.cnf",generate_random_string(2541))

    lib_vmware = os.path.join(usr,"lib","vmware")
    create_config_file(lib_vmware,"esxcli-software",generate_random_string(545))

    lib_locale = os.path.join(usr,"lib","locale")
    create_config_file(lib_locale,"locale-archive",generate_random_string(954))

def create_esx_var(base_path="/ESXI 7/var"):
    esximg = '/ESXI 7/var/db/esximg/'
    create_directory(esximg)

    payload = '/ESXI 7/var/db/payloads/'
    create_directory(payload)

    vm = '/ESXI 7/var/lib/vmware/'
    create_directory(vm)

    sfcb = '/ESXI 7/var/lib/sfcb/registration/'
    create_directory(sfcb)

    installer = '/ESXI 7/var/lib/initenvs/installer/'
    create_directory(installer)

    dhcp = '/ESXI 7/var/lib/dhcp/'
    create_directory(dhcp)

    token = '/ESXI 7/var/lock/eToken/'
    create_directory(token)

    lock = '/ESXI 7/var/lock/iscsi/'
    create_config_file(lock,"lock",generate_random_string(55))

    opt = '/ESXI 7/var/opt/'
    create_directory(opt)

    cron = '/ESXI 7/var/spool/cron/crontabs/'
    create_config_file(cron,".#root",generate_random_string(65))
    create_config_file(cron,"root",generate_random_string(65))

    # Thư mục /var/log/vmware
    log_vmware = '/ESXI 7/var/log/vmware/journal/'
    create_directory(log_vmware)

    log_path = '/ESXI 7/var/log/'
    log_file = {
        ".vmsyslogd.err": 1,
        "apiForwarder.log": 50,
        "attestd.log": 30,
        "auth.log": 25,
        "boot.gz": 65,
        "clusterAgent.log": 1,
        "cmmdsd.log": 1,
        "cmmdsTimeMachine.log": 1,
        "cmmdsTimeMachineDump.log": 1,
        "configRP.log": 52,
        "configstore-boot.log": 12,
        "dhclient.log": 1,
        "dpd.log": 1,
        "esxcli.log": 1,
        "epd.log": 1,
        "esxgdpd.log": 1,
        "esxtokend.log": 1,
        "esxupdate.log": 1,
        "hostd.log": 1,
        "init.log": 1,
        "vmkernel.log": 1,
    }
    for filename, size in log_file.items():
        create_config_file(log_path,filename,generate_random_string(size))
    
    var_file = {
        "cache": 56,
        "core": 45,
        "tmp": 65,
        "vmware":32,
    }
    for name, varsize in var_file.items():
        create_config_file(base_path,name,generate_random_string(varsize))



    # Thư mục /var/db/vmware
    var_db_vmware_path = os.path.join(base_path, "db", "vmware")
    create_config_file(var_db_vmware_path, "vmInventory.db", "")
    create_config_file(var_db_vmware_path, "vpxd.db", "")

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
    create_config_file(bootbank_path,f"OSDATA-{str(uuid.uuid4())}",content)

    #Tạo các folder với tên uuid 


    #Thư mục vmfs/devices
    device_path = os.path.join(base_path,"vmfs")
    devices_content = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\device.txt"
    with open(devices_content, 'r', encoding='utf-8') as f:
        data_devices_content = f.read()  # Đọc nội dung file vào biến chuỗi
    create_config_file(device_path,"devices",data_devices_content)

    # Tạo cấu trúc máy ảo Windows, Kali-Linux và Ubuntu
    domain = "example.com"
    for _ in range(10):
        # Chọn ngẫu nhiên loại máy ảo
        vm_type = random.choice(["Windows", "Kali-Linux","Ubuntu"])
        vm = "Window"
        vm_name = f"{vm_type}"
        version_window = random.choice(["7","8","10","11"])
        number = f"{version_window}"
        vm_name_Window = f"{vm_type}_{number}"
        name = "vmware"

        # Tạo thư mục VM
        if vm == "Window":
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



        elif vm_type == "Kali-Linux":
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
            
def create_esx_vmimages(vmimages ="/ESXI 7/vmimages"):
    create_config_file(vmimages,"floppies",generate_random_string(15))
    create_config_file(vmimages,"tools-isoimages",generate_random_string(15))

def create_esx_config_files(base_path="/ESXI 7"):
    """Tạo các file cấu hình ESXi 7."""

#Tạo file trong thư mục chính 
    Databootbank_1 = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\BOOTBANK1.txt"
    with open(Databootbank_1, 'r', encoding='utf-8') as f:
        boot_cfg_content_1 = f.read()  # Đọc nội dung file vào biến chuỗi
    create_config_file(base_path,"bootbank",boot_cfg_content_1)

    create_config_file(base_path,".#encryption.info",generate_random_string(2))
    create_config_file(base_path,".mtoolsrc",generate_random_string(2))
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


if __name__ == "__main__":
    create_esx_config_files()
    create_esx_bin()
    create_esx_dev()
    create_esx_etc()
    create_esx_include()
    create_esx_lib()
    create_esx_lib64()
    create_esx_opt()
    create_esx_proc()
    create_esx_tardisks()
    create_esx_tardisks_noauto()
    create_esx_tmp()
    create_esx_usr()
    create_esx_var()
    create_esx_vmfs()
    create_esx_vmimages()
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
