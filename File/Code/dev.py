import os

from ESXi_config import create_config_file
from ESXi_config import generate_random_string
from ESXi_config import create_directory

def create_esx_dev(base_path="/ESXI 7/dev"):
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
        create_config_file(base_path,devn,generate_random_string(devs))

    cbt_path = os.path.join(base_path,"cbt")
    create_config_file(cbt_path,"control",generate_random_string(15))

    cdrom_path = '/ESXI 7/dev/cdrom/'
    create_directory(cdrom_path)

    char_devmgr_path = '/ESXI 7/dev/char/devmgr/'
    create_directory(char_devmgr_path)

    char_mem_path = '/ESXI 7/dev/char/mem/'
    create_directory(char_mem_path)

    char_pty_path = '/ESXI 7/dev/char/pty/'
    create_directory(char_pty_path)

    char_scsi_trace_path = '/ESXI 7/dev/char/scsi-trace/'
    create_directory(char_scsi_trace_path)

    char_serial_path = '/ESXI 7/dev/char/serial/'
    create_directory(char_serial_path)

    char_tty_path = '/ESXI 7/dev/char/tty/'
    create_directory(char_tty_path)

    char_vmkdriver_path = '/ESXI 7/dev/char/vmkdriver/'
    create_directory(char_vmkdriver_path)

    char_vob_path = '/ESXI 7/dev/char/vob/'
    create_directory(char_vob_path)

    char_vscsi_filters_path = '/ESXI 7/dev/char/vscsi-filters/'
    create_directory(char_vscsi_filters_path)

    char_vsoc_path = '/ESXI 7/dev/char/vsoc/'
    create_directory(char_vsoc_path)

    deltadisks_path = os.path.join(base_path,"deltadisks")
    create_config_file(deltadisks_path,"control",generate_random_string(15))

    disks_path = os.path.join(base_path,"disks")
    Disks = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\dev_disks.txt"
    with open(Disks, 'r', encoding='utf-8') as f:
        disks_content = f.read()  # Đọc nội dung file vào biến chuỗi
    create_config_file(disks_path,"disks",disks_content)

    PMemDisk_path = '/ESXI 7/dev/PMemDisk'
    create_directory(PMemDisk_path)

    PMemDS_path = '/ESXI 7/dev/PMemDS'
    create_directory(PMemDS_path)

    PMemNamespaces_path = '/ESXI 7/dev/PMemNamespaces'
    create_directory(PMemNamespaces_path)

    PMemVolumes_path = '/ESXI 7/dev/PMemVolumes'
    create_directory(PMemVolumes_path)

    vflash_path = '/ESXI 7/dev/vflash'
    create_directory(vflash_path)