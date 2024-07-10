from ESXi_config import create_directory

def create_esx_tmp():
    tmp_folder = {
        '/ESXI 7/tmp/vmware-root/',
        '/ESXI 7/tmp/vmware-root_68260-1619746241/',
        '/ESXI 7/tmp/vmware-uid_0/',
        '/ESXI 7/tmp/vmware-root_85464_5645446546/',
        '/ESXI 7/tmp/vmware-root_54545_8454548451/',
    }
    for path in tmp_folder:
        create_directory(path)