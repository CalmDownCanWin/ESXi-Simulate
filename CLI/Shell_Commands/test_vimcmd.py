import ESXi_fs as fs
import ESXi_command as cmd
import random
import os
import re
import error_handler as er

class ESXiVimCmdCommand(cmd.SimpleCommand):
    """
    /bin/vim-cmd
    """

    def run(self):
        if len(self.args) == 0 or self.args[0] == "help":
            self.write_output("Commands available under /:\r\n")
            self.write_output("hbrsvc/       internalsvc/  solo/         vmsvc/\r\n")
            self.write_output("hostsvc/      proxysvc/     vimsvc/       help\r\n")
        else:
            command = " ".join(self.args) 

            if command.startswith("vmsvc/"):
                self.handle_vmsvc(command[6:]) 
            elif command.startswith("hostsvc/"):
                self.handle_hostsvc(command[8:]) 
            else:
                self.stderr = f"Invalid command '{command}'"
                self.returncode = 1

    def handle_vmsvc(self, command):
        if command == "":
            self.write_output("Commands available under vmsvc/:\r\r\n")
            self.write_output("acquiremksticket                 get.snapshotinfo\r\n")
            self.write_output("acquireticket                    get.spaceNeededForConsolidation\r\n")
            self.write_output("createdummyvm                    get.summary\r\n")
            self.write_output("destroy                          get.tasklist\r\n")
            self.write_output("device.connection                getallvms\r\n")
            self.write_output("device.connusbdev                gethostconstraints\r\n")
            self.write_output("device.ctlradd                   message\r\n")
            self.write_output("device.ctlrremove                power.getstate\r\n")
            self.write_output("device.disconnusbdev             power.hibernate\r\n")
            self.write_output("device.diskadd                   power.off\r\n")
            self.write_output("device.diskaddexisting           power.on\r\n")
            self.write_output("device.diskextend                power.reboot\r\n")
            self.write_output("device.diskremove                power.reset\r\n")
            self.write_output("device.getdevices                power.shutdown\r\n")
            self.write_output("device.nvdimmadd                 power.suspend\r\n")
            self.write_output("device.nvdimmremove              power.suspendResume\r\n")
            self.write_output("device.toolsSyncSet              queryftcompat\r\n")
            self.write_output("devices.createnic                reload\r\n")
            self.write_output("get.capability                   setscreenres\r\n")
            self.write_output("get.config                       snapshot.create\r\n")
            self.write_output("get.config.cpuidmask             snapshot.dumpoption\r\n")
            self.write_output("get.configoption                 snapshot.get\r\n")
            self.write_output("get.datastores                   snapshot.remove\r\n")
            self.write_output("get.disabledmethods              snapshot.removeall\r\n")
            self.write_output("get.environment                  snapshot.revert\r\n")
            self.write_output("get.filelayout                   snapshot.setoption\r\n")
            self.write_output("get.filelayoutex                 tools.cancelinstall\r\n")
            self.write_output("get.guest                        tools.install\r\n")
            self.write_output("get.guestheartbeatStatus         tools.upgrade\r\n")
            self.write_output("get.managedentitystatus          unregister\r\n")
            self.write_output("get.networks                     upgrade\r\n")
            self.write_output("get.runtime\r\n")
        elif command == "getallvms":
            self.get_all_vms()
        elif command.startswith(("power.off", "power.shutdown", "power.suspend")):
            match = re.search(r"(power\.[^\s]+)\s*(\d+)", command)  
            if match:
                action = match.group(1)
                vmid = match.group(2)
                self.stderr = f"Error processing command 'vim-cmd vmsvc/{action} {vmid}'"
                self.returncode = 1
                
            else:
                self.stdout = f"\rInsufficient arguments.\r\nUsage: {command} vmid\r\n"
                if command.startswith(("power.off")):
                    self.stderr = f"Power off the specified virtual machines"
                elif command.startswith(("power.shutdown")):
                    self.stderr = f"Shutdown the guest OS"
                elif command.startswith(("power.suspend")):
                    self.stderr = f"Suspend the specified virtual machines"
                self.returncode = 1
        else:
            self.stderr = f"Invalid command 'vim-cmd vmsvc/{command}'"
            self.returncode = 1

    def get_all_vms(self):
        vm_dir = os.path.join(self.fs.root, "vmfs/volumes")
        if not self.fs.isdir(vm_dir):
            self.stderr = "No VMs found.\r\n"
            return

        self.write_output("Vmid   Name                 File                   Guest OS       Version   Annotation\r\n")
        self.write_output("------ --------------------- ------------------------ --------------------- ---------- --------\r\n")
        for datastore in self.fs.listdir(vm_dir):
            datastore_path = os.path.join(vm_dir, datastore)
            if self.fs.isdir(datastore_path):
                for vm_folder in self.fs.listdir(datastore_path):
                    vmx_path = os.path.join(datastore_path, vm_folder, f"{vm_folder}.vmx")
                    if self.fs.isfile(vmx_path):
                        vmid = random.randint(100, 999)
                        guest_os = random.choice(["ubuntu64Guest", "centos64Guest", "windows8Server64Guest"])
                        version = f"vmx-{random.randint(10, 20)}"
                        annotation = f"VM-{random.randint(1,10)}" # annotation
                        self.write_output(f"{vmid:<6} {vm_folder:<20} [{datastore}] {vm_folder}/{vm_folder}.vmx   {guest_os:<15} {version:<8} {annotation}\r\n")

    def handle_hostsvc(self, command):
        if command == "":
            self.write_output("Commands available under hostsvc/:\r\n")
            self.write_output("advopt/                   enable_ssh                refresh_services\r\n")
            self.write_output("autostartmanager/         firewall_disable_ruleset  reset_service\r\n")
            self.write_output("datastore/                firewall_enable_ruleset   runtimeinfo\r\n")
            self.write_output("datastorebrowser/         get_service_status        set_hostid\r\n")
            self.write_output("firmware/                 hostconfig                standby_mode_enter\r\n")
            self.write_output("net/                      hosthardware              standby_mode_exit\r\n")
            self.write_output("rsrc/                     hostsummary               start_esx_shell\r\n")
            self.write_output("storage/                  maintenance_mode_enter    start_service\r\n")
            self.write_output("summary/                  maintenance_mode_exit     start_ssh\r\n")
            self.write_output("vmotion/                  pci_add                   stop_esx_shell\r\n")
            self.write_output("cpuinfo                   pci_remove                stop_service\r\n")
            self.write_output("disable_esx_shell         queryconnectioninfo       stop_ssh\r\n")
            self.write_output("disable_ssh               querydisabledmethods      task_list\r\n")
            self.write_output("enable_esx_shell          refresh_firewall          updateSSLThumbself.write_outputsInfo")
        elif command == "autostartmanager":
            self.handle_hostsvc_autostartmanager(command[24:])
        elif command == "enable_ssh":
            self.write_output("SSH service successfully enabled.\r\n")
           
        else:
            self.stderr = f"Invalid command 'vim-cmd hostsvc/ {command}'"
            self.returncode = 1
           

    def handle_hostsvc_autostartmanager(self, command):
        if command == "":
            self.write_output("Commands available under hostsvc/autostartmanager/:\r\n")
            self.write_output("autostart              get_autostartseq       update_defaults\r\n")
            self.write_output("autostop               get_defaults\r\n")
            self.write_output("enable_autostart       update_autostartentry\r\n")
        elif command.startswith("enable_autostart"):
            self.write_output("Command executed successfully.\r\n")
        else:
            self.stderr = f"Invalid command 'vim-cmd hostsvc/autostartmanager/ {command}'"
            self.returncode = 1
           
