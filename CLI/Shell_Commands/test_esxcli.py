import sys
import random
import os
import signal
import time
import datetime
import uuid
import ESXi_fs as fs
import ESXi_command as cmd

import error_handler as er

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
#def disconnect_attacker():
#    """Ngắt kết nối attacker."""
#    os.kill(os.getppid(), signal.SIGHUP)


# esxcli_function

def show_help(self):
    help_text = """Usage: esxcli [options] {namespace}+ {cmd} [cmd options]\r\n

Options:\r\n
  --formatter=FORMATTER\r\n
                        Override the formatter to use for a given command. Available formatter: keyvalue, xml, csv\r\n
  --screen-width=SCREENWIDTH\r\n
                        Use the specified screen width when formatting text\r\n
  --debug               Enable debug or internal use options\r\n
  --version             Display version information for the script\r\n
  -?, --help            Display usage information for the script\r\n

Available Namespaces:
"""
    for namespace in NAMESPACES:
        help_text += f"  \r{namespace:18} Mô tả ngắn gọn cho {namespace}.\r\n"
    self.write_output(help_text)

# --- get vm from filesystem ---
def get_fake_vms(filesystem):
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


def handle_vm(self,filesystem, *args):
    if len(args) == 0:
        self.write_output("Usage: esxcli vm {cmd} [cmd options]\r\n")
        self.write_output("Available Namespaces:\r\n")
        self.write_output("  appinfo               Manage the appinfo component on the ESXi host.\r\n")
        self.write_output("  process               Operations on running virtual machine processes\r\n")
    elif args[0] == "process":
        handle_vm_process(self,filesystem, *args[1:])
    else:
        self.write_output(f"Error: Unknow command or namespace 'vm {args[0]}' \r\n")


def handle_vm_process(self,filesystem, *args):
    fake_vms = get_fake_vms(filesystem)

    if len(args) == 0:
        self.write_output("Usage: esxcli vm process {cmd} [cmd options]\r\n")
        self.write_output("Available Commands:\r\n")
        self.write_output("  kill                  Used to forcibly kill Virtual Machines that are stuck and not responding to normal stop operations.\r\n")
        self.write_output("  list                  List the virtual machines on this system. This command currently will only list running VMs on the system.\r\n")
    elif args[0] == "list":
        if fake_vms:
            for vm in fake_vms:
                self.write_output(f"World ID: {vm['World ID']}\r\n Name: {vm['Name']}\r\n File: {vm['Datastore']}\r\n")
        else:
            self.write_output("No VMs found.\r\n")
    elif args[0] == "kill":
        if len(args) < 2:
            self.write_output("Error. Missing required parameter.\r\n")
  
        else:
            world_id = int(args[1])
            matching_vms = [vm for vm in fake_vms if vm["World ID"] == world_id]
            if matching_vms:
                #self.write_output(f"Đã gửi yêu cầu tắt máy ảo với World ID: {world_id}\r\n")
                self.stderr = "Error: Operation not permitted"
                time.sleep(random.uniform(1,5))
                self.returncode = 1
                
            else:
                time.sleep(0.5)
                self.write_output(f"Unable to find a virtual machine with the world ID {world_id}\r\n")
    else:
        self.write_output(f"Error: Unknow 'vm process {args[0]}' \r\n")



def handle_network(self,filesystem, *args):
    if len(args) == 0:
        self.write_output("Usage: esxcli network {cmd} [cmd options]\r\n")
        self.write_output("Available Namespaces:\r\n")
        self.write_output("  ens                   Commands to list and manipulate Enhanced Networking Stack (ENS) feature on virtual switch.\r\n")
        self.write_output("  firewall              A set of commands for firewall related operations\r\n")
        self.write_output("  ip                    Operations that can be performed on vmknics\r\n")
        self.write_output("  multicast             Operations having to do with multicast\r\n")
        self.write_output("  nic                   Operations having to do with the configuration of Network Interface Card and getting and updating the NIC settings.\r\n")
        self.write_output("  port                  Commands to get information about a port\r\n")
        self.write_output("  sriovnic              Operations having to do with the configuration of SRIOV enabled Network Interface Card and getting and updating the NIC settings.\r\n")
        self.write_output("  vm                    A set of commands for VM related operations\r\n")
        self.write_output("  vswitch               Commands to list and manipulate Virtual Switches on an ESX host.\r\n")
        self.write_output("  diag                  Operations pertaining to network diagnostics\r\n")
    elif args[0] in ["firewall", "ip", "vm"]:
        handler_name = f"handle_network_{args[0]}"
        handler = globals().get(handler_name)
        if handler:
            handler(self,filesystem, *args[1:])
        else:
            self.write_output(f"Errorr: '{args[0]}'.\r\n")
    else:
        self.write_output(f"Error: Unknow command or namespace 'network {args[0]}' \r\n")


def handle_network_firewall(self,filesystem, *args):
    if len(args) == 0:
        self.write_output("Usage: esxcli network firewall {cmd} [cmd options]\r\n")
        self.write_output("Available Namespaces:\r\n")
        self.write_output("  ruleset               Commands to list and update firewall ruleset configuration\r\n")
        self.write_output("Available Commands:\r\n")
        self.write_output("  get                   Get the firewall status.\r\n")
        self.write_output("  load                  Load firewall module and rulesets configuration.\r\n")
        self.write_output("  refresh               Load ruleset configuration for firewall.\r\n")
        self.write_output("  set                   Set firewall enabled status and default action.\r\n")
        self.write_output("  unload                Allow unload firewall module.\r\n")
    elif args[0] == "get":
        self.write_output("   Default Action: DROP\r\n")
        self.write_output("   Enabled: true\r\n")
        self.write_output("   Loaded: true\r\n")
    elif args[0] == "ruleset":
        handle_network_firewall_ruleset(self,filesystem, *args[1:])
    else:
        self.write_output(f"Error: Unknow 'network firewall {args[0]}' \r\n")
        

def handle_network_firewall_ruleset(self,filesystem, *args):
    if len(args) == 0:
        self.write_output("Usage: esxcli network firewall ruleset {cmd} [cmd options]\r\n")
        self.write_output("Available Namespaces:\r\n")
        self.write_output("  allowedip             Commands to list and add/remove allowedip on ruleset\r\n")
        self.write_output("  client                Commands related to firewall ruleset clients\r\n")
        self.write_output("  rule                  Commands to list rules in the ruleset\r\n")
        self.write_output("Available Commands:\r\n")
        self.write_output("  list                  List the rulesets in firewall.\r\n")
        self.write_output("  set                   Set firewall ruleset status (allowedAll flag and enabled status).\r\n")
    else:
        self.write_output(f"Error: Unknow 'network firewall ruleset {args[0]}' \r\n")
        

def handle_network_ip(self,filesystem, *args):
    if len(args) == 0:
        self.write_output("  dns                   Operations pertaining to Domain Name Server configuration.\r\n")
        self.write_output("  interface             Operations having to do with the creation, management and deletion of VMkernel network interfaces (vmknic).\r\n")
        self.write_output("  ipsec                 Operations on Internet Protocol Security\r\n")
        self.write_output("  route                 Operations pertaining to route configuration\r\n")
        self.write_output("  connection            List active tcpip connections\r\n")
        self.write_output("  neighbor              Operations that can be performed on arp tables\r\n")
        self.write_output("  netstack              Operations having to do with the creation, management and deletion of VMkernel Netstack Instances.\r\n")
    elif args[0] == "dns":
        handle_network_ip_dns(self,filesystem, *args[1:])
    elif args[0] == "interface":
        handle_network_ip_interface(self,filesystem, *args[1:])
    elif args[0] == "connection":
        handle_network_ip_connection(self,filesystem)
    else:
        self.write_output(f"Error: Unknow command or namespace 'network ip {args[0]}' \r\n")
        

def handle_network_ip_dns(self,filesystem, *args):
    if len(args) == 0:
        self.write_output("Usage: esxcli network ip dns {cmd} [cmd options]\r\n")
        self.write_output("Available Namespaces:\r\n")
        self.write_output("  search                Operations pertaining to DNS search domain configuration.\r\n")
        self.write_output("  server                Operations pertaining to DNS server configuration.\r\n")
    elif args[0] == "search":
        self.write_output(" DNSSearch Domains: localdomain, example.com\r\n")
    elif args[0] == "server":
        self.write_output(" DNSServers: 192.168.1.1\r\n") 
    else:
        self.write_output(f"Error: Unknow command or namespace 'network ip dns {args[0]}' \r\n")
        

def handle_network_ip_interface(self,filesystem, *args):
    if len(args) == 0:
        self.write_output("Usage: esxcli network ip interface {cmd} [cmd options]\r\n")
        self.write_output("Available Namespaces:\r\n")
        self.write_output("  ipv4                  Commands to get and set IPv4 settings for vmknic.\r\n")
        self.write_output("  ipv6                  Commands to get and set IPv6 settings for vmknic.\r\n")
    elif args[0] == "ipv4":
        self.write_output("Name  IPv4 Address     IPv4 Netmask   IPv4 Broadcast   Address Type  Gateway        DHCP DNS\r\n")
        self.write_output("----  ---------------  -------------  ---------------  ------------  -------------  --------\r\n")
        self.write_output(f"vmk0  192.168.{random.randint(1,254)}.10  255.255.255.0  192.168.{random.randint(1,254)}.255  STATIC        192.168.{random.randint(1,254)}.1     false\r\n")
    elif args[0] == "ipv6":
        self.write_output("Interface  Address                   Netmask  Type    Status\r\n")
        self.write_output("---------  ------------------------  -------  ------  ------\r\n")
        self.write_output(f"vmk0       {':'.join('%04x' % random.randint(0, 0xffff) for _ in range(8))}       64  STATIC  PREFERRED\r\n")
    else:
        self.write_output(f"Error: Unknow command or namespace 'network ip interface {args[0]}' \r\n")
        

def handle_network_ip_connection(self,filesystem):
    self.write_output("Proto  Recv Q  Send Q  Local Address                     Foreign Address      State        World ID  CC Algo  World Name\r\n")
    self.write_output("-----  ------  ------  --------------------------------  -------------------  -----------  --------  -------  ----------\r\n")
    self.write_output(f"tcp         0       0  127.0.0.1:8307                    127.0.0.1:{random.randint(1024,65535)}      ESTABLISHED     67305  newreno  hostd-IO\r\n")
    self.write_output("tcp         0       0  127.0.0.1:18122                   127.0.0.1:8307       ESTABLISHED     67079  newreno  rhttpproxy-work\r\n")
    self.write_output(f"tcp         0       0  127.0.0.1:80                      127.0.0.1:{random.randint(1024,65535)}      ESTABLISHED     67083  newreno  rhttpproxy-IO\r\n")
    self.write_output(f"tcp         0       0  127.0.0.1:{random.randint(1024,65535)}                   127.0.0.1:80         ESTABLISHED     69426  newreno  python\r\n")
    self.write_output("tcp         0       0  127.0.0.1:57016                   127.0.0.1:8307       TIME_WAIT           0\r\n")
    self.write_output(f"tcp         0       0  127.0.0.1:{random.randint(1024,65535)}                   127.0.0.1:80         TIME_WAIT           0\r\n")
    self.write_output(f"tcp         0       0  127.0.0.1:8307                    127.0.0.1:{random.randint(1024,65535)}      CLOSE_WAIT      67306  newreno  hostd-IO\r\n")
    self.write_output(f"tcp         0       0  127.0.0.1:{random.randint(1024,65535)}                   127.0.0.1:8307       FIN_WAIT_2      67088  newreno  rhttpproxy-work\r\n")

def handle_network_vm(self,filesystem, *args):
    fake_vms = get_fake_vms(filesystem)

    if len(args) == 0:
        self.write_output("Usage: esxcli network vm {cmd} [cmd options]\r\n")
        self.write_output("Available Namespaces:\r\n")
        self.write_output("  port                  Command to list ports of a given VM\r\n")
        self.write_output("Available Commands:\r\n")
        self.write_output("  list                  List networking information for the VM's that have active ports.\r\n")
    elif args[0] == "list":
        if fake_vms:
            for vm in fake_vms:
                self.write_output(f"Network: {vm['Name']}\r\n")
                self.write_output(f"  MAC Address: {':'.join('%02x' % random.randint(0, 255) for _ in range(6))}\r\n")
                self.write_output(f"  IP Address: 192.168.{random.randint(1, 254)}.{random.randint(2, 254)}\r\n")
                self.write_output(f"  VLAN: {random.randint(1, 4094)}\r\n")
                self.write_output(f"  Portgroup: {vm['Name']}-portgroup\r\n")
                self.write_output("-" * 20) 
        else:
            self.write_output("No VMs found.\r\n")
    elif args[0] == "port":
        if len(args) < 2:
            self.write_output("Error: Missing required parameter\r\n")
            
        else:
            world_id = int(args[1])
            matching_vms = [vm for vm in fake_vms if vm["World ID"] == world_id]
            if matching_vms:
                self.write_output(f"  - Port ID: {random.randint(0, 65535)}\r\n")
                self.write_output(f"  - VLAN ID: {random.randint(0, 4094)}\r\n")
                self.write_output(f"  - MAC Address: {':'.join('%02x' % random.randint(0, 255) for _ in range(6))}\r\n")
            else:
                self.write_output(f"Not found: {world_id}\r\n")
    else:
        self.write_output(f"Error: Unknow 'network vm {args[0]}' \r\n")



def handle_storage(self,filesystem, *args):
    if len(args) == 0:
        self.write_output("Usage: esxcli storage {cmd} [cmd options]\r\n")
        self.write_output("Available Namespaces:\r\n")
        self.write_output(" core                  VMware core storage commands.\r\n")
        self.write_output(" hpp                   VMware High Performance Plugin (HPP).\r\n")
        self.write_output(" nfs                   Operations to create, manage, and remove Network Attached Storage filesystems.\r\n")
        self.write_output(" nfs41                 Operations to create, manage, and remove NFS v4.1 filesystems.\r\n")
        self.write_output(" nmp                   VMware Native Multipath Plugin (NMP). This is the VMware default implementation of the Pluggable Storage Architecture.\r\n")
        self.write_output(" san                   IO device management operations to the SAN devices on the system.\r\n")
        self.write_output(" vflash                virtual flash Management Operations on the system.\r\n")
        self.write_output(" vmfs                  VMFS operations.\r\n")
        self.write_output(" vvol                  Operations pertaining to Virtual Volumes\r\n")
        self.write_output(" filesystem            Operations pertaining to filesystems, also known as datastores, on the ESX host.\r\n")
        self.write_output(" iofilter              IOFilter related commands.\r\n")

    elif args[0] in ["vmfs", "filesystem"]:
        handler_name = f"handle_storage_{args[0]}"
        handler = globals().get(handler_name)
        if handler:
            handler(self,filesystem, *args[1:])
        else:
            self.write_output(f"Error: '{args[0]}'.\r\n")
    else:
        self.write_output(f"Error: Unknow command or namespace 'storage {args[0]}' \r\n")
        

def handle_storage_vmfs(self,filesystem, *args):
    if len(args) == 0:
        self.write_output("Usage: esxcli storage vmfs {cmd} [cmd options]\r\n")
        self.write_output("Available Namespaces:\r\n")
        self.write_output("  reclaim               Manage VMFS Space Reclamation\r\n")
        self.write_output("  snapshot              Manage VMFS snapshots.\r\n")
        self.write_output("  extent                Manage VMFS extents.\r\n")
        self.write_output("  host                  Manage hosts accessing a VMFS volume.\r\n")
        self.write_output("  lockmode              Manage VMFS array locking mode.\r\n")
        self.write_output("  pbcache               VMFS Pointer Block Cache statistics.\r\n")
    else:
        self.write_output(f"Error: Unknow 'storage vmfs {args[0]}' \r\n")



def handle_storage_filesystem(self,filesystem, *args):
    fake_vms = get_fake_vms(filesystem)

    if len(args) == 0:
        self.write_output("Usage: esxcli storage filesystem {cmd} [cmd options]\r\n")
        self.write_output("Available Commands:\r\n")
        self.write_output("  automount             Request mounting of known datastores not explicitly unmounted.\r\n")
        self.write_output("  list                  List the volumes available to the host. This includes VMFS, NAS, VFAT and UFS partitions.\r\n")
        self.write_output("  mount                 Connect to and mount an unmounted volume on the ESX host.\r\n")
        self.write_output("  rescan                Scan storage devices for new mountable filesystems.\r\n")
        self.write_output("  unmount               Disconnect and unmount and existing VMFS or NAS volume. This will not delete the configuration for the volume, but will remove the volume from the list of mounted volumes.\r\n")
    elif args[0] == "list":
        self.write_output("Mount Point                                        Volume Name                                 UUID                                 Mounted  Type           Size         Free\r\n")
        self.write_output("-------------------------------------------------  ------------------------------------------  -----------------------------------  -------  ------  -----------  -----------\r\n")
        if fake_vms:
            for vm in fake_vms:
                mount_point = f"/vmfs/volumes/{vm['Datastore']}/{vm['Name']}"
                volume_name = vm['Name']
                uuids = str(uuid.uuid4())
                mounted = "true"
                type = "VMFS"
                size = f"{random.randint(100, 500)}GB"
                free = f"{random.randint(10, 90)}GB"
                self.write_output(f"{mount_point:<50} {volume_name:<50} {uuids:<50} {mounted:<8} {type:<11} {size:<12} {free}\r\n")
        else:
            self.write_output("No datastores found.\r\n")
    else:
        self.write_output(f"Error: Unknow 'storage filesystem {args[0]}' \r\n")



def handle_system(self,filesystem, *args):
    if len(args) == 0:
        self.write_output("Usage: esxcli system {cmd} [cmd options]\r\n")
        self.write_output("Available Namespaces:\r\n")
        self.write_output("  auditrecords          Audit record handling.\r\n")
        self.write_output("  boot                  Operations relating to host boot that allow manipulation of VMkernel boot time configuration.\r\n")
        self.write_output("  coredump              Operations pertaining to the VMkernel Core dump configuration.\r\n")
        self.write_output("  module                Operations that allow manipulation of the VMkernel loadable modules and device drivers. Operations include load, list and setting options.\r\n")
        self.write_output("  ntp                   Commands pertaining to Network Time Protocol Agent configuration.\r\n")
        self.write_output("  process               Commands relating to running processes.\r\n")
        self.write_output("  ptp                   Commands pertaining to Precision Time Protocol Agent configuration.\r\n")
        self.write_output("  secpolicy             Options related to VMkernel access control subsystem. These options are typically in place for specific workarounds or debugging. These commands should be used at the direction of VMware Support Engineers.\r\n")
        self.write_output("  security              Operations pertaining to server authentication.\r\n")
        self.write_output("  settings              Operations that allow viewing and manipulation of system settings.\r\n")
        self.write_output("  slp                   Commands pertaining to Service Location Protocol (SLP).\r\n")
        self.write_output("  stats                 Access to various system statistics\r\n")
        self.write_output("  syslog                Operations relating to system logging.\r\n")
        self.write_output("  visorfs               Operations pertaining to the visorfs memory filesytem.\r\n")
        self.write_output("  wbem                  Commands pertaining to WEB Based Enterprise Management (WBEM) Agent configuration.\r\n")
        self.write_output("  account               Manage user accounts.\r\n")
        self.write_output("  clock                 Commands to get and set system clock parameters\r\n")
        self.write_output("  hostname              Operations pertaining the network name of the ESX host.\r\n")
        self.write_output("  maintenanceMode       Command to manage the system's maintenance mode.\r\n")
        self.write_output("  permission            Manage permissions for accessing the ESXi host.\r\n")
        self.write_output("  shutdown              Command to shutdown the system.\r\n")
        self.write_output("  snmp                  Commands pertaining to SNMPv1/v2c/v3 Agent configuration.\r\n")
        self.write_output("  time                  Commands to get and set system time.\r\n")
        self.write_output("  uuid                  Get the system UUID\r\n")
        self.write_output("  version               Commands to get version information.\r\n")
        self.write_output("  welcomemsg            Commands to get and set the welcome banner for DCUI.\r\n")
    elif args[0] in ["account", "hostname", "permission", "time", "uuid", "version"]:
        handler_name = f"handle_system_{args[0]}"
        handler = globals().get(handler_name)
        if handler:
            handler(self,*args[1:])
        else:
            self.write_output(f"Error: '{args[0]}'.\r\n")
            
    else:
        self.write_output(f"Error: Unknow command or namespace 'system {args[0]}' \r\n")

def handle_system_account(self,*args):
    if len(args) == 0:
        self.write_output("Usage: esxcli system account {cmd} [cmd options]\r\n")
        self.write_output("Available Commands:\r\n")
        self.write_output("  add                   Create a new local user account.\r\n")
        self.write_output("  list                  List local user accounts.\r\n")
        self.write_output("  remove                Remove an existing local user account.\r\n")
        self.write_output("  set                   Modify an existing local user account.\r\n")
    elif args[0] == "list":
        self.write_output("User ID  Description\r\n")
        self.write_output("-------  -----------\r\n")
        self.write_output("root     Administrator\r\n")
        self.write_output("dcui     DCUI User\r\n")
        self.write_output("vpxuser  VMware VirtualCenter administration account\r\n")
        self.write_output(f"user{random.randint(1,100)}     Example User\r\n")
    else:
        self.write_output(f"Error: Unknow 'system account {args[0]}' \r\n")
        

def handle_system_hostname(self,*args):
    self.write_output("   Domain Name: localdomain\r\n")
    self.write_output(f"   Fully Qualified Domain Name: esx-{random.randint(1, 10)}.localdomain\r\n")
    self.write_output(f"   Host Name: esx-{random.randint(1, 10)}\r\n")

def handle_system_time(self,*args):
    current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ\r\n")
    self.write_output(current_time)

def handle_system_uuid(self,*args):
    self.write_output(str(uuid.uuid4())) 

def handle_system_version(self,*args):
    self.write_output("   Product: VMware ESXi\r\n")
    self.write_output(f"   Version: 7.0.{random.randint(0, 3)}\r\n")  
    self.write_output(f"   Build: Releasebuild-17325{random.randint(1000, 9999)}\r\n")
    self.write_output("   Update: 1\r\n")
    self.write_output(f"   Patch: {random.randint(1, 50)}\r\n")


#handle_command
def handle_unimplemented_namespace(self,filesystem, namespace, *args):

    time.sleep(3)
    self.write_output(f"Error: Unknown command or namespace {namespace}\r\n")


def handle_namespace(self,filesystem, namespace, *args):

    handlers = {
        "vm": handle_vm,
        "network": handle_network,
        "storage": handle_storage,
        "system": handle_system,
    }

    if namespace in handlers:
        handlers[namespace](self,filesystem, *args)  
    else:
        handle_unimplemented_namespace(self,filesystem, namespace, *args)


def handle_command(self,filesystem, command):
    parts = command.split()

    namespace = parts[0]
    arguments = parts[1:]

    handle_namespace(self,filesystem, namespace, *arguments)

class ESXiEsxcliCommand(cmd.SimpleCommand):
    """
    /bin/esxcli
    """
    def run(self):
        if len(self.args) == 0 or self.args[0] in ["-?", "--help"]:
            show_help(self)
        elif len(self.args) >= 1:
            command = " ".join(self.args)
            handle_command(self,self.fs, command)
        else:
            self.write_output("Error.\r\n")

