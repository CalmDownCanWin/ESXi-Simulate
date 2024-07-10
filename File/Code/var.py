import os

from ESXi_config import create_directory
from ESXi_config import create_config_file
from ESXi_config import generate_random_string

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

    run = '/ESXI 7/var/run/'
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
        "log",
        "nonSchemaFiles",
        "sdrsInjector.pid",
        "storageRM.pid",
        "utmp",
    }
    for rfilen in r_file:
        create_config_file(run,rfilen,generate_random_string(1))

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