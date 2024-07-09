import ESXi_fs as fs
import ESXi_command as cmd
import stat
import os

class ESXiCatCommand(cmd.SimpleCommand):
    def run(self):
        if "--help" in self.args:
            self.show_help()
            return

        if len(self.args) >= 1:
            for filename in self.args:
                self.process_file(filename)
        elif self.stdin:
            self.stdout = self.stdin.decode()
        else:
            self.stderr = "cat: missing operand"
            self.returncode = 1

    def show_help(self):
        self.stdout = """Usage: cat [-nbvteA] [FILE]...

Print FILEs to stdout

        -n      Number output lines
        -b      Number nonempty lines
        -v      Show nonprinting characters as ^x or M-x
        -t      ...and tabs as ^I
        -e      ...and end lines with $
        -A      Same as -vte
"""

    def process_file(self, filename):
        try:
            path = self.fs.resolve_path(filename)
            mode = os.stat(path).st_mode

            if stat.S_ISDIR(mode):
                self.stderr += f"cat: {filename}: Is a directory\n"
                self.returncode = 1
            elif stat.S_ISREG(mode):
                with self.fs.open(filename, "r") as f:
                    if mode & stat.S_IXUSR:
                        # File thực thi: output giả lập
                        self.stdout += "ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=..., not stripped\n"
                    else:
                        self.stdout += f.read()
            else:
                self.stderr += f"cat: {filename}: Is not a regular file\n"
                self.returncode = 1

        except FileNotFoundError:
            self.stderr += f"cat: {filename}: No such file or directory\n"
            self.returncode = 1