import ESXi_fs as fs
import ESXi_command as cmd

class ESXiUnameCommand(cmd.SimpleCommand):
    """
    /bin/uname
    """
    def run(self):
        if "--help" in self.args or "-h" in self.args:
            self.show_help()
            return

        kernel_name = "VMkernel"
        nodename = "LuaGa.localdomain"
        kernel_release = "7.0.1"
        kernel_version = "#1 SMP Release build-17325551 Dec 15 2020 04:18:26"
        machine = "x86_64"
        hardware_platform = "x86_64"
        operating_system = "ESXi"

        output = []
        for opt in self.args:
            if opt == "-a":
                output = [
                    kernel_name,
                    nodename,
                    kernel_release,
                    kernel_version,
                    machine,
                    hardware_platform,
                    operating_system,
                ]
                break
            elif opt == "-s":
                output.append(kernel_name)
            elif opt == "-n":
                output.append(nodename)
            elif opt == "-r":
                output.append(kernel_release)
            elif opt == "-v":
                output.append(kernel_version)
            elif opt == "-m":
                output.append(machine)
            elif opt == "-p":
                output.append("x86_64") 
            elif opt == "-i":
                output.append(hardware_platform)
            elif opt == "-o":
                output.append(operating_system)

        if not output:
            output.append(kernel_name)

        self.write_output(" ".join(output) + "\n")

    def show_help(self):
        self.write_output(
            """Usage: uname [-amnrspvio]\r

Print system information\r

        -a      Print all\r
        -m      The machine (hardware) type\r
        -n      Hostname\r
        -r      Kernel release\r
        -s      Kernel name (default)\r
        -p      Processor type\r
        -v      Kernel version\r
        -i      The hardware platform\r
        -o      OS name\r
"""
        )