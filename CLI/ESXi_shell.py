import ESXi_fs as fs
import ESXi_command as cmd
import shlex
import os

from test_cat import ESXiCatCommand
from test_ls import ESXiLsCommand
from test_ping import ESXiPingCommand

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
    "ping": ESXiPingCommand
}



# Khởi tạo hệ thống file
my_fs = fs.SimpleFS(root="")

while True:
    try:
        # Nhận input từ người dùng
        cwd = my_fs.getcwd()
        if cwd == my_fs.root:
            cwd = '~'
        user_input = input(f"[root@hostname:{os.path.basename(cwd)}] ")

        # Phân tích command và arguments
        parts = shlex.split(user_input)
        if not parts:
            continue
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