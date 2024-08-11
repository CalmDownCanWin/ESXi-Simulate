import ESXi_fs as fs
import ESXi_command as cmd
import random
import os
from utils import disconnect_attacker

class ESXiVmdumperCommand(cmd.SimpleCommand):
    """
    Lệnh vmdumper mô phỏng cho honeypot ESXi.
    """

    def run(self):
        if "-h" in self.args or "--help" in self.args:
            self.show_help()
            return

        # Xử lý options
        self.list_vms = False
        options = [arg for arg in self.args if arg.startswith("-")]
        args = [arg for arg in self.args if not arg.startswith("-")]
        
        for opt in options:
            if opt == "-l":
                self.list_vms = True

        if len(args) < 2:
            if self.list_vms:
                self.list_running_vms()
                return
            self.show_help()
            self.returncode = 1
            return

        world_id = args[0]
        action = args[1]

        self.write_output(f"Dumping VM with World ID {world_id} using action '{action}'...\r\n")

        # ... (giữ nguyên phần tạo thông báo giả dựa trên action)
        if action == "unsync":
            self.write_output("Successfully initialized unsynchronized dump process.\r\n")
            self.write_output("Writing unsynchronized dump data to file...\r\n")
            self.write_output("Unsynchronized dump completed successfully.\r\n")
        elif action == "sync":
            self.write_output("Successfully initialized synchronized dump process.\r\n")
            self.write_output("Synchronizing memory...\r\n")
            self.write_output("Writing synchronized dump data to file...\r\n")
            self.write_output("Synchronized dump completed successfully.\r\n")
        elif action in ["vmx", "vmx_force"]:
            self.write_output("Suspending VM...\r\n")
            self.write_output(f"Writing VMX configuration data to file...\r\n")
            self.write_output("VMX dump completed successfully.\r\n")
        elif action == "samples_on":
            self.write_output("Enabling performance counters...\r\n")
        elif action == "samples_off":
            self.write_output("Disabling performance counters...\r\n")
        elif action == "nmi":
            self.write_output("Sending NMI to VM...\r\n")
        elif action == "backtrace":
            self.write_output("Collecting backtrace...\r\n")
        else:
            self.write_output("Unknown action.\r\n")
            self.returncode = 1
            return

        self.write_output(f"VM with World ID {world_id} successfully shut down.\r\n")
        disconnect_attacker()

    def list_running_vms(self):
        """Liệt kê thông tin máy ảo giả từ filesystem."""
        vm_dir = os.path.join(self.fs.root, "vmfs/volumes")
        if not self.fs.isdir(vm_dir):
            self.stderr = "No VMs found.\r\n"
            return

        for datastore in self.fs.listdir(vm_dir):
            datastore_path = os.path.join(vm_dir, datastore)
            if self.fs.isdir(datastore_path):
                for vm_folder in self.fs.listdir(datastore_path):
                    vmx_path = os.path.join(datastore_path, vm_folder, f"{vm_folder}.vmx")
                    if self.fs.isfile(vmx_path):
                        world_id = random.randint(1000, 9999)  # Tạo World ID giả
                        self.write_output(f"World ID: {world_id} Name: {vm_folder}\r\n")

    def show_help(self):
        """Hiển thị thông tin trợ giúp."""
        self.write_output("vmdumper: [options] <world id> <unsync|sync|vmx|vmx_force|samples_on|samples_off|nmi|backtrace>\r\n")
        self.write_output("         -f: ignore vsi version check\r\n")
        self.write_output("         -h: self.write_output friendly help message\r\n")
        self.write_output("         -l: self.write_output information about running VMs\r\n")
        self.write_output("         -g: log specified text to the vmkernel log\r\n")
