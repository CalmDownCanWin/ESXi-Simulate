import ESXi_fs as fs
import ESXi_command as cmd
import os
import random

class ESXiEnvCommand(cmd.SimpleCommand):
    """
    /bin/env
    """
    def run(self):
        environ = {
            "USER": "root",
            "SHLVL": "1",
            "HOME": "/",
            "SSH_TTY": f"/dev/pts/{random.randint(0, 999)}",
            "PS1": "[root@\h:\w]", 
            "LOGNAME": "root",
            "VI_USERNAME": "root",
            "TERM": "xterm-256color",
            "PATH": "/bin:/sbin", 
            "LANG": "en_US.UTF-8",
            "SHELL": "/bin/sh",
            "LC_ALL": "en_US.UTF-8",
            "PWD": "/",
            "TMOUT": "0"
        }

        # output
        for key, value in environ.items():
            self.write_output(f"{key}={value}\r\n")