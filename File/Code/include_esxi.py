import os

from ESXi_config import create_config_file
from ESXi_config import generate_random_string

def create_esx_include(base_path):
    include_path = os.path.join(base_path,"include","python3.8")
    create_config_file(include_path,"pyconfig.h",generate_random_string(1024))