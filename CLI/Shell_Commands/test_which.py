import ESXi_fs as fs
import ESXi_command as cmd
import os

class ESXiWhichCommand(cmd.SimpleCommand):
    """
    /bin/which
    """
    def run(self):
        if not self.args or "PATH" not in self.environ:
            return

        for program in self.args:
            if program in ["ls", "cat", "touch", "esxcli", "vim-cmd", "vmdumper", "rm", "mkdir", "rmdir", "cp", "mv", "pwd", "ping", "ssh", "uname", "wc", "which", "echo", "wget", "scp"]:
                self.write_output(f"/bin/{program}\n")
                break
