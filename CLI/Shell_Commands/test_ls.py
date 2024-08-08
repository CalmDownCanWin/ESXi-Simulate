import ESXi_fs as fs
from ESXi_command import SimpleCommand as cmd
import os
import stat
import time

class ESXiLsCommand(cmd):
    """
    /bin/ls
    """
    def run(self):
        if "--help" in self.args :
            self.show_help()
            return

        # options
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

        # arguments
        paths = self.args[:]
        for i, arg in enumerate(paths):
            if arg.startswith("-"):
                paths.pop(i)
        if not paths:
            paths = ["."]

        # list
        for path in paths:
            self.list_directory_contents(path)

    def list_directory_contents(self, path):
        path = self.fs.resolve_path(path)
        if path in ["/dev", "/etc", "/bin", "/var", "/lib", "/usr"]:
            path = os.path.join(self.fs.root, path[1:])
        print(path)
        if not self.fs.exists(path):
            self.stderr += f"ls: cannot access '{os.path.basename(path)}': No such file or directory\n"
            self.returncode = 1
            return

        if self.list_dirs:
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

                files.sort()
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
        if self.one_column:
            for file in files:
                self.write_output(f"{file}\n")
        else:
            self.write_output("  ".join(files) + "\n")

    def print_long_listing(self, path, files):
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
        for unit in ['B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if size < 1024.0:
                return f"{size:.1f}{unit}"
            size /= 1024.0
        return f"{size:.1f}Y"

    def show_help(self):
        print(
            """Usage: ls [-1AaCxdLHRFplinshrSXvctu] [-w WIDTH] [FILE]...\r

List directory contents\r

        -1      One column output\r
        -a      Include entries which start with .\r
        -A      Like -a, but exclude . and ..\r
        -x      List by lines\r
        -d      List directory entries instead of contents\r
        -L      Follow symlinks\r
        -H      Follow symlinks on command line\r
        -R      Recurse\r
        -p      Append / to dir entries\r
        -F      Append indicator (one of */=@|) to entries\r
        -l      Long listing format\r
        -i      List inode numbers\r
        -n      List numeric UIDs and GIDs instead of names\r
        -s      List allocated blocks\r
        -lc     List ctime\r
        -lu     List atime\r
        --full-time     List full date and time\r
        -h      Human readable sizes (1K 243M 2G)\r
        --group-directories-first\r
        -S      Sort by size\r
        -X      Sort by extension\r
        -v      Sort by version\r
        -t      Sort by mtime\r
        -tc     Sort by ctime\r
        -tu     Sort by atime\r
        -r      Reverse sort order\r
        -w N    Format N columns wide\r
        --color[={always,never,auto}]   Control coloring\r
"""
        )
