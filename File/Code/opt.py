import os

from ESXi_config import create_config_file
from ESXi_config import generate_random_string

def create_esx_opt(base_path):
    opt_nvme = os.path.join(base_path,"opt","vmware","nvme")
    create_config_file(opt_nvme,"esxcli-nvme-plugin",generate_random_string(1024))

    opt_vmware = os.path.join(base_path,"opt","vmware","vpxa","vpx")
    create_config_file(opt_vmware,"bundleversion.xml",generate_random_string(1024))
    create_config_file(opt_vmware,"vpxResultFilter.xml",generate_random_string(1024))