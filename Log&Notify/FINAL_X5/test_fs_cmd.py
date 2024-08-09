import ESXi_fs as fs
import ESXi_command as cmd
import os
import re
import time

class FSCmd(cmd.SimpleCommand):
    """
    Lớp cơ sở cho các command liên quan đến filesystem.
    """

    def check_file_exists(self, filename):
        """
        Kiểm tra file có tồn tại không.
        """
        if not self.fs.exists(filename):
            self.stderr = f"{self.cmd}: {filename}: No such file or directory"
            self.returncode = 1
            return False
        return True

    def check_dir_exists(self, dirname):
        """
        Kiểm tra thư mục có tồn tại không.
        """
        if not self.fs.isdir(dirname):
            self.stderr = f"{self.cmd}: {dirname}: Not a directory"
            self.returncode = 1
            return False
        return True

class ESXiGrepCommand(FSCmd):
    """
    Lệnh grep.
    """
    def run(self):
        if self.check_arguments(2):
            pattern = self.args[0]
            filename = self.args[1]
            if self.check_file_exists(filename):
                try:
                    with self.fs.open(filename, "r") as f:
                        for line in f:
                            if re.search(pattern, line):
                                self.write_output(line)
                except Exception as e:
                    self.stderr = f"grep: {filename}: {e}"
                    self.returncode = 1

class ESXiTailCommand(FSCmd):
    """
    Lệnh tail.
    """
    def run(self):
        n = 10  # Số dòng mặc định
        if "-n" in self.args:
            try:
                n = int(self.args[self.args.index("-n") + 1])
            except (IndexError, ValueError):
                self.stderr = "tail: invalid number of lines"
                self.returncode = 1
                return

        if self.check_arguments(1):
            filename = self.args[0]
            if self.check_file_exists(filename):
                try:
                    with self.fs.open(filename, "r") as f:
                        lines = f.readlines()
                        self.write_output("".join(lines[-n:]))
                except Exception as e:
                    self.stderr = f"tail: {filename}: {e}"
                    self.returncode = 1

class ESXiHeadCommand(FSCmd):
    """
    Lệnh head.
    """
    def run(self):
        n = 10  # Số dòng mặc định
        if "-n" in self.args:
            try:
                n = int(self.args[self.args.index("-n") + 1])
            except (IndexError, ValueError):
                self.stderr = "head: invalid number of lines"
                self.returncode = 1
                return

        if self.check_arguments(1):
            filename = self.args[0]
            if self.check_file_exists(filename):
                try:
                    with self.fs.open(filename, "r") as f:
                        lines = f.readlines()
                        self.write_output("".join(lines[:n]))
                except Exception as e:
                    self.stderr = f"head: {filename}: {e}"
                    self.returncode = 1

class ESXiCdCommand(FSCmd):
    """
    Lệnh cd.
    """
    def run(self):
        if self.check_arguments(1):
            path = self.args[0]

            if path == '~':
                path = self.fs.root
            elif path.startswith("/"):
                path = os.path.join(self.fs.root, path[1:])

            try:
                self.fs.chdir(path)
                self.cwd = self.fs.getcwd()
            except fs.FileNotFoundError:
                self.stderr = f"cd: can't cd to {path}: No such file or directory"
                self.returncode = 1

class ESXiTouchCommand(FSCmd):
    """
    Lệnh touch.
    """
    def run(self):
        for filename in self.args:
            try:
                with self.fs.open(filename, 'a'):
                    pass
            except (fs.FileNotFoundError, PermissionError) as e:
                self.stderr += f"touch: {filename}: {e}\n"
                self.returncode = 1

class ESXiRmCommand(FSCmd):
    """
    Lệnh rm.
    """
    def run(self):
        for filename in self.args:
            if self.check_file_exists(filename):
                try:
                    if not self.fs.isdir(filename):
                        choice = input(f"rm: remove '{filename}'? ")
                        if choice == 'y':
                            self.fs.remove(filename)
                        else:
                            continue
                    else:
                        self.stderr += f"rm: '{filename}' is a directory\n"
                except  (PermissionError, OSError) as e:
                    self.stderr += f"rm: {filename}: {e}\n"
                    self.returncode = 1

class ESXiMkdirCommand(FSCmd):
    """
    Lệnh mkdir.
    """
    def run(self):
        for dirname in self.args:
            try:
                self.fs.mkdir(dirname)
            except (fs.FileNotFoundError, PermissionError, OSError) as e:
                self.stderr += f"mkdir: {dirname}: {e}\n"
                self.returncode = 1

class ESXiRmdirCommand(FSCmd):
    """
    Lệnh rmdir.
    """
    def run(self):
        for dirname in self.args:
            if self.check_file_exists(dirname):
                try:
                    if not self.fs.listdir(dirname):
                        self.fs.rmdir(dirname)
                    else:
                        self.stderr += f"rmdir: '{dirname}' : Directory not empty\n"
                except (PermissionError, OSError) as e:
                    self.stderr += f"rmdir: {dirname}: {e}\n"
                    self.returncode = 1

class ESXiCpCommand(FSCmd):
    """
    Lệnh cp.
    """
    def run(self):
        if self.check_arguments(2):
            source = self.args[0]
            destination = self.args[1]
            if destination == '.':
                destination = os.path.join(".", os.path.basename(source))
            
            try:
                self.fs.copy(source, destination)
            except (fs.FileNotFoundError, PermissionError, OSError) as e:
                self.stderr = f"cp: {e}"
                self.returncode = 1

class ESXiMvCommand(FSCmd):
    """
    Lệnh mv.
    """
    def run(self):
        if self.check_arguments(2):
            source = self.args[0]
            destination = self.args[1]
            try:
                if self.fs.isdir(destination):
                    # Di chuyển source vào destination directory
                    basename = os.path.basename(source)
                    new_path = os.path.join(destination, basename)
                    self.fs.rename(source, new_path)
                else:
                    # Đổi tên source thành destination
                    self.fs.rename(source, destination)
            except (fs.FileNotFoundError, PermissionError, OSError) as e:
                self.stderr = f"mv: {e}"
                self.returncode = 1

class ESXiPwdCommand(FSCmd):
    """
    Lệnh pwd.
    """
    def run(self):
        relative_path = os.path.relpath(self.cwd, self.fs.root)
        if relative_path == '.':
            relative_path = '/'
        self.stdout = relative_path

class ESXiClearCommand(FSCmd):
    """
    Lệnh clear mô phỏng cho honeypot ESXi.
    """
    def run(self):
        self.stdout = "\033c" 

class ESXiEchoCommand(FSCmd):
    """
    Command "echo" for ESXi honeypot
    """

    def run(self):
        self.handle_redirection()

        output = " ".join(self.args)
        self.write_output(output + '\n')

        self.close_outfile()

# Thêm các lệnh khác vào đây...

