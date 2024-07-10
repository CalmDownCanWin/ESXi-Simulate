import os 
import random
import uuid

from ESXi_config import create_config_file
from ESXi_config import create_directory
from ESXi_config import create_ssh_keys
from ESXi_config import create_sshd_config
from ESXi_config import create_hosts_file
from ESXi_config import create_vmware_lic
from ESXi_config import create_passwd_file
from ESXi_config import generate_random_string

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

    config = '/ESXI 7/etc/config/EMU/mili/'
    create_config_file(config,"intr_logopts.txt",generate_random_string(5284))
    create_config_file(config,"savestp.txt",generate_random_string(5284))
    create_config_file(config,"savetgt.txt",generate_random_string(5284))

    init = '/ESXI 7/etc/init.d/'
    init_file = {
        "apiForwarder": 654,
        "attestd": 758,
        "cdp": 52,
        "clomd": 2,
        "cmmdsd": 452,
        "cmmdsTimeMachine": 24,
        "dcbd": 24,
        "DCUI": 52,
        "dpd": 452,
        "epd": 52,
        "esxgdpd": 5,
        "ESXShell": 52,
        "esxTokenCPS": 52,
        "esxui": 52,
        "fsvmsockrelay": 3,
        "gstored": 38,
        "health": 57,
        "hostd": 82,
        "hostdCgiServer": 8,
        "iofilterd-spm": 8,
        "iofilterd-vmwarevmcrypt": 2,
        "iofiltervpd": 28,
        "kmxa": 75,
        "kmxd": 52,
        "lacp": 58,
        "lbtd": 53,
        "loadESX": 1,
        "lsud": 158,
        "lwsmd": 15,
        "nicmgmtd": 4,
        "pmemGarbageCollection": 14,
        "sfcbd-watchdog": 1,
        "vsandevicemonitord": 633,
        "vsanmgmtd": 85,
        "vsanObserver": 7,
        "vsantraced": 599,
        "vvold": 18,
        "wsman": 15,
        "xorg": 85,
    }
    for initname, initsize in init_file.items():
        create_config_file(init,initname,generate_random_string(initsize))

    etc_file = {
        ".#chkconfig.db": 54,
        ".#dhclient-vmk0.leases": 62,
        ".#krb5.conf": 693,
        ".#random-seed": 54,
        "banner": 54,
        "chkconfig.db": 54,
        "dhclient-vmk0.conf": 54,
        "dhclient-vmk0.leases": 5045,
        "dhclient6-vmk0.conf": 54,
        "dhclient6-vmk0.leases": 54,
        "environment": 54,
        "eToken.conf": 54,
        "group": 54,
        "host.conf": 54,
        "profile": 54,
        "inittab": 54,
        "issue": 54,
        "krb5.conf": 54,
        "krb5.keytab": 54,
        "localtime": 54,
        "motd": 54,
        "nscd.conf": 54,
        "nsswitch.conf": 54,
        "ntp.conf": 54,
        "ntp.drift": 54,
        "ntp.keys": 54,
        "passwdqc.conf": 54,
        "profile.local": 54,
        "protocols": 5459,
        "ptp.conf": 54,
        "random-seed": 54,
        "resolv.conf": 54,
        "services": 20584,
        "SHAC_Config.ini": 54,
        "shells": 54,
        "slp.reg": 54,
        "vmotion-resolv.conf": 54,
        "vmsyslog.conf": 54,
        "vSphereProvisioning-resolv.conf": 54,
    }
    for etcname,etcsize in etc_file.items():
        create_config_file(etc_path,etcname,generate_random_string(etcsize))

    vmsyslog = '/ESXI 7/etc/vmsyslog.conf.d/'
    for initname, initsize in init_file.items():
        create_config_file(vmsyslog,initname,generate_random_string(initsize))


    like = '/ESXI 7/etc/likewise/'
    create_directory(like)

    openw = '/ESXI 7/etc/openwsman/'
    create_config_file(openw,"identify.xml",generate_random_string(54))
    create_config_file(openw,"openwsman.conf.tmpl",generate_random_string(54))
    create_config_file(openw,"owsmangencert.sh",generate_random_string(54))
    create_config_file(openw,"subscriptions",generate_random_string(54))

    opt = '/ESXI 7/etc/opt/'
    create_directory(opt)

    pam_tem = '/ESXI 7/etc/pam.d/template/'
    create_directory(pam_tem)

    pam = '/ESXI 7/etc/pam.d/'
    pam_file = {
        "daemondk": 12,
        "dcui": 12,
        "hostd-cgi": 12,
        "login": 12,
        "openwsman": 12,
        "other": 12,
        "settingsd": 12,
        "passwd": 12,
        "settingsd": 12,
        "system-auth-generic": 12,
        "vmtoolsd": 12,
        "vmware-authd": 12,
    }
    for pamname,pamsize in pam_file.items():
        create_config_file(pam,pamname,generate_random_string(pamsize))


    rc = '/ESXI 7/etc/rc.local.d/'
    rc_file = {
        "009.vsanwitness.sh": 15,
        "cleanupStatefulHost.py": 15,
        "kickstart.py": 15,
        "local.sh": 15,
        "psaScrub.py": 15,
    }
    for rcname,rcsize in rc_file.items():
        create_config_file(rc,rcname,generate_random_string(rcsize))
    
    se = '/ESXI 7/etc/security/'
    se_file = {
        ".#access.conf": 13,
        "access.conf": 13,
        "dcui-access.conf": 13,
        "opasswd": 13,
        "pam_env.conf": 13,
        "ssh_limits.conf": 13,
    }
    for sename,sesze in se_file.items():
        create_config_file(se,sename,generate_random_string(sesze))

    sfcb = '/ESXI 7/etc/sfcb/'
    create_config_file(sfcb,"repository",generate_random_string(12))
    create_config_file(sfcb,"sfcb.cfg",generate_random_string(12))
    create_config_file(os.path.join(sfcb,"omc"),"sensor_health",generate_random_string(12))

    shut = '/ESXI 7/etc/shutdown.d/'
    create_config_file(shut,"iofilterd-spm",generate_random_string(13))
    create_config_file(shut,"iofilterd-vmwarevmcrypt",generate_random_string(13))

    vmt = '/ESXI 7/etc/vmware-tools/'
    vmt_file = {
        "poweroff-vm-default": 354,
        "poweron-vm-default": 354,
        "resume-vm-default": 354,
        "statechange.subr": 10,
        "suspend-vm-default": 354,
        "tools.conf": 10,
    }
    for vmtn,vmts in vmt_file.items():
        create_config_file(vmt,vmtn,generate_random_string(vmts))

    com = '/ESXI 7/etc/vmware-tools/plugins/common/'
    create_directory(com)

    vmsvc = '/ESXI 7/etc/vmware-tools/plugins/vmsvc/'
    create_directory(vmsvc)

    script = '/ESXI 7/etc/vmware-tools/script-data/'
    create_directory(script)

    vmware = '/ESXI 7/etc/vmware-tools/scripts/vmware/'
    create_config_file(vmware,"network",generate_random_string(25))

    X11 = '/ESXI 7/etc/X11/'
    create_config_file(X11,"server.xkm",generate_random_string(1035))
    create_config_file(X11,"xorg.conf",generate_random_string(10))
