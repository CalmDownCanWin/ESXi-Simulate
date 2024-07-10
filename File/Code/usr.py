import os

from ESXi_config import create_directory
from ESXi_config import create_config_file
from ESXi_config import generate_random_string

def create_esx_usr(usr ="/ESXI 7/usr"):
    create_config_file(usr,"bin",generate_random_string(561))
    create_config_file(usr,"sbin",generate_random_string(561))

    lib64 = '/ESXI 7/usr/lib64/'
    create_directory(os.path.join(lib64,"cim"))

    create_config_file(os.path.join(lib64,"locale"),"locale-archive",generate_random_string(55))

    open = '/ESXI 7/usr/lib64/openwsman/'
    create_directory(os.path.join(open,"authenticators"))
    create_directory(os.path.join(open,"plugins"))

    vmw = '/ESXI 7/usr/lib64/vmware/'
    create_directory(vmw)

    li_file = {
        "libboost_atomic-gcc64-mt-x64-1_67.so.1.67.0": 51,
        "libboost_bzip2-gcc48-mt-1_55.so.1.55.0": 51,
        "libboost_bzip2-gcc48-mt-d-1_55.so.1.55.0": 51,
        "libboost_chrono-gcc64-mt-x64-1_67.so.1.67.0": 51,
        "libboost_context-gcc64-mt-x64-1_67.so.1.67.0": 51,
        "libboost_date_time-gcc64-mt-x64-1_67.so.1.67.0": 51,
        "libboost_filesystem-gcc64-mt-x64-1_67.so.1.67.0": 51,
        "libboost_iostreams-gcc64-mt-x64-1_67.so.1.67.0": 51,
        "libboost_log-gcc64-mt-x64-1_67.so.1.67.0": 51,
        "libboost_program_options-gcc64-mt-x64-1_67.so.1.67.0": 51,
        "libboost_python35-gcc64-mt-x64-1_67.so.1.67.0": 51,
        "libboost_regex-gcc64-mt-x64-1_67.so.1.67.0": 51,
        "libwsman_curl_client_transport.so.1": 51,
    }
    for lin,lis in li_file.items():
        create_config_file(lib64,lin,generate_random_string(lis))
    

    libexec = '/ESXI 7/usr/libexec/'
    create_config_file(libexec,"pci-info",generate_random_string(1))

    create_directory(os.path.join(libexec,"jumpstart","plugins"))
    create_directory(os.path.join(libexec,"jumpstart","plugins2"))

    create_directory(os.path.join(libexec,"vmwauth","lib64"))


    share = '/ESXI 7/usr/share/'
    sha_folder = {
        "certs",
        "doc",
        "esximage",
        "hwdata",
        "keymaps",
        "sensors",
        "syslinux",
        "terminfo",
        "weasel",
        "X11",
    }
    for shan in sha_folder:
        create_directory(os.path.join(share,shan))



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