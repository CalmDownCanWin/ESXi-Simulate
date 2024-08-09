import os
import shlex
import ESXi_fs as fs
import time
import re
import random

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
        self.log_command()

        if self.check_malicious():
            self.Notify_malicious_behavior()

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

        try:
            mode = "a" if self.append_output else "w"
            self.outfile = self.fs.open(self.outfile, mode)
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
        """Ghi output vào stdout hoặc file output."""
        if self.outfile:
            try:
                self.outfile.write(output)
            except Exception as e:
                self.stderr = f"{self.cmd}: {self.outfile}: {e}"
                self.returncode = 1
        else:
            self.stdout += output

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
    
    def log_command(self):

        timestamp = time.strftime("%Y-%m-%d %H:$M:$S")
        log_entry = f"{timestamp} - {self.cwd} $ {self.cmd} {' '.join(self.args)}\n"
        
        log_filepath = os.path.join(self.fs.root, "var/log")
        log_file = os.path.join(log_filepath, "auth.log")

        with open(log_file, " a") as f:
            f.write(log_entry)


    def check_malicious(self):
        
        MALICIOUS_COMMANDS = ["ls"]
        MALICIOUS_PATTERNS = [r"wget .*hack.*", r"curl .*evil.*"]
        full_command = f"{self.cmd} {' '.join(self.args)}"
        if full_command in MALICIOUS_COMMANDS:
            return True
        for pattern in MALICIOUS_PATTERNS:
            if re.search(pattern, full_command):
                return True
            return False
        
    def Notify_malicious_behavior(self):

        FAKE_MESSAGES = [
        "Error: Permission denied.",
        "Command not found.",
        "System error. Please contact administrator.",
        ]
        self.stderr = random.choice(FAKE_MESSAGES)
        self.returncode = 1
        
    def parse_shell_script(self, script):
        """
        Phân tích shell script để trích xuất các command esxcli.
        """
        commands = []
        for line in script.splitlines():
            if line.strip().startswith("esxcli"):
                commands.append(shlex.split(line))
        return commands
