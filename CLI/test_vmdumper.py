import ESXi_fs as fs
import ESXi_command as cmd
import random
import os

class ESXiVmdumperCommand(cmd.SimpleCommand):
    """
    Lệnh vmdumper mô phỏng cho honeypot ESXi.
    """

    def run(self):
        if "-h" in self.args or "--help" in self.args:
            self.show_help()
            return

        if len(self.args) < 2:
            self.show_help()
            self.returncode = 1
            return

        # Xử lý options
        self.list_vms = False
        options = [arg for arg in self.args if arg.startswith("-")]
        args = [arg for arg in self.args if not arg.startswith("-")]
        
        for opt in options:
            if opt == "-l":
                self.list_vms = True

        if self.list_vms:
            self.list_running_vms()
            return

        if len(args) < 2:
            self.show_help()
            self.returncode = 1
            return

        world_id = args[0]
        action = args[1]

        print(f"Dumping VM with World ID {world_id} using action '{action}'...\n")

        # ... (giữ nguyên phần tạo thông báo giả dựa trên action)
        if action == "unsync":
            print("Successfully initialized unsynchronized dump process.\n")
            print("Writing unsynchronized dump data to file...\n")
            print("Unsynchronized dump completed successfully.\n")
        elif action == "sync":
            print("Successfully initialized synchronized dump process.\n")
            print("Synchronizing memory...\n")
            print("Writing synchronized dump data to file...\n")
            print("Synchronized dump completed successfully.\n")
        elif action in ["vmx", "vmx_force"]:
            print("Suspending VM...\n")
            print(f"Writing VMX configuration data to file...\n")
            print("VMX dump completed successfully.\n")
        elif action == "samples_on":
            print("Enabling performance counters...\n")
        elif action == "samples_off":
            print("Disabling performance counters...\n")
        elif action == "nmi":
            print("Sending NMI to VM...\n")
        elif action == "backtrace":
            print("Collecting backtrace...\n")
        else:
            print("Unknown action.\n")
            self.returncode = 1
            return

        print(f"VM with World ID {world_id} successfully shut down.\n")
        self.handle_CTRL_C()

    def list_running_vms(self):
        """Liệt kê thông tin máy ảo giả từ filesystem."""
        vm_dir = os.path.join(self.fs.root, "vmfs/volumes")
        if not self.fs.isdir(vm_dir):
            self.stderr = "No VMs found.\n"
            return

        for datastore in self.fs.listdir(vm_dir):
            datastore_path = os.path.join(vm_dir, datastore)
            if self.fs.isdir(datastore_path):
                for vm_folder in self.fs.listdir(datastore_path):
                    vmx_path = os.path.join(datastore_path, vm_folder, f"{vm_folder}.vmx")
                    if self.fs.isfile(vmx_path):
                        world_id = random.randint(1000, 9999)  # Tạo World ID giả
                        print(f"World ID: {world_id} Name: {vm_folder}\n")

    def show_help(self):
        """Hiển thị thông tin trợ giúp."""
        print("vmdumper: [options] <world id> <unsync|sync|vmx|vmx_force|samples_on|samples_off|nmi|backtrace>\n")
        print("         -f: ignore vsi version check\n")
        print("         -h: print friendly help message\n")
        print("         -l: print information about running VMs\n")
        print("         -g: log specified text to the vmkernel log\n")