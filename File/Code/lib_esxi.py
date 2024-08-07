import os

from ESXi_config import create_config_file
from ESXi_config import create_directory
from ESXi_config import generate_random_string
from ESXi_config import create_symlinks

def create_esx_lib(folder):
    lib_path= os.path.join(os.path.expanduser("~"), folder,"lib")
    security_path= os.path.join(lib_path,"security")
    create_directory(security_path)

    lib_file = {
        "ld-2.17.so": 165614,
        "libc-2.17.so": 45513,
        "libcrypt.so.1.0": 5615,
        "libcrypto.so": 11,
        "libcrypto.so.1.0.2": 56411,
        "libdl-2.17.so": 5415,
        "libexpat.so": 16,
        "libgcc_s.so": 16,
        "libgcc_s.so.1": 16,
        "libm-2.17.so": 16,
        "libm.so.6": 16,
        "libnsl-2.17.so": 16,
        "libnsl.so.1": 16,
        "libnss_compat-2.17.so": 16,
        "libnss_compat.so.2": 16,
        "libnss_dns-2.17.so": 16,
        "libnss_dns.so.2": 16,
        "libnss_files-2.17.so": 16,
        "libnss_files.so.2": 16,
        "libnss_nis-2.17.so": 16,
        "libnss_nis.so.2": 16,
        "libnss_nisplus-2.17.so": 16,
        "libnss_nisplus.so.2": 16,
        "libpthread-2.17.so": 16,
        "libpthread.so.0": 16,
        "libresolv-2.17.so": 16,
        "libresolv.so.2": 16,
        "librt-2.17.so": 16,
        "librt.so.1": 16,
        "libssl.so": 16,
        "libssl.so.1.0.2": 16,
        "libstdc++.so": 16,
        "libstdc++.so.6": 16,
        "libstdc++.so.6.0.22": 16,
        "libthread_db-1.0.so": 16,
        "libthread_db.so.1": 16,
        "libutil-2.17.so": 16,
        "libutil.so.1": 16,
        "libvmkmgmt.so": 16,
        "libvmksysinfoNoVob.so": 16,
        "libvmkuser.so": 16,
        "libvmkuser.so.0": 16,
        "libvmkuser.so.0.21": 16,
        "libvmlibs.so": 16,
        "libxml2.so": 16,
        "libxml2.so.2": 16,
        "libxml2.so.2.9.14": 16,
        "libz.so.1.2.12": 16,
    }
    for libn,libs in lib_file.items():
        create_config_file(lib_path,libn,generate_random_string(libs))


    lib_symlinks = {
        "ld-linux.so.2": "ld-2.17.so",
        "libc.so.6": "libc-2.17.so",
        "libcrypt.so.1": "libcrypt.so.1.0",
        "libcrypt.so": "libcrypt.so.1.0.2",
        "libdl.so.2": "libdl-2.17.so",
        "libm.so.6": "libm-2.17.so",
        "libnsl.so.1": "libnsl-2.17.so",
        "libnss_compat.so.2": "libnss_compat-2.17.so",
        "libnss_dns.so.2": "libnss_dns-2.17.so",
        "libnss_files.so.2": "libnss_files-2.17.so",
        "libnss_nis.so.2": "libnss_nis-2.17.so",
        "libnss_nisplus.so.2": "libnss_nisplus-2.17.so",
        "libpthread.so.0": "libpthread-2.17.so",
        "libresolv.so.2": "libresolv-2.17.so",
        "librt.so.1": "librt-2.17.so",
        "libssl.so": "libssl.so.1.0.2",
        "libstdc++.so": "libstdc++.so.6.0.22",
        "libstdc++.so.6": "libstdc++.so.6.0.22",
        "libthread_db.so.1": "libthread_db-1.0.so",
        "libutil.so.1": "libutil-2.17.so",
        "libvmkuser.so": "/lib/libvmkuser.so.0.21",
        "libvmkuser.so.0": "/lib/libvmkuser.so.0.21",
        "libxml2.so": "libxml2.so.2.9.14",
        "libxml2.so.2": "libxml2.so.2.9.14",
        "libz.so": "libz.so.1.2.12",
        "libz.so.1": "libz.so.1.2.12",
    }
    create_symlinks(lib_path,lib_symlinks)