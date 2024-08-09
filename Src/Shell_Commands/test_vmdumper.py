import ESXi_fs as fs
import ESXi_command as cmd
import random
import os


class ESXiVmdumperCommand(cmd.SimpleCommand):
    """
    /bin/vmdumper
    """

    def run(self):
        if "-h" in self.args or "--help" in self.args:
            self.show_help()
            return

        # options
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

        #self.write_output(f"Dumping VM with World ID {world_id} using action '{action}'...\r\n")

        if action == "unsync":
            self.write_output("Dumping unsync cores...\r\n")
        elif action == "sync":
            self.write_output("Dumping sync cores...\r\n")
        elif action == "vmx":
            self.write_output("Dumping vmx core...\r\n")
        elif action == "vmx_force":
            self.write_output("Dumping vmx core (force)...\r\n")
        elif action == "samples_on":
            self.write_output("Turning VM samples on...\r\n")
        elif action == "samples_off":
            self.write_output("Turning VM samples off...\r\n")
        elif action == "nmi":
            self.write_output("Sending NMI to guest...\r\n")
        elif action == "backtrace":
            self.write_output("Dumping world backtrace to log...\r\n")
        else:
            self.show_help()
            return
        
        self.write_output(f"Operation failed with error: Invalid world\r\n")
       

    def list_running_vms(self):
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
                        world_id = random.randint(1000, 9999)
                        self.write_output(f"World ID: {world_id} Name: {vm_folder}\r\n")

    def show_help(self):
        self.write_output("vmdumper: [options] <world id> <unsync|sync|vmx|vmx_force|samples_on|samples_off|nmi|backtrace>\r\n")
        self.write_output("         -f: ignore vsi version check\r\n")
        self.write_output("         -h: self.write_output friendly help message\r\n")
        self.write_output("         -l: self.write_output information about running VMs\r\n")
        self.write_output("         -g: log specified text to the vmkernel log\r\n")
