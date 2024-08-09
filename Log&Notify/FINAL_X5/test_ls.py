import ESXi_fs as fs
from ESXi_command import SimpleCommand as cmd
import os
import stat
import time

class ESXiLsCommand(cmd):
    """
    Lệnh ls.
    """
    def run(self):
        if "--help" in self.args :
            self.show_help()
            return

        # Xử lý options
        self.one_column = False
        self.show_hidden = False
        self.show_all = False
        self.list_dirs = False
        self.long_listing = False
        self.recursive = False
        self.human_readable = False
        self.options = set()
        for opt in self.args:
            if opt.startswith('-'):
                self.options.update(list(opt[1:]))
            elif opt == "-1":
                self.one_column = True
            elif opt == "-d":
                self.list_dirs = True
            elif opt == "-R":
                self.recursive = True
            elif opt == "-h":
                self.human_readable = True

        # Xử lý arguments
        paths = self.args[:]
        for i, arg in enumerate(paths):
            if arg.startswith("-"):
                paths.pop(i)
        if not paths:
            paths = ["."]

        # Liệt kê nội dung thư mục
        for path in paths:
            self.list_directory_contents(path)

    def list_directory_contents(self, path):
        """
        Liệt kê nội dung của một thư mục.
        """
        path = self.fs.resolve_path(path)
        if not self.fs.exists(path):
            self.stderr += f"ls: cannot access '{path}': No such file or directory\n"
            self.returncode = 1
            return

        if self.list_dirs:
            # Chỉ liệt kê thư mục
            print(path + "\n")
        else:
            try:
                files = self.fs.listdir(path)

                if "a" in self.options:
                    self.show_hidden = True 
                if "A" in self.options:
                    self.show_all = True
            
                if not self.show_hidden and not self.show_all:
                    files = [f for f in files if not f.startswith(".")]
                if self.show_all:
                    files = [f for f in files if not (f.startswith(".") and len(f) <= 2)]

                if "l" in self.options:
                    self.print_long_listing(path, files)
                else:
                    self.print_short_listing(files)

                if self.recursive:
                    for file in files:
                        if self.fs.isdir(os.path.join(path, file)):
                            print(f"\n{os.path.join(path, file)}:\n")
                            self.list_directory_contents(os.path.join(path, file))

            except FileNotFoundError:
                self.stderr += f"ls: cannot access '{path}': No such file or directory\n"
                self.returncode = 1
            except PermissionError:
                self.stderr += f"ls: cannot open directory '{path}': Permission denied\n"
                self.returncode = 1

    def print_short_listing(self, files):
        """
        In danh sách file ngắn gọn.
        """
        if self.one_column:
            for file in files:
                self.write_output(f"{file}\n")
        else:
            self.write_output("  ".join(files) + "\n")

    def print_long_listing(self, path, files):
        """
        In danh sách file chi tiết.
        """
        for file in files:
            filepath = os.path.join(path, file)
            stat_info = os.stat(filepath)
            mode = stat.filemode(stat_info.st_mode)
            nlink = stat_info.st_nlink
            uid = stat_info.st_uid
            gid = stat_info.st_gid
            size = stat_info.st_size
            mtime = time.strftime("%b %d %H:%M", time.localtime(stat_info.st_mtime))
            if self.human_readable:
                size = self.human_readable_size(size)
            self.write_output(f"{mode} {nlink} {uid} {gid} {size:>8} {mtime} {file}\r\n")

    def human_readable_size(self, size):
        """
        Chuyển đổi kích thước file sang dạng human-readable.
        """
        for unit in ['B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if size < 1024.0:
                return f"{size:.1f}{unit}"
            size /= 1024.0
        return f"{size:.1f}Y"

    def show_help(self):
        """
        Hiển thị thông tin trợ giúp.
        """
        print(
            """Usage: ls [-1AaCxdLHRFplinshrSXvctu] [-w WIDTH] [FILE]...

List directory contents

        -1      One column output
        -a      Include entries which start with .
        -A      Like -a, but exclude . and ..
        -x      List by lines
        -d      List directory entries instead of contents
        -L      Follow symlinks
        -H      Follow symlinks on command line
        -R      Recurse
        -p      Append / to dir entries
        -F      Append indicator (one of */=@|) to entries
        -l      Long listing format
        -i      List inode numbers
        -n      List numeric UIDs and GIDs instead of names
        -s      List allocated blocks
        -lc     List ctime
        -lu     List atime
        --full-time     List full date and time
        -h      Human readable sizes (1K 243M 2G)
        --group-directories-first
        -S      Sort by size
        -X      Sort by extension
        -v      Sort by version
        -t      Sort by mtime
        -tc     Sort by ctime
        -tu     Sort by atime
        -r      Reverse sort order
        -w N    Format N columns wide
        --color[={always,never,auto}]   Control coloring
"""
        )
