import ESXi_fs as fs
import ESXi_command as cmd
from test_esxcli import ESXiEsxcliCommand, disconnect_attacker,get_fake_vms, handle_vm, handle_network, handle_storage
from test_vimcmd import ESXiVimCmdCommand 
from test_vmdumper import ESXiVmdumperCommand

import re
import shlex 

class ESXiShCommand(cmd.SimpleCommand):
    """
    Lệnh sh mô phỏng cho honeypot ESXi.
    """

    # Dictionary ánh xạ keyword với pattern và handler
COMMAND_PATTERNS = {
    "esxcli": {
        r"esxcli vm process list": (handle_vm, ["process", "list"]),
        r"esxcli vm process kill ": (handle_vm, ["process", "kill"]),
        r"esxcli network firewall get": (handle_network, ["firewall", "get"]),
        r"esxcli storage filesystem list": (handle_storage, ["filesystem", "list"])
        # Thêm các pattern và handler cho esxcli khác vào đây
    },
    "vmdumper": {
        r"vmdumper -l": (ESXiVmdumperCommand, ["-l"]),
        # Thêm các pattern và handler cho vmdumper khác vào đây
    },
    "vim-cmd": {
        r"vim-cmd vmsvc/getallvms": (ESXiVimCmdCommand, ["vmsvc/", "getallvms"]),
        # Thêm các pattern và handler cho vim-cmd khác vào đây
    },
}

class ESXiShCommand(cmd.SimpleCommand):
    """
    Lệnh sh mô phỏng cho honeypot ESXi.
    """


    def run(self):
        if self.check_arguments(1):
            script_file = self.args[0]
        # ... (Kiểm tra file tồn tại)

        try:
            with self.fs.open(script_file, "r") as f:
                script = f.read()

            found_command = False
            # Thực thi từng command
            for keyword, patterns in COMMAND_PATTERNS.items():
                for pattern, (handler, handler_args) in patterns.items():
                    match = re.search(pattern, script)
                    if match:
                        found_command = True
                        if callable(handler):  # Handler là function
                            # Xử lý command bằng function
                            if match.groups():
                                # Nếu regex có group, truyền giá trị group cho handler
                                handler(self,self.fs, *handler_args, *match.groups())
                            else:
                                handler(self,self.fs, *handler_args)
                        else:  # Handler là class
                            # Xử lý command bằng class
                            command_obj = handler(keyword, handler_args, self.cwd, self.fs)
                            command_obj.run()
                            self.stdout += command_obj.get_output()
                            self.stderr += command_obj.get_error()

            if not found_command:
                self.stderr = "sh: <script_file>: not executable: magic 7F 45 4C 46 02 01 01 00 00 00 00 00 00 00 00 00"  # Mô phỏng lỗi ELF
                self.returncode = 126 # Error code not executable 
                disconnect_attacker() # Ngắt kết nối attacker

        except (fs.FileNotFoundError, PermissionError) as e:
            self.stderr = f"sh: {script_file}: {e}"
            self.returncode = 1
    
