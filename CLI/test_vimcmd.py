import ESXi_fs as fs
import ESXi_command as cmd
import random
import os

class ESXiVimCmdCommand(cmd.SimpleCommand):
    """
    Lệnh vim-cmd mô phỏng cho honeypot ESXi.
    """

    def run(self):
        if len(self.args) == 0 or self.args[0] == "help":
            print("Commands available under /:")
            print("hbrsvc/       internalsvc/  solo/         vmsvc/")
            print("hostsvc/      proxysvc/     vimsvc/       help")
        else:
            # Gộp tất cả các arguments lại thành một chuỗi
            command = " ".join(self.args) 

            if command.startswith("vmsvc/"):
                self.handle_vmsvc(command[6:]) # Loại bỏ "vmsvc/"
            elif command.startswith("hostsvc/"):
                self.handle_hostsvc(command[8:]) # Loại bỏ "hostsvc/"
            else:
                self.stderr = f"Invalid command '{command}'"
                self.returncode = 1

    def handle_vmsvc(self, command):
        """Xử lý namespace 'vim-cmd vmsvc/'."""
        if command == "":
            print("Commands available under vmsvc/:")
            # ... (In danh sách commands)
            print("acquiremksticket                 get.snapshotinfo")
            print("acquireticket                    get.spaceNeededForConsolidation")
            print("createdummyvm                    get.summary")
            print("destroy                          get.tasklist")
            print("device.connection                getallvms")
            print("device.connusbdev                gethostconstraints")
            print("device.ctlradd                   message")
            print("device.ctlrremove                power.getstate")
            print("device.disconnusbdev             power.hibernate")
            print("device.diskadd                   power.off")
            print("device.diskaddexisting           power.on")
            print("device.diskextend                power.reboot")
            print("device.diskremove                power.reset")
            print("device.getdevices                power.shutdown")
            print("device.nvdimmadd                 power.suspend")
            print("device.nvdimmremove              power.suspendResume")
            print("device.toolsSyncSet              queryftcompat")
            print("devices.createnic                reload")
            print("get.capability                   setscreenres")
            print("get.config                       snapshot.create")
            print("get.config.cpuidmask             snapshot.dumpoption")
            print("get.configoption                 snapshot.get")
            print("get.datastores                   snapshot.remove")
            print("get.disabledmethods              snapshot.removeall")
            print("get.environment                  snapshot.revert")
            print("get.filelayout                   snapshot.setoption")
            print("get.filelayoutex                 tools.cancelinstall")
            print("get.guest                        tools.install")
            print("get.guestheartbeatStatus         tools.upgrade")
            print("get.managedentitystatus          unregister")
            print("get.networks                     upgrade")
            print("get.runtime")
        elif command == "getallvms":
            self.get_all_vms()
        elif command in ["power.off", "power.shutdown", "power.suspend"]:
            # Tách vmid từ command
            parts = command.split(" ")
            if len(parts) < 2:
                self.stderr = "Insufficient arguments."
                self.stderr += f"\nUsage: {command} vmid"
                self.returncode = 1
            else:
                vmid = parts[1]
                self.stderr = f"Error processing command 'vim-cmd vmsvc/{command} {vmid}'"
                self.returncode = 1
                self.handle_CTRL_C()  # Ngắt kết nối
        else:
            self.stderr = f"Invalid command 'vim-cmd vmsvc/ {command}'"
            self.returncode = 1

    def get_all_vms(self):
        """Lấy thông tin máy ảo giả từ filesystem."""
        vm_dir = os.path.join(self.fs.root, "vmfs/volumes")
        if not self.fs.isdir(vm_dir):
            self.stderr = "No VMs found.\n"
            return

        print("Vmid   Name                 File                   Guest OS       Version   Annotation\n")
        for datastore in self.fs.listdir(vm_dir):
            datastore_path = os.path.join(vm_dir, datastore)
            if self.fs.isdir(datastore_path):
                for vm_folder in self.fs.listdir(datastore_path):
                    vmx_path = os.path.join(datastore_path, vm_folder, f"{vm_folder}.vmx")
                    if self.fs.isfile(vmx_path):
                        vmid = random.randint(100, 999)
                        guest_os = random.choice(["ubuntu64Guest", "centos64Guest", "windows8Server64Guest"])
                        version = f"vmx-{random.randint(10, 20)}"
                        annotation = f"VM-{random.randint(1,10)}" # annotation ngẫu nhiên 
                        print(f"{vmid:<6} {vm_folder:<20} [{datastore}] {vm_folder}/{vm_folder}.vmx   {guest_os:<15} {version:<8} {annotation}")

    def handle_hostsvc(self, command):
        """Xử lý namespace 'vim-cmd hostsvc/'."""
        if command == "":
            print("Commands available under hostsvc/:")
            # ... (in danh sách commands)
            print("advopt/                   enable_ssh                refresh_services")
            print("autostartmanager/         firewall_disable_ruleset  reset_service")
            print("datastore/                firewall_enable_ruleset   runtimeinfo")
            print("datastorebrowser/         get_service_status        set_hostid")
            print("firmware/                 hostconfig                standby_mode_enter")
            print("net/                      hosthardware              standby_mode_exit")
            print("rsrc/                     hostsummary               start_esx_shell")
            print("storage/                  maintenance_mode_enter    start_service")
            print("summary/                  maintenance_mode_exit     start_ssh")
            print("vmotion/                  pci_add                   stop_esx_shell")
            print("cpuinfo                   pci_remove                stop_service")
            print("disable_esx_shell         queryconnectioninfo       stop_ssh")
            print("disable_ssh               querydisabledmethods      task_list")
            print("enable_esx_shell          refresh_firewall          updateSSLThumbprintsInfo")
        elif command == "autostartmanager":
            self.handle_hostsvc_autostartmanager(command[24:]) # Loại bỏ "autostartmanager"
        elif command == "enable_ssh":
            print("SSH service successfully enabled.\n")
            self.handle_CTRL_C()  # Ngắt kết nối
        else:
            self.stderr = f"Invalid command 'vim-cmd hostsvc/ {command}'"
            self.returncode = 1
            self.handle_CTRL_C()  # Ngắt kết nối

    def handle_hostsvc_autostartmanager(self, command):
        """Xử lý namespace 'vim-cmd hostsvc/autostartmanager/'."""
        if command == "":
            print("Commands available under hostsvc/autostartmanager/:")
            print("autostart              get_autostartseq       update_defaults")
            print("autostop               get_defaults")
            print("enable_autostart       update_autostartentry")
        elif command == "enable_autostart":
            print("Command executed successfully.\n")
        else:
            self.stderr = f"Invalid command 'vim-cmd hostsvc/autostartmanager/ {command}'"
            self.returncode = 1
            self.handle_CTRL_C()  # Ngắt kết nối