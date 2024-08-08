import os

from ESXi_config import create_config_file
from ESXi_config import generate_random_string
from ESXi_config import create_directory

def create_esx_dev(base_path):
    dev_file = {
        "cdp": 13,
        "console": 13,
        "cswitch": 13,
        "dmesg": 13,
        "dvfilter-generic-vmware": 13,
        "dvfiltertbl": 13,
        "dvsdev": 13,
        "ens_rep": 13,
        "generic": 13,
        "hyperclock": 13,
        "iodm": 13,
        "kbdmap": 13,
        "klog": 13,
        "lacp": 13,
        "null": 13,
        "nvdManagement": 13,
        "port": 13,
        "ptmx": 13,
        "random": 13,
        "shm": 13,
        "sunrpc-gss": 13,
        "TraceStreamVMFS": 13,
        "tty": 13,
        "tty1": 13,
        "tty2": 13,
        "tty3": 13,
        "tty4": 13,
        "ttyp0": 13,
        "urandom": 13,
        "usb0101": 13,
        "usb0201": 13,
        "usbdevices": 13,
        "usbpassthrough": 13,
        "vmwMgmtInfo": 13,
        "vmwMgmtNode0": 13,
        "vmwMgmtNode1": 13,
        "vmwMgmtNode2": 13,
        "vprobe": 13,
        "vsock": 13,
        "zero": 13,
    }
    for devn,devs in dev_file.items():
        create_config_file(os.path.join(base_path,"dev"),devn,generate_random_string(devs))

    cbt_path = os.path.join(base_path,"dev","cbt")
    create_config_file(cbt_path,"control",generate_random_string(15))

    cdrom_path = os.path.join(base_path,"dev","cdrom")
    create_directory(cdrom_path)

    char_devmgr_path = os.path.join(base_path,"dev","char","devmgr")
    create_directory(char_devmgr_path)

    char_mem_path = os.path.join(base_path,"dev","char","mem")
    create_directory(char_mem_path)

    char_pty_path = os.path.join(base_path,"dev","char","pty")
    create_directory(char_pty_path)

    char_scsi_trace_path = os.path.join(base_path,"dev","char","scsi-trace")
    create_directory(char_scsi_trace_path)

    char_serial_path = os.path.join(base_path,"dev","char","serial")
    create_directory(char_serial_path)

    char_tty_path = os.path.join(base_path,"dev","char","tty")
    create_directory(char_tty_path)

    char_vmkdriver_path = os.path.join(base_path,"dev","char","vmkdriver")
    create_directory(char_vmkdriver_path)

    char_vob_path = os.path.join(base_path,"dev","char","vob")
    create_directory(char_vob_path)

    char_vscsi_filters_path = os.path.join(base_path,"dev","char","vscsi-filters")
    create_directory(char_vscsi_filters_path)

    char_vsoc_path = os.path.join(base_path,"dev","char","vsoc")
    create_directory(char_vsoc_path)

    deltadisks_path = os.path.join(base_path,"dev","deltadisks")
    create_config_file(deltadisks_path,"control",generate_random_string(15))

    disks_path = os.path.join(base_path,"dev","disks")
    Disks = "dev_disks.txt"
    with open(Disks, 'r', encoding='utf-8') as f:
        disks_content = """t10.NVMe____VMware_Virtual_NVMe_Disk________________VMWare_NVME_0000____00000001
t10.NVMe____VMware_Virtual_NVMe_Disk________________VMWare_NVME_0000____00000001:1
t10.NVMe____VMware_Virtual_NVMe_Disk________________VMWare_NVME_0000____00000001:5
t10.NVMe____VMware_Virtual_NVMe_Disk________________VMWare_NVME_0000____00000001:6
t10.NVMe____VMware_Virtual_NVMe_Disk________________VMWare_NVME_0000____00000001:7
t10.NVMe____VMware_Virtual_NVMe_Disk________________VMWare_NVME_0000____00000002
t10.NVMe____VMware_Virtual_NVMe_Disk________________VMWare_NVME_0000____00000002:1
vml.0100000000564d57617265204e564d455f3030303020202020564d77617265
vml.0100000000564d57617265204e564d455f3030303020202020564d77617265:1
vml.0100000000564d57617265204e564d455f3030303020202020564d77617265:5
vml.0100000000564d57617265204e564d455f3030303020202020564d77617265:6
vml.0100000000564d57617265204e564d455f3030303020202020564d77617265:7
vml.0100010000564d57617265204e564d455f3030303020202020564d77617265
vml.0100010000564d57617265204e564d455f3030303020202020564d77617265:1
vml.054e8c490ab3972791eb04c40b0ddf7bdc9eee19d2dd723d9fc1899f2635ce12b9
vml.054e8c490ab3972791eb04c40b0ddf7bdc9eee19d2dd723d9fc1899f2635ce12b9:1
vml.054e8c490ab3972791eb04c40b0ddf7bdc9eee19d2dd723d9fc1899f2635ce12b9:5
vml.054e8c490ab3972791eb04c40b0ddf7bdc9eee19d2dd723d9fc1899f2635ce12b9:6
vml.054e8c490ab3972791eb04c40b0ddf7bdc9eee19d2dd723d9fc1899f2635ce12b9:7
vml.05b201b1046b6c89868bbf6b9bbfd8f6222039d774429467ef0ca1d2a1e43e52eb
vml.05b201b1046b6c89868bbf6b9bbfd8f6222039d774429467ef0ca1d2a1e43e52eb:1"""
    create_config_file(disks_path,"disks",disks_content)

    PMemDisk_path = os.path.join(base_path,"dev","PMemDisk")
    create_directory(PMemDisk_path)

    PMemDS_path = os.path.join(base_path,"dev","PMemDS")
    create_directory(PMemDS_path)

    PMemNamespaces_path = os.path.join(base_path,"dev","PMemNamespaces")
    create_directory(PMemNamespaces_path)

    PMemVolumes_path = os.path.join(base_path,"dev","PMemVolumes")
    create_directory(PMemVolumes_path)

    vflash_path = os.path.join(base_path,"dev","vflash")
    create_directory(vflash_path)
