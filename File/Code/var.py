import os
import random

from ESXi_config import create_directory
from ESXi_config import create_config_file
from ESXi_config import generate_random_string
# from ESXi_config import generate_log_entry
from ESXi_config import create_symlinks




def create_esx_var(base_path= os.path.join(os.path.expanduser("~"), "ESXI 7","var")):
    esximg = os.path.join(os.path.expanduser("~"), "ESXI 7","var","db","esximg")
    create_directory(esximg)

    payload = os.path.join(os.path.expanduser("~"), "ESXI 7","var","db","payloads")
    create_directory(payload)

    vm = os.path.join(os.path.expanduser("~"), "ESXI 7","var","lib","vmware")
    create_config_file(os.path.join(vm,"osdata"),"locker",generate_random_string(2))
    create_config_file(os.path.join(vm,"osdata"),"store",generate_random_string(2))

    sfcb = os.path.join(os.path.expanduser("~"), "ESXI 7","var","lib","sfcb","registration")
    create_directory(sfcb)

    installer = os.path.join(os.path.expanduser("~"), "ESXI 7","var","lib","initenvs","installer")
    create_directory(installer)

    dhcp = os.path.join(os.path.expanduser("~"), "ESXI 7","var","lib","dhcp")
    create_directory(dhcp)

    token = os.path.join(os.path.expanduser("~"), "ESXI 7","var","lock","eToken")
    create_directory(token)

    lock = os.path.join(os.path.expanduser("~"), "ESXI 7","var","lock","iscsi")
    create_config_file(lock,"lock",generate_random_string(55))

    opt = os.path.join(os.path.expanduser("~"), "ESXI 7","var","opt")
    create_directory(opt)

    run = os.path.join(os.path.expanduser("~"), "ESXI 7","var","run")
    r_folder = {
        "crx",
        "iofilters",
        "nscd",
        "shm",
        "vmware",
        "vmware-hostd-ticket",
    }
    for rfoldern in r_folder:
        create_directory(os.path.join(run,rfoldern))

    r_file = {
        ".#inetd.conf",
        "bootTime",
        "crond.pid",
        "dcui.pid",
        "dhcp-vmk0.pid",
        "inetd.conf",
        "inetd.pid",
        "nonSchemaFiles",
        "sdrsInjector.pid",
        "storageRM.pid",
        "utmp",
    }
    for rfilen in r_file:
        create_config_file(run,rfilen,generate_random_string(1))

    run_symlinks = {"log": "/scratch/log",}
    create_symlinks(run,run_symlinks)

    cron = os.path.join(os.path.expanduser("~"), "ESXI 7","var","spool","cron","crontabs")
    create_config_file(cron,".#root",generate_random_string(65))
    create_config_file(cron,"root",generate_random_string(65))

    # Thư mục /var/log/vmware
    log_vmware = os.path.join(os.path.expanduser("~"), "ESXI 7","var","log","vmware","journal")
    create_directory(log_vmware)

    log_path = os.path.join(os.path.expanduser("~"), "ESXI 7","var","log")
    log_file = {
        ".vmsyslogd.err": 1,
        "apiForwarder.log": 50,
        "attestd.log": 30,
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
        "kickstart.log": 1,
        "loadESX.log": 1,
        "nfcd.log": 1,
        "osfsd.log": 1,
        "rhttpproxy.log": 1,
        "sandboxd.log": 1,
        "settingsd.log": 1,
        "shell.log": 1,
        "sysboot.log": 1,
        "vmauthd.log": 1,
        "vmkernel.log": 1,
        "vmkwarning.log": 1,
        "vsanEsxcli.log": 1,
        "vsanesxcmd.log": 1,
        "vsanfs.configdump.log": 1,
        "vsanfs.mgmt.log": 1,
        "vvold.log": 1,
        "vmware-vmtoolsd-root.log": 1,
        "vmware-vmsvc-root.log": 1,
        "vpxa.log": 1,
        "vsananalyticsevents.log": 1,
        "vsandevicemonitord.log": 1,
        "vsansystem.log": 1,
        "vdfsd-proxy.log": 1,
        "sysboot.log": 1,
        "syslog.log": 1,
        "usb.log": 1,
        "vltd.log": 1,
        "vvold.log": 1,
        "Xorg.log": 1,
    }
    for filename, size in log_file.items():
        create_config_file(log_path,filename,generate_random_string(size))
    
    my_symlinks = {
        "cache": "/var/lib/vmware/osdata/cache",
        "core": "/scratch/core",
        "tmp": "/scratch/var/tmp/",
        "vmware": "/scratch/vmware",
    }
    
    create_symlinks(base_path,my_symlinks)



    # Thư mục /var/db/vmware
    var_db_vmware_path = os.path.join(base_path, "db", "vmware")
    create_config_file(var_db_vmware_path, "vmInventory.db", "")
    create_config_file(var_db_vmware_path, "vpxd.db", "")