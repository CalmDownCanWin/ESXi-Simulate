import os

from ESXi_config import create_config_file
from ESXi_config import generate_random_string
from ESXi_config import create_directory
# from ESXi_config import create_symlinks




def create_esx_lib64(base_path):
    lib64_path = os.path.join(base_path,"lib64")
    pcsc_path = os.path.join(lib64_path,"pcsc","drivers","ifd-ccid.bundle","Contents")
    pcsc_linux_path = os.path.join(lib64_path,"pcsc","drivers","ifd-ccid.bundle","Contents","Linux")
    create_config_file(pcsc_path,"Info.plist",generate_random_string(1024))
    create_config_file(pcsc_linux_path,"libccid.so",generate_random_string(1024))

    python3_5_path = os.path.join(lib64_path,"python3.5","site-packages","loadesxLive","borautils")
    create_config_file(python3_5_path,"elfbin.pyc",generate_random_string(14))
    create_config_file(python3_5_path,"exception.pyc",generate_random_string(1))
    create_config_file(python3_5_path,"libelf.so",generate_random_string(130))

    python_load_path = os.path.join(lib64_path,"python3.5","site-packages","loadesxLive")
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

    python_vmware_path = os.path.join(lib64_path,"python3.5","site-packages","vmware")
    create_config_file(python_vmware_path,"esximage",generate_random_string(1024))

    python3_8 = os.path.join(lib64_path,"python3.8")
    py3_8_folder = {
        "asyncio",
        "collections",
        "concurrent",
        "config-3.8",
        "ctypes",
        "curses",
        "dbm",
        "distutils",
        "email",
        "encodings",
        "ensurepip",
        "gevent",
        "gevent-1.3.5-py3.8.egg-info",
        "html",
        "http",
        "idlelib",
        "importlib",
        "json",
        "lib-dynload",
        "lib2to3",
        "logging",
        "multiprocessing",
        "pydoc_data",
        "site-packages",
        "sqlite3",
        "tkinter",
        "turtledemo",
        "unittest",
        "urllib",
        "venv",
        "wsgiref",
        "xml",
        "xmlrpc",
    }
    for foldern in py3_8_folder:
        create_directory(os.path.join(python3_8,foldern))

    sec = os.path.join(lib64_path,"security")
    create_directory(sec)

    li_file = {
        "diskLibWrapper.so": 546,
        "ld-2.17.so": 546,
        "ld-linux-x86-64.so.2": 546,
        "libadvanced_options.so": 546,
        "libarchive.so.13": 546,
        "libauditTlsParams.so": 546,
        "libaws-cpp-sdk-core.so": 546,
        "libaws-cpp-sdk-kms.so": 546,
        "libaws-cpp-sdk-s3.so": 546,
        "libbmcal.so": 546,
        "libbz2.so": 546,
        "libbz2.so.1.0": 546,
        "libbz2.so.1.0.8": 546,
        "libc-2.17.so": 546,
        "libconfigstorecommon.so": 546,
        "libconfigmanager.so": 546,
        "libconfigstore.so.0.1": 546,
        "libconfigstoredocument.so": 546,
        "libconfigstoreupgrade.so": 546,
        "libcpptools.so": 546,
        "libcrypt.so.1": 546,
        "libcrypt.so.1.0": 546,
        "libcrypto.so": 546,
        "libdatafilectl.so.0.1": 546,
        "libdouble-conversion.so": 546,
        "libdouble-conversion.so.3.0.0": 546,
        "libdpu-api-bindings.so": 546,
        "libesx_hardware_usb_passthrough_switch.so": 546,
        "libesx_identity_auth_proxy_certificate.so": 546,
        "libesx_identity_smart_card_authentication.so": 546,
        "libesx_security_settings.so": 546,
        "libesx_storage_fcoe_fcoe_activation_driver_policies.so": 546,
        "libesx_storage_fcoe_fcoe_activation_nic_policies.so": 546,
        "libesx_storage_iscsi_hardware_adapters.so": 546,
        "libesx_storage_iscsi_software_adapter.so": 546,
        "libesx_storage_nvmeof_nvme_connections.so": 546,
        "libesx_storage_nfs_krb_credentials.so": 546,
        "libesx_storage_nvmeof_nvme_over_fabrics_adapters.so": 546,
        "libesx_storage_satp_default_psps.so": 546,
        "libesx_storage_vasa_vvol.so": 546,
        "libesx_update_software_acceptance_level.so": 546,
        "libesxtoken-vapi-bindings.so": 546,
        "libesxtokenauthn.so": 546,
        "libgsoapssl++.so": 546,
        "libhostd-api-bindings.so": 546,
        "libinternal-esx-vm-api.so": 546,
        "libioFilterVPCommon.so": 546,
        "libiscsimgmtinternal.so": 546,
        "libkadm5srv_mit.so.11": 546,
        "libkrb5support.so.0": 546,
        "liblwiocommon.so.0": 546,
        "liblwnetcommon.so.0": 546,
        "libMallocArenaFix.so": 546,
        "libnfs_v3_datastores.so": 546,
        "libnfs_v41_datastores.so": 546,
        "libnmp_claim_rules.so": 546,
        "libnss_compat-2.17.so": 546,
        "libnss_nisplus-2.17.so": 546,
        "libpam_misc.so.0.82.1": 546,
        "libpng16.so.16.37.0": 546,
        "libqlerrortrace.so": 546,
        "libqlkmipsimple.so": 546,
        "libqlloader.so": 546,
        "libqlopenssl.so": 546,
        "libqlproxy.so": 546,
        "libqlsocket.so": 546,
        "libredfish.so.1.99.0": 546,
        "libschemastore.so": 546,
        "libssl.so.1.0.2": 546,
        "libstats-api-bindings.so": 546,
        "libstdc++.so.6.0.22": 546,
        "libsyslog_config.so": 546,
        "libsystem-management-api-bindings.so": 546,
        "libtrusted-execution-internal-api-bindings.so": 546,
        "libvapi-cis-bindings.so.2": 546,
        "libvapi-introspection.so.2": 546,
        "libvapi-metadata-services.so.2": 546,
        "libvapi-std-bindings.so.2": 546,
        "libvimconfigstore.so": 546,
        "libvmkmemstats.so": 546,
        "libvmkuser.so.0.23": 546,
        "libvmsnapshot.so": 546,
        "libvmw-pref-dc.so": 546,
        "libvmx-vmiop.so": 546,
        "libvsanexternalapi.so": 546,
        "libvsanmgmt-types.so": 546,
        "libvsanspbm.so": 546,
        "libvsanvitvmkctl.so": 546,
        "libx86emu.so.1": 546,
        "libXfont2.so.2": 546,
        "libxml2.so.2.9.14": 546,
        "libyaml-cpp.so.0.6": 546,
        "libz.so.1.2.12": 546,
        "ld-linux-x86-64.so.2": 1,
        "libbz2.so": 1,
        "libbz2.so.1.0": 1,
        "libc.so.6": 1,
        "libconfigstore.so": 1,
        "libconfigstore.so.0": 1,
        "libcrypt.so.1": 1,
        "libcrypt.so": 1,
        "libcurl.so": 1,
        "libcurl.so.4": 1,
        "libdatafilectl.so": 1,
        "libdatafilectl.so.0":1,
        "libdl.so.2": 1,
        "libdouble-conversion.so": 1,
        "libedit.so":1,
        "libedit.so.0":1,
        "libevent-2.1.so.7":1,
        "libevent.so":1,
        "libexslt.so":1,
        "libexslt.so.2.2":1,
        "libglog.so":1,
        "libglog.so.0":1,
        "libiscsimgmt.so.0":1,
        "libjansson.so":1,
        "libjansson.so.4":1,
        "libpng.so":1,
        "libpng16.so":1,
        "libpng16.so.16":1,
        "libpthread.so.0":1,
        "libpython3.5m.so.1.0":1,
        "libpython3.8.so":1,
        "libreadline.so":1,
        "libredfish.so.1":1,
        "libresolv.so.2":1,
        "librt.so.1":1,
        "libssl.so":1,
        "libstdc++.so":1,
        "libstdc++.so.6":1,
        "libthread_db.so.1":1,
        "libusb-1.0.so":1,
        "libusb-1.0.so.0": 1,
        "libutil.so.1": 1,
        "libuuid.so": 1,
        "libuuid.so.1": 1,
        "libvmiof.so": 1,
        "libvmiof.so.1": 1,
        "libvmiof.so.2": 1,
        "libvmiof.so.2.5": 1,
        "libvmkuser.so": 1,
        "libvmkuser.so.0": 1,
        "libvmx-vmiop.so": 1,
        "libxml2.so": 1,
        "libxml2.so.2": 1,
        "libxslt.so": 1,
        "libxslt.so.1": 1,
        "libz.so": 1,
        "libz.so.1":  1,
    }
    for lib64n,lib64s in li_file.items():
        create_config_file(lib64_path,lib64n,generate_random_string(lib64s))

    # my_symlinks = {
    #     "ld-linux-x86-64.so.2": "ld-2.17.so",
    #     "libbz2.so": "libbz2.so.1.0",
    #     "libbz2.so.1.0": "libbz2.so.1.0.8",
    #     "libc.so.6": "libc-2.17.so",
    #     "libconfigstore.so": "libconfigstore.so.0.1",
    #     "libconfigstore.so.0": "libconfigstore.so.0.1",
    #     "libcrypt.so.1": "libcrypt.so.1.0",
    #     "libcrypt.so": "libcrypt.so.1.0.2",
    #     "libcurl.so": "libcurl.so.4.7.0",
    #     "libcurl.so.4": "libcurl.so.4.7.0",
    #     "libdatafilectl.so": "libdatafilectl.so.0.1",
    #     "libdatafilectl.so.0": "libdatafilectl.so.0.1",
    #     "libdl.so.2": "libdl-2.17.so",
    #     "libdouble-conversion.so": "libdouble-conversion.so.3.0.0",
    #     "libedit.so": "libedit.so.0.0.41",
    #     "libedit.so.0": "libedit.so.0.0.41",
    #     "libevent-2.1.so.7": "libevent-2.1.so.7.0.1",
    #     "libevent.so": "libevent-2.1.so.7.0.1",
    #     "libexslt.so": "libexslt.so.0.8.17",
    #     "libexslt.so.2.2": "libexslt.so.0.8.17",
    #     "libglog.so": "libglog.so.0.3.5",
    #     "libglog.so.0": "libglog.so.0.3.5",
    #     "libiscsimgmt.so.0": "/lib64/libiscsimgmt.so.0.0",
    #     "libjansson.so": "libjansson.so.4.10.0",
    #     "libjansson.so.4": "libjansson.so.4.10.0",





    #     "libpng.so": "libpng16.so",
    #     "libpng16.so": "libpng16.so.16.37.0",
    #     "libpng16.so.16": "libpng16.so.16.37.0",
    #     "libpthread.so.0": "libpthread-2.17.so",
    #     "libpython3.5m.so.1.0": "/lib64/libpython3.so",
    #     "libpython3.8.so": "libpython3.8.so.1.0",
    #     "libreadline.so": "libedit.so",
    #     "libredfish.so.1": "libredfish.so.1.99.0",
    #     "libresolv.so.2": "libresolv-2.17.so",
    #     "librt.so.1": "librt-2.17.so",
    #     "libssl.so": "libssl.so.1.0.2",
    #     "libstdc++.so": "libstdc++.so.6.0.22",
    #     "libstdc++.so.6": "libstdc++.so.6.0.22",
    #     "libthread_db.so.1": "libthread_db-1.0.so",
    #     "libusb-1.0.so": "libusb-1.0.so.0.1.0",
    #     "libusb-1.0.so.0": "libusb-1.0.so.0.1.0",
    #     "libutil.so.1": "libutil-2.17.so",
    #     "libuuid.so": "libuuid.so.1",
    #     "libuuid.so.1": "libuuid.so.1.2",
    #     "libvmiof.so": "libvmiof.so.2.7",
    #     "libvmiof.so.1": "libvmiof.so.2.7",
    #     "libvmiof.so.2": "libvmiof.so.2.7",
    #     "libvmiof.so.2.5": "libvmiof.so.2.7",
    #     "libvmkuser.so": "/lib64/libvmkuser.so.0.23",
    #     "libvmkuser.so.0": "/lib64/libvmkuser.so.0.23",
    #     "libvmx-vmiop.so": "/usr/lib64/vmware/plugin/libvmx-vmiop.so",
    #     "libxml2.so": "libxml2.so.2.9.14",
    #     "libxml2.so.2": "libxml2.so.2.9.14",
    #     "libxslt.so": "libxslt.so.1.1.28",
    #     "libxslt.so.1": "libxslt.so.1.1.28",
    #     "libz.so": "libz.so.1.2.12",
    #     "libz.so.1": "libz.so.1.2.12",
    #     }
    # create_symlinks(lib64_path,my_symlinks)

