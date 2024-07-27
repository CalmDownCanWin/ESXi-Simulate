import os
import datetime

from ESXi_config import create_config_file
from ESXi_config import generate_random_string

def create_esx_tardisks(tardisks_path='/ESXI 7/tardisks/'):
    """Tạo thư mục và file giả mạo trong /tardisks."""
    os.makedirs(tardisks_path, exist_ok=True)

    # File metadata giả mạo
    metadata_content = f"""
    {{
        "created": "{datetime.datetime.now().isoformat()}",
        "patches": [
            {{
                "name": "fake-patch-1",
                "version": "1.2.3",
                "status": "installed"
            }},
            {{
                "name": "fake-patch-2",
                "version": "4.5.6",
                "status": "staged"
            }}
        ]
    }}
    """
    create_config_file(tardisks_path, "metadata.json", metadata_content)
    # File patch giả mạo
    create_config_file(tardisks_path, "fake-patch-1.vib", generate_random_string(1024))

    # Các file giả mạo ESXi
    tardisks_files = {
        "atlantic.v00": 1414,
        "basemisc.tgz": 11430,
        "bnxtnet.v00": 919,
        "brcmfcoe.v00": 2227,
        "crx.v00": 2227,
        "elxnet.v00": 2227,
        "i40en.v00": 2227,
        "icen.v00": 2227,
        "igbn.v00": 2227,
        "imgdb.tgz": 2227,
        "ionic_en.v00": 2227,
        "iser.v00": 2227,
        "ixgben.v00": 2227,
        "lsi_mr3.v00": 2227,
        "lsi_msgp.v00": 2227,
        "lsi_msgp.v01": 2227,
        "lsi_msgp.v02": 2227,
        "lsuv2_hp.v00": 2227,
        "lsuv2_in.v00": 2227,
        "lsuv2_ls.v00": 2227,
        "lsuv2_nv.v00": 2227,
        "lsuv2_oe.v00": 2227,
        "ionic_en.v01": 2227,
        "ionic_en.v02": 2227,
        "nmlx4_co.v00": 2227,
        "nmlx4_en.v00": 2227,
        "elx_esx_.v00": 2317,
        "elxiscsi.v00": 565,
        "esx_ui.v00": 22641,
        "esxupdt.v00": 2292,
        "iavmd.v00": 742,
        "gc.v00": 1024,
        "irdman.v00": 1024,
        "loadesx.v00": 3586,
        "lpfc.v00": 3009,
        "lpnic.v00": 635,
        "vmkata.v00": 163431,
        "vmkata.v00": 202,
        "vmw_ahci.v00": 348,
        "vmware_e.v00": 199,
        "vmx.v00": 122337,
        "vsan.v00": 41470,
        "vsanheal.v00": 8356,
        "vsanmgmt.v00": 26437,
        "weaselin.v00": 2701,
        "xorg.v00": 3438,
    }
    for filename, size in tardisks_files.items():
        create_config_file(tardisks_path, filename, generate_random_string(size))