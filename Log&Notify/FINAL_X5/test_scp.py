import ESXi_fs as fs
import ESXi_command as cmd
import re
import hashlib
import os
import time
import random

class ESXiScpCommand(cmd.SimpleCommand):
    """
    Lệnh scp mô phỏng cho honeypot ESXi.
    """

    def __init__(self, cmd, args, cwd, fs, environ=None, stdin=None):
        super().__init__(cmd, args, cwd, fs, environ, stdin)
        # self.download_path = "/path/to/your/esxi_download_path"

    def run(self):
        if "-h" in self.args or "--help" in self.args:
            self.show_help()
            return

        if len(self.args) < 2:
            self.stderr = "scp: missing file operand"
            self.returncode = 1
            return

        # Lấy source và target
        source = self.args[:-1]
        target = self.args[-1]

        # Mô phỏng quá trình copy
        print("Copying files...\n")
        for src in source:
            self.simulate_copy(src, target)

    def simulate_copy(self, source, target):
        """
        Mô phỏng quá trình copy file.
        """
        # Tạo nội dung giả lập cho file
        fake_content = b"This is a fake file created by ESXi honeypot.\n"

        # Tạo tên file giả lập
        filename = os.path.basename(source)
        # timestamp = time.strftime("%Y%m%d-%H%M%S")
        # fake_filename = f"{timestamp}_{filename}"

        # Lưu file giả lập 
        # filepath = os.path.join(self.download_path, fake_filename)
        filepath = self.fs.resolve_path(filename)
        with open(filepath, "wb") as f:
            f.write(fake_content)

        # Tính toán hash SHA256 của file
        #shasum = hashlib.sha256(fake_content).hexdigest()

        # In thông báo giả mạo
        file_size = len(fake_content)
        for i in range(0, 101, 5):
            progress = int(i * file_size / 100)
            bar = "=" * int(i / 5) + " " * (20 - int(i / 5))
            speed = random.randint(100, 5000)
            print(f"\r{source} [{bar}] {i}% {progress}KB/{file_size}KB {speed}KB/s", end="")
            time.sleep(0.1)

        print(f"\r{source} [{'=' * 20}] 100% {file_size}KB/{file_size}KB {speed}KB/s   00:00    \n")
        print(f"'{filename}' -> '{target}'\n")

    def show_help(self):
        """
        Hiển thị thông tin trợ giúp.
        """
        print(
            """usage: scp [-346BCpqrTv] [-c cipher] [-F ssh_config] [-i identity_file]
            [-J destination] [-l limit] [-o ssh_option] [-P port]
            [-S program] source ... target
"""
        )