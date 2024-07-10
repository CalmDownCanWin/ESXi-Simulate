import os

from ESXi_config import create_config_file
from ESXi_config import generate_random_string
from ESXi_config import create_directory



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

    python3_8 = '/ESXI 7/lib64/python3.8/'
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

    sec = '/ESXI 7/lib64/security/'
    create_directory(sec)

    lib64 = '/ESXI 7/lib64/'
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
    }
    for lib64n,lib64s in li_file.items():
        create_config_file(lib64,lib64n,generate_random_string(lib64s))

