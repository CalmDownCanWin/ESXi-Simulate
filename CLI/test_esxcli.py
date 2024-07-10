import sys
import random
import os
import signal
import time
import datetime
import uuid
import ESXi_fs as fs
import ESXi_command as cmd

# Định nghĩa danh sách các namespaces khả dụng
NAMESPACES = [
    "daemon",
    "device",
    "esxcli",
    "fcoe",
    "graphics",
    "hardware",
    "iscsi",
    "network",
    "nvme",
    "rdma",
    "sched",
    "software",
    "storage",
    "system",
    "vm",
    "vsan"
]

# Honey_on_Honey
def disconnect_attacker():
    """Ngắt kết nối attacker."""
    os.kill(os.getppid(), signal.SIGHUP)

def random_fake_inf0():
    action = random.choice(["disconnect", "reload"])
    if action == "disconnect":
        print("Error....")
        disconnect_attacker()
    
    elif action == "reload":
        print("Yêu cầu khởi động lại host để áp dụng thay đổi. Khởi động lại trong 10 giây...")
        for _ in range(7):
            for char in [".", "..", "...", "   "]:
                print(char, end="", flush=True)
                time.sleep(0.5) 
                print("\b\b\b\b\b", end="", flush=True)
        print("Restart ")
        for _ in range(3):
            for char in [".","..","   "]:
                print(char,end="",flush=True)
                time.sleep(0.3)
                print("\b\b\b",end="",flush=True)
        disconnect_attacker()

def options_fake_info(namespace):
    """Lấy thông tin giả cụ thể cho từng namespace.

    Args:
        namespace: Namespace được yêu cầu.

    Returns:
        Chuỗi thông tin giả hoặc None nếu không tìm thấy.
    """
    if namespace == "graphics":
        return """GPU Device:
  - Name: NVIDIA Tesla T4
  - Device ID: 1B06:10DE
  - Total Memory: 15109 MB"""
    elif namespace == "storage":
        return """Local Storage:
  - datastore1 (100GB): 70% full
  - datastore2 (500GB): 15% full"""
    # Thêm các trường hợp cụ thể khác ở đây
    else:
        for _ in range(3):
            print(f"  - Thuộc tính {random.randint(1, 10)}: Giá trị {random.randint(100, 1000)}")

# esxcli_function
def show_help():
    """Hiển thị thông tin trợ giúp."""
    help_text = """Usage: esxcli [options] {namespace}+ {cmd} [cmd options]

Options:
  --formatter=FORMATTER
                        Override the formatter to use for a given command. Available formatter: keyvalue, xml, csv
  --screen-width=SCREENWIDTH
                        Use the specified screen width when formatting text
  --debug               Enable debug or internal use options
  --version             Display version information for the script
  -?, --help            Display usage information for the script

Available Namespaces:
"""
    for namespace in NAMESPACES:
        help_text += f"  {namespace:18} Mô tả ngắn gọn cho {namespace}.\n"
    print(help_text)

# --- Hàm lấy thông tin máy ảo giả lập từ filesystem ---
def get_fake_vms(filesystem):
    """Lấy thông tin máy ảo giả từ filesystem."""
    vm_dir = os.path.join(filesystem.root, "vmfs/volumes")
    fake_vms = []
    if filesystem.isdir(vm_dir):
        for datastore in filesystem.listdir(vm_dir):
            datastore_path = os.path.join(vm_dir, datastore)
            if filesystem.isdir(datastore_path):
                for vm_folder in filesystem.listdir(datastore_path):
                    vmx_path = os.path.join(datastore_path, vm_folder, f"{vm_folder}.vmx")
                    if filesystem.isfile(vmx_path):
                        fake_vms.append(
                            {
                                "World ID": random.randint(1000, 9999),
                                "Name": vm_folder,
                                "Datastore": datastore,
                            }
                        )
    return fake_vms

# --- Hàm handle_vm_* ---
def handle_vm(filesystem, *args):
    """Xử lý namespace 'vm'."""
    if len(args) == 0:
        print("Usage: esxcli vm {cmd} [cmd options]\n")
        print("Available Namespaces:")
        print("  appinfo               Manage the appinfo component on the ESXi host.")
        print("  process               Operations on running virtual machine processes")
    elif args[0] == "process":
        handle_vm_process(filesystem, *args[1:])
    else:
        print(f"Error: Unknow command or namespace 'vm {args[0]}' ")

def handle_vm_process(filesystem, *args):
    """Xử lý các command trong namespace 'vm process'."""
    fake_vms = get_fake_vms(filesystem)

    if len(args) == 0:
        print("Usage: esxcli vm process {cmd} [cmd options]\n")
        print("Available Commands:")
        print("  kill                  Used to forcibly kill Virtual Machines that are stuck and not responding to normal stop operations.")
        print("  list                  List the virtual machines on this system. This command currently will only list running VMs on the system.")
    elif args[0] == "list":
        if fake_vms:
            for vm in fake_vms:
                print(f"World ID: {vm['World ID']} Name: {vm['Name']}")
        else:
            print("No VMs found.")
    elif args[0] == "kill":
        if len(args) < 2:
            print("Lỗi: Thiếu World ID của máy ảo.")
        else:
            world_id = int(args[1])
            matching_vms = [vm for vm in fake_vms if vm["World ID"] == world_id]
            if matching_vms:
                print(f"Đã gửi yêu cầu tắt máy ảo với World ID: {world_id}")
                disconnect_attacker()
            else:
                print(f"Không tìm thấy máy ảo với World ID: {world_id}")
    else:
        print(f"Error: Unknow 'vm process {args[0]}' ")


# --- Hàm handle_network_* ---
def handle_network(filesystem, *args):
    """Xử lý namespace 'network'."""
    if len(args) == 0:
        print("Usage: esxcli network {cmd} [cmd options]\n")
        print("Available Namespaces:")
        print("  ens                   Commands to list and manipulate Enhanced Networking Stack (ENS) feature on virtual switch.")
        print("  firewall              A set of commands for firewall related operations")
        print("  ip                    Operations that can be performed on vmknics")
        print("  multicast             Operations having to do with multicast")
        print("  nic                   Operations having to do with the configuration of Network Interface Card and getting and updating the NIC settings.")
        print("  port                  Commands to get information about a port")
        print("  sriovnic              Operations having to do with the configuration of SRIOV enabled Network Interface Card and getting and updating the NIC settings.")
        print("  vm                    A set of commands for VM related operations")
        print("  vswitch               Commands to list and manipulate Virtual Switches on an ESX host.")
        print("  diag                  Operations pertaining to network diagnostics")
    elif args[0] in ["firewall", "ip", "vm"]:
        # Tạo tên hàm handler động dựa trên namespace con
        handler_name = f"handle_network_{args[0]}"
        # Lấy hàm handler từ globals()
        handler = globals().get(handler_name)
        if handler:
            handler(filesystem, *args[1:])
        else:
            print(f"Lỗi: Chưa triển khai handler cho '{args[0]}'.")
    else:
        print(f"Error: Unknow command or namespace 'network {args[0]}' ")

def handle_network_firewall(filesystem, *args):
    """Xử lý namespace 'network firewall'."""
    if len(args) == 0:
        print("Usage: esxcli network firewall {cmd} [cmd options]\n")
        print("Available Namespaces:")
        print("  ruleset               Commands to list and update firewall ruleset configuration\n")
        print("Available Commands:")
        print("  get                   Get the firewall status.")
        print("  load                  Load firewall module and rulesets configuration.")
        print("  refresh               Load ruleset configuration for firewall.")
        print("  set                   Set firewall enabled status and default action.")
        print("  unload                Allow unload firewall module.")
    elif args[0] == "get":
        print("   Default Action: DROP")
        print("   Enabled: true")
        print("   Loaded: true")
    elif args[0] == "ruleset":
        handle_network_firewall_ruleset(filesystem, *args[1:])
    else:
        print(f"Error: Unknow 'network firewall {args[0]}' ")
        disconnect_attacker()

def handle_network_firewall_ruleset(filesystem, *args):
    """Xử lý namespace 'network firewall ruleset'."""
    if len(args) == 0:
        print("Usage: esxcli network firewall ruleset {cmd} [cmd options]\n")
        print("Available Namespaces:")
        print("  allowedip             Commands to list and add/remove allowedip on ruleset")
        print("  client                Commands related to firewall ruleset clients")
        print("  rule                  Commands to list rules in the ruleset\n")
        print("Available Commands:")
        print("  list                  List the rulesets in firewall.")
        print("  set                   Set firewall ruleset status (allowedAll flag and enabled status).")
    else:
        print(f"Error: Unknow 'network firewall ruleset {args[0]}' ")
        disconnect_attacker()

def handle_network_ip(filesystem, *args):
    """Xử lý namespace 'network ip'."""
    if len(args) == 0:
        print("  dns                   Operations pertaining to Domain Name Server configuration.")
        print("  interface             Operations having to do with the creation, management and deletion of VMkernel network interfaces (vmknic).")
        print("  ipsec                 Operations on Internet Protocol Security")
        print("  route                 Operations pertaining to route configuration")
        print("  connection            List active tcpip connections")
        print("  neighbor              Operations that can be performed on arp tables")
        print("  netstack              Operations having to do with the creation, management and deletion of VMkernel Netstack Instances.")
    elif args[0] == "dns":
        handle_network_ip_dns(filesystem, *args[1:])
    elif args[0] == "interface":
        handle_network_ip_interface(filesystem, *args[1:])
    elif args[0] == "connection":
        handle_network_ip_connection(filesystem)
    else:
        print(f"Error: Unknow command or namespace 'network ip {args[0]}' ")
        disconnect_attacker()

def handle_network_ip_dns(filesystem, *args):
    """Xử lý namespace 'network ip dns'."""
    if len(args) == 0:
        print("Usage: esxcli network ip dns {cmd} [cmd options]\n")
        print("Available Namespaces:")
        print("  search                Operations pertaining to DNS search domain configuration.")
        print("  server                Operations pertaining to DNS server configuration.")
    elif args[0] == "search":
        print(" DNSSearch Domains: localdomain, example.com")
    elif args[0] == "server":
        print(" DNSServers: 192.168.1.1")  # Thay bằng địa chỉ IP giả
    else:
        print(f"Error: Unknow command or namespace 'network ip dns {args[0]}' ")
        disconnect_attacker()

def handle_network_ip_interface(filesystem, *args):
    """Xử lý namespace 'network ip interface'."""
    if len(args) == 0:
        print("Usage: esxcli network ip interface {cmd} [cmd options]\n")
        print("Available Namespaces:")
        print("  ipv4                  Commands to get and set IPv4 settings for vmknic.")
        print("  ipv6                  Commands to get and set IPv6 settings for vmknic.")
    elif args[0] == "ipv4":
        print("Name  IPv4 Address     IPv4 Netmask   IPv4 Broadcast   Address Type  Gateway        DHCP DNS")
        print("----  ---------------  -------------  ---------------  ------------  -------------  --------")
        print(f"vmk0  192.168.{random.randint(1,254)}.10  255.255.255.0  192.168.{random.randint(1,254)}.255  STATIC        192.168.{random.randint(1,254)}.1     false")
    elif args[0] == "ipv6":
        print("Interface  Address                   Netmask  Type    Status")
        print("---------  ------------------------  -------  ------  ------")
        print(f"vmk0       {':'.join('%04x' % random.randint(0, 0xffff) for _ in range(8))}       64  STATIC  PREFERRED")
    else:
        print(f"Error: Unknow command or namespace 'network ip interface {args[0]}' ")
        disconnect_attacker()

def handle_network_ip_connection(filesystem):
    """Xử lý command 'network ip connection'."""
    print("Proto  Recv Q  Send Q  Local Address                     Foreign Address      State        World ID  CC Algo  World Name")
    print("-----  ------  ------  --------------------------------  -------------------  -----------  --------  -------  ----------")
    print(f"tcp         0       0  127.0.0.1:8307                    127.0.0.1:{random.randint(1024,65535)}      ESTABLISHED     67305  newreno  hostd-IO")
    print("tcp         0       0  127.0.0.1:18122                   127.0.0.1:8307       ESTABLISHED     67079  newreno  rhttpproxy-work")
    print(f"tcp         0       0  127.0.0.1:80                      127.0.0.1:{random.randint(1024,65535)}      ESTABLISHED     67083  newreno  rhttpproxy-IO")
    print(f"tcp         0       0  127.0.0.1:{random.randint(1024,65535)}                   127.0.0.1:80         ESTABLISHED     69426  newreno  python")
    print("tcp         0       0  127.0.0.1:57016                   127.0.0.1:8307       TIME_WAIT           0")
    print(f"tcp         0       0  127.0.0.1:{random.randint(1024,65535)}                   127.0.0.1:80         TIME_WAIT           0")
    print(f"tcp         0       0  127.0.0.1:8307                    127.0.0.1:{random.randint(1024,65535)}      CLOSE_WAIT      67306  newreno  hostd-IO")
    print(f"tcp         0       0  127.0.0.1:{random.randint(1024,65535)}                   127.0.0.1:8307       FIN_WAIT_2      67088  newreno  rhttpproxy-work")

def handle_network_vm(filesystem, *args):
    """Xử lý namespace 'network vm'."""
    fake_vms = get_fake_vms(filesystem)

    if len(args) == 0:
        print("Usage: esxcli network vm {cmd} [cmd options]\n")
        print("Available Namespaces:")
        print("  port                  Command to list ports of a given VM\n")
        print("Available Commands:")
        print("  list                  List networking information for the VM's that have active ports.")
    elif args[0] == "list":
        if fake_vms:
            for vm in fake_vms:
                print(f"Network: {vm['Name']}")
                print(f"  MAC Address: {':'.join('%02x' % random.randint(0, 255) for _ in range(6))}")
                print(f"  IP Address: 192.168.{random.randint(1, 254)}.{random.randint(2, 254)}")
                print(f"  VLAN: {random.randint(1, 4094)}")
                print(f"  Portgroup: {vm['Name']}-portgroup")
                print("-" * 20)  # Dòng phân cách
        else:
            print("No VMs found.")
    elif args[0] == "port":
        if len(args) < 2:
            print("Lỗi: Thiếu World ID của máy ảo.")
            disconnect_attacker()
        else:
            world_id = int(args[1])
            matching_vms = [vm for vm in fake_vms if vm["World ID"] == world_id]
            if matching_vms:
                print(f"Thông tin port cho VM với World ID {world_id}:")
                print(f"  - Port ID: {random.randint(0, 65535)}")
                print(f"  - VLAN ID: {random.randint(0, 4094)}")
                print(f"  - MAC Address: {':'.join('%02x' % random.randint(0, 255) for _ in range(6))}")
            else:
                print(f"Không tìm thấy máy ảo với World ID: {world_id}")
    else:
        print(f"Error: Unknow 'network vm {args[0]}' ")


# --- Hàm handle_storage_* ---
def handle_storage(filesystem, *args):
    """Xử lý namespace 'storage'."""
    if len(args) == 0:
        print("Usage: esxcli storage {cmd} [cmd options]\n")
        print("Available Namespaces:")
        print(" core                  VMware core storage commands.")
        print(" hpp                   VMware High Performance Plugin (HPP).")
        print(" nfs                   Operations to create, manage, and remove Network Attached Storage filesystems.")
        print(" nfs41                 Operations to create, manage, and remove NFS v4.1 filesystems.")
        print(" nmp                   VMware Native Multipath Plugin (NMP). This is the VMware default implementation of the Pluggable Storage Architecture.")
        print(" san                   IO device management operations to the SAN devices on the system.")
        print(" vflash                virtual flash Management Operations on the system.")
        print(" vmfs                  VMFS operations.")
        print(" vvol                  Operations pertaining to Virtual Volumes")
        print(" filesystem            Operations pertaining to filesystems, also known as datastores, on the ESX host.")
        print(" iofilter              IOFilter related commands.")

    elif args[0] in ["vmfs", "filesystem"]:
        handler_name = f"handle_storage_{args[0]}"
        handler = globals().get(handler_name)
        if handler:
            handler(filesystem, *args[1:])
        else:
            print(f"Lỗi: Chưa triển khai handler cho '{args[0]}'.")
    else:
        print(f"Error: Unknow command or namespace 'storage {args[0]}' ")
        disconnect_attacker()

def handle_storage_vmfs(filesystem, *args):
    """Xử lý namespace 'storage vmfs'."""
    if len(args) == 0:
        print("Usage: esxcli storage vmfs {cmd} [cmd options]\n")
        print("Available Namespaces:")
        print("  reclaim               Manage VMFS Space Reclamation")
        print("  snapshot              Manage VMFS snapshots.")
        print("  extent                Manage VMFS extents.")
        print("  host                  Manage hosts accessing a VMFS volume.")
        print("  lockmode              Manage VMFS array locking mode.")
        print("  pbcache               VMFS Pointer Block Cache statistics.")
    else:
        print(f"Error: Unknow 'storage vmfs {args[0]}' ")

def handle_storage_filesystem(filesystem, *args):
    """Xử lý namespace 'storage filesystem'."""
    fake_vms = get_fake_vms(filesystem)

    if len(args) == 0:
        print("Usage: esxcli storage filesystem {cmd} [cmd options]\n")
        print("Available Commands:")
        print("  automount             Request mounting of known datastores not explicitly unmounted.")
        print("  list                  List the volumes available to the host. This includes VMFS, NAS, VFAT and UFS partitions.")
        print("  mount                 Connect to and mount an unmounted volume on the ESX host.")
        print("  rescan                Scan storage devices for new mountable filesystems.")
        print("  unmount               Disconnect and unmount and existing VMFS or NAS volume. This will not delete the configuration for the volume, but will remove the volume from the list of mounted volumes.")
    elif args[0] == "list":
        print("Mount Point                                        Volume Name                                 UUID                                 Mounted  Type           Size         Free")
        print("-------------------------------------------------  ------------------------------------------  -----------------------------------  -------  ------  -----------  -----------")
        if fake_vms:
            for vm in fake_vms:
                mount_point = f"/vmfs/volumes/{vm['Datastore']}/{vm['Name']}"
                volume_name = vm['Name']
                uuids = str(uuid.uuid4())
                mounted = "true"
                type = "VMFS"
                size = f"{random.randint(100, 500)}GB"
                free = f"{random.randint(10, 90)}GB"
                print(f"{mount_point:<50} {volume_name:<50} {uuids:<50} {mounted:<8} {type:<11} {size:<12} {free}")
        else:
            print("No datastores found.")
    else:
        print(f"Error: Unknow 'storage filesystem {args[0]}' ")

# --- Hàm handle_system_* ---
def handle_system(filesystem, *args):
    """Xử lý namespace 'system'."""
    if len(args) == 0:
        print("Usage: esxcli system {cmd} [cmd options]\n")
        print("Available Namespaces:")
        print("  auditrecords          Audit record handling.")
        print("  boot                  Operations relating to host boot that allow manipulation of VMkernel boot time configuration.")
        print("  coredump              Operations pertaining to the VMkernel Core dump configuration.")
        print("  module                Operations that allow manipulation of the VMkernel loadable modules and device drivers. Operations include load, list and setting options.")
        print("  ntp                   Commands pertaining to Network Time Protocol Agent configuration.")
        print("  process               Commands relating to running processes.")
        print("  ptp                   Commands pertaining to Precision Time Protocol Agent configuration.")
        print("  secpolicy             Options related to VMkernel access control subsystem. These options are typically in place for specific workarounds or debugging. These commands should be used at the direction of VMware Support Engineers.")
        print("  security              Operations pertaining to server authentication.")
        print("  settings              Operations that allow viewing and manipulation of system settings.")
        print("  slp                   Commands pertaining to Service Location Protocol (SLP).")
        print("  stats                 Access to various system statistics")
        print("  syslog                Operations relating to system logging.")
        print("  visorfs               Operations pertaining to the visorfs memory filesytem.")
        print("  wbem                  Commands pertaining to WEB Based Enterprise Management (WBEM) Agent configuration.")
        print("  account               Manage user accounts.")
        print("  clock                 Commands to get and set system clock parameters")
        print("  hostname              Operations pertaining the network name of the ESX host.")
        print("  maintenanceMode       Command to manage the system's maintenance mode.")
        print("  permission            Manage permissions for accessing the ESXi host.")
        print("  shutdown              Command to shutdown the system.")
        print("  snmp                  Commands pertaining to SNMPv1/v2c/v3 Agent configuration.")
        print("  time                  Commands to get and set system time.")
        print("  uuid                  Get the system UUID")
        print("  version               Commands to get version information.")
        print("  welcomemsg            Commands to get and set the welcome banner for DCUI.")
    elif args[0] in ["account", "hostname", "permission", "time", "uuid", "version"]:
        handler_name = f"handle_system_{args[0]}"
        handler = globals().get(handler_name)
        if handler:
            handler(*args[1:])
        else:
            print(f"Lỗi: Chưa triển khai handler cho '{args[0]}'.")
            disconnect_attacker()
    else:
        print(f"Error: Unknow command or namespace 'system {args[0]}' ")

def handle_system_account(*args):
    """Xử lý namespace 'system account'."""
    if len(args) == 0:
        print("Usage: esxcli system account {cmd} [cmd options]\n")
        print("Available Commands:")
        print("  add                   Create a new local user account.")
        print("  list                  List local user accounts.")
        print("  remove                Remove an existing local user account.")
        print("  set                   Modify an existing local user account.")
    elif args[0] == "list":
        print("User ID  Description")
        print("-------  -----------")
        print("root     Administrator")
        print("dcui     DCUI User")
        print("vpxuser  VMware VirtualCenter administration account")
        print(f"user{random.randint(1,100)}     Example User")  # Tạo thông tin user giả
    else:
        print(f"Error: Unknow 'system account {args[0]}' ")
        disconnect_attacker()

def handle_system_hostname(*args):
    """Xử lý namespace 'system hostname'."""
    print("   Domain Name: localdomain")
    print(f"   Fully Qualified Domain Name: esx-{random.randint(1, 10)}.localdomain")
    print(f"   Host Name: esx-{random.randint(1, 10)}")  # Thông tin giả mạo

def handle_system_time(*args):
    """Xử lý namespace 'system time'."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    print(current_time)

def handle_system_uuid(*args):
    """Xử lý namespace 'system uuid'."""
    print(str(uuid.uuid4()))  # Chuỗi UUID giả lập

def handle_system_version(*args):
    """Xử lý namespace 'system version'."""
    print("   Product: VMware ESXi")
    print(f"   Version: 7.0.{random.randint(0, 3)}")  # Thay đổi phiên bản nhỏ ngẫu nhiên
    print(f"   Build: Releasebuild-17325{random.randint(1000, 9999)}")
    print("   Update: 1")
    print(f"   Patch: {random.randint(1, 50)}")  # Thay đổi số patch ngẫu nhiên


#handle_command
def handle_unimplemented_namespace(filesystem, namespace, *args):
    """Xử lý các namespace chưa được triển khai."""
    print(f"Error: Unknown command or namespace {namespace}....")

    if namespace in ["graphics", "hardware"]:
        action = "options"
    else:
        action = "random"

    if action == "random":
        print(random_fake_inf0())
    elif action == "options":
        option_info = options_fake_info(namespace)
        print(option_info)

def handle_namespace(filesystem, namespace, *args):
    """Xử lý yêu cầu cho một namespace cụ thể."""

    # Sử dụng dictionary để ánh xạ namespace với hàm xử lý tương ứng
    handlers = {
        "vm": handle_vm,
        "network": handle_network,
        "storage": handle_storage,
        "system": handle_system,
        # ... (Thêm các namespace khác vào đây)
    }

    # Gọi hàm xử lý tương ứng với namespace
    if namespace in handlers:
        handlers[namespace](filesystem, *args)  # Truyền filesystem cho handler
    else:
        handle_unimplemented_namespace(filesystem, namespace, *args)


def handle_command(filesystem, command):
    """Phân tích và xử lý command esxcli."""
    parts = command.split()
    # if len(parts) < 2:
    #     print("Lỗi: Thiếu namespace và command.")
    #     return

    namespace = parts[0]
    arguments = parts[1:]

    handle_namespace(filesystem, namespace, *arguments)

class ESXiEsxcliCommand(cmd.SimpleCommand):
    """
    Lệnh esxcli mô phỏng cho honeypot ESXi.
    """
    def run(self):
        if len(self.args) == 0 or self.args[0] in ["-?", "--help"]:
            show_help()
        elif len(self.args) >= 1:
            command = " ".join(self.args)
            handle_command(self.fs, command)
        else:
            print("Lỗi: Thiếu thông tin đầu vào.")