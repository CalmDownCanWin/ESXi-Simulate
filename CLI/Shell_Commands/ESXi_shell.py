import ESXi_fs as fs
import ESXi_command as cmd
import shlex
import os

from test_cat import ESXiCatCommand
from test_ls import ESXiLsCommand
from test_ping import ESXiPingCommand
from test_chmod import ESXiChmodCommand
from test_wget import ESXiWgetCommand
from test_scp import ESXiScpCommand

from test_vmdumper import ESXiVmdumperCommand
from test_vimcmd import ESXiVimCmdCommand
from test_esxcli import ESXiEsxcliCommand
from test_sh import ESXiShCommand

from test_fs_cmd import *

# Class_Command
COMMAND_MAP = {
    "cat": ESXiCatCommand,
    "ls" : ESXiLsCommand,
    "cd" : ESXiCdCommand,
    "pwd": ESXiPwdCommand,
    "mkdir": ESXiMkdirCommand,
    "rmdir": ESXiRmdirCommand,
    "touch": ESXiTouchCommand,
    "cp": ESXiCpCommand,
    "rm": ESXiRmCommand,
    "mv": ESXiMvCommand,
    "clear": ESXiClearCommand,
    "ping": ESXiPingCommand,
    "vmdumper": ESXiVmdumperCommand,
    "vim-cmd": ESXiVimCmdCommand,
    "esxcli": ESXiEsxcliCommand,
    "sh": ESXiShCommand,
    "chmod": ESXiChmodCommand,
    "wget" : ESXiWgetCommand,
    "scp" : ESXiScpCommand
}



# Filesystem
my_fs = fs.SimpleFS(root="")

while True:
    try:
        #Input
        cwd = my_fs.getcwd()
        if cwd == my_fs.root:
            cwd = '~'
        user_input = input(f"[root@LuaGa:{os.path.basename(cwd)}] ")

        # Analyze command and arguments
        parts = shlex.split(user_input)
        if not parts:
            continue
        if parts[0].startswith("./") and not parts[0].startswith("/"):
            command = "sh"
            args = parts
        else:
            command = parts[0]
            args = parts[1:]

        
        # find class command in COMMAND_MAP
        command_class = COMMAND_MAP.get(command)
        if command_class:

        # Execute command
            command_obj = command_class(command, args, my_fs.getcwd(), my_fs)
            command_obj.run()

        #Output and Error
            print(command_obj.get_output())
            if command_obj.get_error():
                print(command_obj.get_error())
        else:
            print(f'Command not found: {command}')

    except KeyboardInterrupt:
        print("\nExiting shell.")
        break
