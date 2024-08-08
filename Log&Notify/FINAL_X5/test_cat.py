import ESXi_fs as fs
import ESXi_command as cmd
import stat
import os

class ESXiCatCommand(cmd.SimpleCommand):
    def run(self):
        if "--help" in self.args:
            self.show_help()
            return

        self.handle_redirection() # Xử lý chuyển hướng output trước

        if self.outfile:
            # Chuyển hướng output sang file
            if self.stdin:
                # Đọc input từ stdin và ghi vào file
                content = self.stdin.decode()
                self.write_output(content)
            else:
                # Yêu cầu input từ user
                #self.write_output("Enter content (Ctrl+D to finish):\n")
                while True:
                    try:
                        line = input()
                        self.write_output(line + "\n")
                    except EOFError:  # Ctrl+D
                        break
        else:
            # Không có chuyển hướng, hoạt động như cat bình thường
            if self.check_arguments(1):
                filename = self.args[0]
                try:
                    with self.fs.open(filename, "r") as f:
                        #contents = f.read()
                        for content in f:
                            self.write_output(f"{content}\r")
                except fs.FileNotFoundError:
                    self.stderr = f"cat: {filename}: No such file or directory"
                    self.returncode = 1
                except PermissionError:
                    self.stderr = f"cat: {filename}: Permission denied"
                    self.returncode = 1
            else:
                self.stderr = "cat: missing operand"
                self.returncode = 1

        self.close_outfile()


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
