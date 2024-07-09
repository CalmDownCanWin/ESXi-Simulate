import os
import shlex
import ESXi_fs as fs

class SimpleCommand:
    def __init__(self, cmd, args, cwd, fs, environ=None, stdin=None):
        self.cmd = cmd
        self.args = args
        self.cwd = cwd
        self.fs = fs
        self.environ = environ or os.environ
        self.stdin = stdin
        self.stdout = ""
        self.stderr = ""
        self.returncode = 0
        self.outfile = None
        self.append_output = False

    def run(self):
        raise NotImplementedError
    
    def handle_redirection(self):
        if ">" in self.args:
            self.append_output = False
            redirect_index = self.args.index(">")
        elif ">>" in self.args:
            self.append_output = True
            redirect_index = self.args.index(">>")
        else:
            return

        if redirect_index == len(self.args) - 1:
            self.stderr = f"{self.cmd}: syntax error near unexpected token `newline'"
            self.returncode = 2
            return

        self.outfile = self.args[redirect_index + 1]
        self.args = self.args[:redirect_index]

    def open_outfile(self):
        if self.outfile:
            try:
                mode = "a" if self.append_output else "w"
                return self.fs.open(self.outfile, mode)
            except (fs.FileNotFoundError, PermissionError) as e:
                self.stderr = f"{self.cmd}: {self.outfile}: {e}"
                self.returncode = 1
                self.outfile = None

    def close_outfile(self):
        if self.outfile:
            self.outfile.close()

    def check_arguments(self, num_args):
        if len(self.args) != num_args:
            self.stderr = f"{self.cmd}: wrong number of arguments"
            self.returncode = 1
            return False
        return True

    def check_file_exists(self, filename):
        if not self.fs.isfile(filename):
            self.stderr = f"{self.cmd}: {filename}: No such file"
            self.returncode = 1
            return False
        return True
    
    def write_output(self, output):
        if self.outfile:
            self.outfile.write(output)
        else:
            self.stdout = output

    def handle_CTRL_C(self):
        self.stderr = "^C"
        self.returncode = 130
        self.close_outfile()

    def get_output(self):
        return self.stdout

    def get_error(self):
        return self.stderr

    def get_returncode(self):
        return self.returncode