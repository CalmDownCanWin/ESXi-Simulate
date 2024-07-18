import os
import random
import uuid

from ESXi_config import create_config_file
from ESXi_config import create_vmx_file
from ESXi_config import create_vmdk_file
from ESXi_config import create_fake_datastore
from ESXi_config import create_flat_vmdk
from ESXi_config import create_log_file
from ESXi_config import generate_random_string
from ESXi_config import create_fake_file


def create_esx_vmfs(base_path="/ESXI 7"):
    # Thư mục vmfs
    # Tạo datastore giả mạo
    create_fake_datastore(base_path, "NVmeDataStore",80 )
    # Thư mục vmfs/volumes/bootbank
    bootbank_path = os.path.join(base_path, "vmfs", "volumes")
    boot_cfg_content_1 = """atlantic.v00  elx_esx_.v00  iavmd.v00     loadesx.v00   lsuv2_nv.v00  nhpsa.v00     nvmxnet3.v00  qfle3i.v00    tpmesxup.v00  vmkusb.v00
b.b00         elxiscsi.v00  icen.v00      lpfc.v00      lsuv2_oe.v00  nmlx4_co.v00  nvmxnet3.v01  qflge.v00     trx.v00       vmw_ahci.v00
basemisc.tgz  elxnet.v00    igbn.v00      lpnic.v00     lsuv2_oe.v01  nmlx4_en.v00  onetime.tgz   qlnative.v00  uc_amd.b00    vmware_e.v00
bmcal.v00     esx_dvfi.v00  imgdb.tgz     lsi_mr3.v00   lsuv2_oe.v02  nmlx4_rd.v00  procfs.b00    rste.v00      uc_hygon.b00  vmx.v00
bnxtnet.v00   esx_ui.v00    ionic_en.v00  lsi_msgp.v00  lsuv2_sm.v00  nmlx5_co.v00  pvscsi.v00    s.v00         uc_intel.b00  vsan.v00
bnxtroce.v00  esxio_co.v00  irdman.v00    lsi_msgp.v01  mtip32xx.v00  nmlx5_rd.v00  qcnic.v00     sb.v00        useropts.gz   vsanheal.v00
boot.cfg      esxupdt.v00   iser.v00      lsi_msgp.v02  native_m.v00  ntg3.v00      qedentv.v00   sfvmk.v00     vdfs.v00      vsanmgmt.v00
brcmfcoe.v00  features.gz   ixgben.v00    lsuv2_hp.v00  ne1000.v00    nvme_pci.v00  qedrntv.v00   smartpqi.v00  vim.v00       weaselin.v00
btldr.v00     gc.v00        jumpstrt.gz   lsuv2_in.v00  nenic.v00     nvmerdma.v00  qfle3.v00     state.tgz     vmkata.v00    xorg.v00
crx.v00       i40en.v00     k.b00         lsuv2_ls.v00  nfnic.v00     nvmetcp.v00   qfle3f.v00    tpm.v00       vmkfcoe.v00
"""
    create_config_file(bootbank_path, "BOOTBANK1", boot_cfg_content_1)

    create_config_file(bootbank_path, "BOOTBANK2", "boot.cfg")

    #Tạo OSDATA
    content = """cache      downloads  locker     store      var        vmkdump
core       healthd    log        tmp        vdtc       vmware
"""
    # Kiểm tra xem đã có file OSDATA trong thư mục hay chưa
    for filename in os.listdir(bootbank_path):
        if filename.startswith("OSDATA"):
            return  # Nếu có file OSDATA rồi thì thoát khỏi hàm
    create_config_file(bootbank_path,f"OSDATA-{str(uuid.uuid4())}",content)
 
    #Thư mục vmfs/devices
    device_path = os.path.join(base_path,"vmfs")
    data_devices_content = """PMemDS                   dvfilter-generic-vmware  port                     usb0201
PMemDisk                 dvfiltertbl              ptmx                     usb0301
PMemNamespaces           dvsdev                   random                   usb0302
PMemVolumes              ens_rep                  shm                      usbdevices
TraceStreamVMFS          generic                  sunrpc-gss               usbpassthrough
cbt                      genscsi                  svm                      vdfm
cdp                      hyperclock               tty                      vflash
cdrom                    iodm                     tty1                     vmwMgmtInfo
char                     kbdmap                   tty2                     vmwMgmtNode0
console                  klog                     tty3                     vmwMgmtNode1
cswitch                  lacp                     tty4                     vmwMgmtNode2
deltadisks               lvm                      ttyp0                    vprobe
disks                    null                     urandom                  vsock
dmesg                    nvdManagement            usb0101                  zero
"""
    create_config_file(device_path,"devices",data_devices_content)

    # Tạo cấu trúc máy ảo Windows, Kali-Linux và Ubuntu
    domain = "example.com"
    vmx_content = """.encoding = "UTF-8"
config.version = "8"
virtualHW.version = "19"
nvram = "Window 10.nvram"
svga.present = "TRUE"
pciBridge0.present = "TRUE"
pciBridge4.present = "TRUE"
pciBridge4.virtualDev = "pcieRootPort"
pciBridge4.functions = "8"
pciBridge5.present = "TRUE"
pciBridge5.virtualDev = "pcieRootPort"
pciBridge5.functions = "8"
pciBridge6.present = "TRUE"
pciBridge6.virtualDev = "pcieRootPort"
pciBridge6.functions = "8"
pciBridge7.present = "TRUE"
pciBridge7.virtualDev = "pcieRootPort"
pciBridge7.functions = "8"
vmci0.present = "TRUE"
hpet0.present = "TRUE"
floppy0.present = "FALSE"
RemoteDisplay.maxConnections = "-1"
numvcpus = "2"
memSize = "4096"
bios.bootRetry.delay = "10"
firmware = "efi"
powerType.powerOff = "default"
powerType.suspend = "soft"
powerType.reset = "default"
tools.upgrade.policy = "manual"
sched.cpu.units = "mhz"
sched.cpu.affinity = "all"
sched.cpu.latencySensitivity = "normal"
vm.createDate = "1719044236742331"
scsi0.virtualDev = "lsisas1068"
scsi0.present = "TRUE"
sata0.present = "TRUE"
usb_xhci.present = "TRUE"
svga.autodetect = "TRUE"
scsi0:0.deviceType = "scsi-hardDisk"
scsi0:0.fileName = "Window 10.vmdk"
sched.scsi0:0.shares = "normal"
sched.scsi0:0.throughputCap = "off"
scsi0:0.present = "TRUE"
ethernet0.virtualDev = "e1000e"
ethernet0.networkName = "VM Network"
ethernet0.addressType = "generated"
ethernet0.wakeOnPcktRcv = "FALSE"
ethernet0.present = "TRUE"
sata0:0.deviceType = "atapi-cdrom"
sata0:0.fileName = "/vmfs/devices/cdrom/mpx.vmhba1:C0:T1:L0"
sata0:0.present = "TRUE"
displayName = "Window 10"
guestOS = "windows9-64"
uefi.secureBoot.enabled = "TRUE"
disk.EnableUUID = "TRUE"
toolScripts.afterPowerOn = "TRUE"
toolScripts.afterResume = "TRUE"
toolScripts.beforeSuspend = "TRUE"
toolScripts.beforePowerOff = "TRUE"
tools.syncTime = "FALSE"
uuid.bios = "56 4d d9 28 84 1b 9d 6a-4e b5 a9 40 b4 53 43 27"
uuid.location = "56 4d d9 28 84 1b 9d 6a-4e b5 a9 40 b4 53 43 27"
vc.uuid = "52 a9 08 27 82 fa ac 39-9b aa 79 4e 3c c0 fb ac"
sched.cpu.min = "0"
sched.cpu.shares = "normal"
sched.mem.min = "0"
sched.mem.minSize = "0"
sched.mem.shares = "normal"
numa.autosize.cookie = "20012"
numa.autosize.vcpu.maxPerVirtualNode = "2"
sched.swap.derivedName = "/vmfs/volumes/6676885b-da7c8fb4-8ca7-000c299cb5ed/Window 10/Window 10-555dbc08.vswp"
vm.genid = "7113999362931944212"
vm.genidX = "-4456333245678140601"
migrate.hostlog = "./Window 10-555dbc08.hlog"
scsi0:0.redo = ""
pciBridge0.pciSlotNumber = "17"
pciBridge4.pciSlotNumber = "21"
pciBridge5.pciSlotNumber = "22"
pciBridge6.pciSlotNumber = "23"
pciBridge7.pciSlotNumber = "24"
scsi0.pciSlotNumber = "160"
ethernet0.pciSlotNumber = "192"
usb_xhci.pciSlotNumber = "224"
sata0.pciSlotNumber = "32"
scsi0.sasWWID = "50 05 05 68 84 1b 9d 60"
svga.vramSize = "16777216"
vmotion.checkpointFBSize = "16777216"
vmotion.checkpointSVGAPrimarySize = "16777216"
vmotion.svga.mobMaxSize = "16777216"
vmotion.svga.graphicsMemoryKB = "16384"
ethernet0.generatedAddress = "00:0c:29:53:43:27"
ethernet0.generatedAddressOffset = "0"
vmci0.id = "-1269611737"
monitor.phys_bits_used = "45"
cleanShutdown = "TRUE"
softPowerOff = "FALSE"
usb_xhci:4.present = "TRUE"
usb_xhci:4.deviceType = "hid"
usb_xhci:4.port = "4"
usb_xhci:4.parent = "-1"
"""
# Window
    for _ in range(5):
        version_window = random.choice(["7","8","10","11"])
        number = f"{version_window}"
        vm_name_Window = f"Window_{number}"
        name = "vmware"
        vm_path = os.path.join(base_path, 'vmfs', 'volumes','NVmeDataStore', vm_name_Window)
        os.makedirs(vm_path, exist_ok=True)
        # Tạo file VMX
        create_config_file(vm_path, f"{vm_name_Window}.vmx", vmx_content)
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmx"),1024 * 1024 * 1024 * 10)
        # Tạo file log
        create_log_file(vm_path,name + ".log")
        create_fake_file(os.path.join(vm_path,f"{name}.log"),1024 * 1024 * 1024 * 8)
        # Tạo file VMDK
        create_vmdk_file(vm_path, vm_name_Window)
        # Tạo file flat.VMDK
        create_flat_vmdk(vm_path, vm_name_Window, size_gb= 100)
        # Tạo file .vmx.bak (có thể được sử dụng trong quá trình restore)
        create_config_file(vm_path, f"{vm_name_Window}.vmx.bak", vmx_content)
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmx.bak"),1024 * 1024 * 1024 * 10)
        #Tạo file .nvram 
        create_config_file(vm_path,f"{vm_name_Window}.nvram",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.nvram"),1024 * 1024 * 1024 * 10)
        #Tạo file vmsd
        create_config_file(vm_path,f"{vm_name_Window}.vmsd",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmsd"),1024 * 1024 * 1024 * 10)
        #Tạo file vmsn
        create_config_file(vm_path,f"{vm_name_Window}.vmsn",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmsn"),1024 * 1024 * 1024 * 10)
        #Tạo file vmtx
        create_config_file(vm_path,f"{vm_name_Window}.vmtx",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmtx"),1024 * 1024 * 1024 * 10)
        #Tạo file vmxf
        create_config_file(vm_path,f"{vm_name_Window}.vmxf",generate_random_string(1024))
        create_fake_file(os.path.join(vm_path,f"{vm_name_Window}.vmxf"),1024 * 1024 * 1024 * 10)

#Kali or Ubuntu
    for _ in range(5):
        # Chọn ngẫu nhiên loại máy ảo
        vm_type = random.choice(["Kali-Linux","Ubuntu"])
        vm_name = f"{vm_type}"
        name = "vmware"
        # Tạo thư mục VM
        if vm_type == "Kali-Linux":
            vm_path = os.path.join(base_path, 'vmfs', 'volumes','NVmeDataStore', vm_name)
            os.makedirs(vm_path, exist_ok=True)
            # Tạo file VMX
            create_config_file(vm_path, f"{vm_name}.vmx", vmx_content)
            # Tạo file log
            create_log_file(vm_path,name + ".log")
            # Tạo file VMDK
            create_vmdk_file(vm_path, vm_name)
            # Tạo file flat.VMDK
            create_flat_vmdk(vm_path, vm_name, size_gb= 100)
            #Tạo file vmx.lck
            create_config_file(vm_path, f"{vm_name}.vmx.lck", vmx_content)
            #Tạo file .nvram 
            create_config_file(vm_path,f"{vm_name}.nvram",generate_random_string(1024))
            #Tạo file vmsd
            create_config_file(vm_path,f"{vm_name}.vmsd",generate_random_string(1024))
            #Tạo file vswp
            create_config_file(vm_path,f"{vm_name}-{generate_random_string(5)}.vswp",generate_random_string(1024))
            #Tạo file vmsn
            create_config_file(vm_path,f"{vm_name}.vmsn",generate_random_string(1024))
            #Tạo file vmtx
            create_config_file(vm_path,f"{vm_name}.vmtx",generate_random_string(1024))
            #Tạo file vmxf
            create_config_file(vm_path,f"{vm_name}.vmxf",generate_random_string(1024))




        elif vm_type == "Ubuntu":
            vm_path = os.path.join(base_path, 'vmfs', 'volumes','NVmeDataStore', vm_name)
            os.makedirs(vm_path, exist_ok=True)
            # Tạo file VMX
            create_config_file(vm_path, f"{vm_name}.vmx", vmx_content)
            # Tạo file log
            create_log_file(vm_path,name + ".log")
            # Tạo file VMDK
            create_vmdk_file(vm_path, vm_name)
            # Tạo file flat.VMDK
            create_flat_vmdk(vm_path, vm_name, size_gb= 100)
            #Tạo file .nvram 
            create_config_file(vm_path,f"{vm_name}.nvram",generate_random_string(1024))
            #Tạo file vmsd
            create_config_file(vm_path,f"{vm_name}.vmsd",generate_random_string(1024))
            #Tạo file vmsn
            create_config_file(vm_path,f"{vm_name}.vmsn",generate_random_string(1024))
            #Tạo file vmtx
            create_config_file(vm_path,f"{vm_name}.vmtx",generate_random_string(1024))
            #Tạo file vmxf
            create_config_file(vm_path,f"{vm_name}.vmxf",generate_random_string(1024))

