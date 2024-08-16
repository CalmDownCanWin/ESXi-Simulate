import os

from ESXi_config import create_directory
from ESXi_config import create_config_file
from ESXi_config import generate_random_string
# from ESXi_config import create_symlinks

def create_esx_usr(base_path):
    usr = os.path.join(base_path,"usr")
#File in folder usr
    create_config_file(usr,"bin",generate_random_string(1))
    create_config_file(usr,"sbin",generate_random_string(1))

    # my_symlinks = {
    #     "bin": "/bin",
    #     "sbin": "/bin",
    #     }
    # create_symlinks(usr,my_symlinks)

#Folder /usr/lib
    lib = os.path.join(usr,"lib")
    create_config_file(lib,"libboost_zlib-gcc48-mt-1_55.so.1.55.0",generate_random_string(1024))
    create_config_file(lib,"libboost_zlib-gcc48-mt-d-1_55.so.1.55.0",generate_random_string(1024))
    #Folder ssl
    lib_ssl = os.path.join(lib,"ssl")
    create_config_file(lib_ssl,"cert.pem",generate_random_string(2541))
    create_config_file(lib_ssl,"certs",generate_random_string(2541))
    create_config_file(lib_ssl,"openssl.cnf",generate_random_string(2541))
    #Folder vmware
    lib_vmware = os.path.join(lib,"vmware")
    create_config_file(lib_vmware,"esxcli-software",generate_random_string(545))
    #Create file /usr/lib/vmware/hostd/docroot/ui/index.html
    ui = os.path.join(usr,"lib","vmware","hostd","docroot","ui")
    create_config_file(ui,"index.html",generate_random_string(1024))

    #Folder locale
    lib_locale = os.path.join(lib,"locale")
    create_config_file(lib_locale,"locale-archive",generate_random_string(954))

    #Folder hostprofiles
    create_config_file(os.path.join(usr,"lib","hostprofiles"),"locale",generate_random_string(10))
    create_config_file(os.path.join(usr,"lib","hostprofiles"),"plugins",generate_random_string(10))


#Folder /usr/lib64/
    lib64 = os.path.join(usr,"lib64")
    create_directory(os.path.join(lib64,"cim"))

    create_config_file(os.path.join(lib64,"locale"),"locale-archive",generate_random_string(55))

    open = os.path.join(usr,"lib64","openwsman")
    create_directory(os.path.join(open,"authenticators"))
    create_directory(os.path.join(open,"plugins"))

    vmw = os.path.join(usr,"lib64","vmware")
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
    
#Folder /usr/libexec
    libexec = os.path.join(usr,"libexec")
    create_config_file(libexec,"pci-info",generate_random_string(1))

    create_directory(os.path.join(libexec,"jumpstart","plugins"))
    create_directory(os.path.join(libexec,"jumpstart","plugins2"))

    create_directory(os.path.join(libexec,"vmwauth","lib64"))

#Folder //usr/share
    share = os.path.join(usr,"share")
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
