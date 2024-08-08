import ESXi_fs as fs
import ESXi_command as cmd
import shlex
import os

from config import HONEYPOT_ROOT
from test_cat import ESXiCatCommand
from test_ls import ESXiLsCommand
from test_ping import ESXiPingCommand
from test_wget import ESXiWgetCommand
from test_scp import ESXiScpCommand

from test_vmdumper import ESXiVmdumperCommand
from test_vimcmd import ESXiVimCmdCommand
from test_esxcli import ESXiEsxcliCommand
from test_sh import ESXiShCommand

from test_fs_cmd import *

# Ánh xạ tên command với class command
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
    "wget" : ESXiWgetCommand,
    "scp" : ESXiScpCommand
}



# Khởi tạo hệ thống file
my_fs = fs.SimpleFS(root=HONEYPOT_ROOT)

while True:
    try:
        # Nhận input từ người dùng
        cwd = my_fs.getcwd()
        if cwd == my_fs.root:
            cwd = '~'
        user_input = input(f"[root@LuaGa:{os.path.basename(cwd)}] ")

        # Phân tích command và arguments
        parts = shlex.split(user_input)
        if not parts:
            continue
        if parts[0].startswith("./") and not parts[0].startswith("/"):
            command = "sh"
            args = parts
        else:
            command = parts[0]
            args = parts[1:]

        
        # Tìm class command trong COMMAND_MAP
        command_class = COMMAND_MAP.get(command)
        if command_class:

        # Tạo instance SimpleCommand và thực thi command
            command_obj = command_class(command, args, my_fs.getcwd(), my_fs)
            command_obj.run()

        # In output và lỗi
            print(command_obj.get_output())
            if command_obj.get_error():
                print(command_obj.get_error())
        else:
            print(f'Command not found: {command}')

    except KeyboardInterrupt:
        print("\nExiting shell.")
        break
