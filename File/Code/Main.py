from ESXi_config import generate_random_string
from ESXi_config import create_config_file
from ESXi_config import create_directory
from bin import create_esx_bin
from dev import create_esx_dev
from etc import create_esx_etc
from include_esxi import create_esx_include
from lib_esxi import create_esx_lib
from lib64_esxi import create_esx_lib64
from opt import create_esx_opt
from tardisks import create_esx_tardisks
from tmp import create_esx_tmp
from usr import create_esx_usr
from var import create_esx_var
from vmfs import create_esx_vmfs
    
def create_esx_proc(proc="/ESXI 7/proc/"):
    create_directory(proc)

def create_esx_tardisks_noauto(noauto="/ESXI 7/tardisks_noauto/"):
    create_directory(noauto)
         
def create_esx_vmimages(vmimages ="/ESXI 7/vmimages"):
    create_config_file(vmimages,"floppies",generate_random_string(15))
    create_config_file(vmimages,"tools-isoimages",generate_random_string(15))

def create_esx_config_files(base_path="/ESXI 7"):
    """Tạo các file cấu hình ESXi 7."""
#Tạo file trong thư mục chính 
    Databootbank_1 = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\BOOTBANK1.txt"
    with open(Databootbank_1, 'r', encoding='utf-8') as f:
        boot_cfg_content_1 = f.read()  # Đọc nội dung file vào biến chuỗi
    create_config_file(base_path,"bootbank",boot_cfg_content_1)

    boot_file = {
        ".#encryption.info": 584,
        ".mtoolsrc": 452,
        "altbootbank": 455,
        "bootpart.gz": 45,
        "bootpart4kn.gz": 2147,
        "local.tgz": 2452,
        "local.tgz.ve": 245,
        "locker": 264,
        "productLocker": 314,
        "sbin": 941,
        "scratch": 45,
        "store": 43,
    }
    for bname, bsize in boot_file.items():
        create_config_file(base_path,bname,generate_random_string(bsize))



if __name__ == "__main__":
    create_esx_config_files()
    create_esx_bin()
    create_esx_dev()
    create_esx_etc()
    create_esx_include()
    create_esx_lib()
    create_esx_lib64()
    create_esx_opt()
    create_esx_proc()
    create_esx_tardisks()
    create_esx_tardisks_noauto()
    create_esx_tmp()
    create_esx_usr()
    create_esx_var()
    create_esx_vmfs()
    create_esx_vmimages()
    print("Các file cấu hình ESXi 7 đã được tạo thành công!")


    # while True:
    #     lua_chon = input("Bạn có muốn chạy chương trình? (Yes/No): ").lower()
    #     if lua_chon in ["Y","y"]:
    #         create_esx_config_files()
    #         print("Các file cấu hình ESXi 7 đã được tạo thành công!")
    #         break  # Thoát khỏi vòng lặp sau khi chạy
    #     elif lua_chon in ["N", "n"]:
    #         print("Đã hủy chạy chương trình.")
    #         break  # Thoát khỏi vòng lặp
    #     else:
    #         print("Lựa chọn không hợp lệ. Vui lòng nhập 'có' hoặc 'không'.")
