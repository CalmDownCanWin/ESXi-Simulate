import ESXi_fs as fs
import ESXi_command as cmd
import error_handler as er

import re
import os
import time
import random

class ESXiScpCommand(cmd.SimpleCommand):
    """
    /bin/scp
    """

    def __init__(self, cmd, args, cwd, fs, environ=None, stdin=None):
        super().__init__(cmd, args, cwd, fs, environ, stdin)

    def run(self):
        if "-h" in self.args or "--help" in self.args:
            self.show_help()
            return

        if len(self.args) < 2:
            self.stderr = "scp: missing file operand"
            self.returncode = 1
            return

        source = self.args[:-1]
        target = self.args[-1]

        # Emualte copy
        self.write_output("Copying files...\r\n")
        for src in source:
            self.simulate_copy(src, target)

    def simulate_copy(self, source, target):

        #fake_content = b"Error!\n"

        # Create fake filename
        filename = os.path.basename(source)

        # Save files
        # filepath = self.fs.resolve_path(filename)
        # with open(filepath, "wb") as f:
        #     f.write(fake_content)

        # Process
        file_size = random.randint(1024, 1024)
        for i in range(0, 101, 5):
            progress = int(i * file_size / 100)
            bar = "=" * int(i / 5) + " " * (20 - int(i / 5))
            speed = random.randint(100, 5000)
            self.write_output(f"\r{source} [{bar}] {i}% {progress}KB/{file_size}KB {speed}KB/s\r\n", end="", flush=True)
            time.sleep(0.1)

        self.write_output(f"\r{source} [{'=' * 20}] 100% {file_size}KB/{file_size}KB {speed}KB/s   00:00    \r\n", end="", flush=True)
        #self.write_output(f"'{filename}' -> '{target}'\r\n")

        self.write_output("\n")                     
        time.sleep(3)

        self.stderr = er.Scp_error(filename)
        self.returncode = 1

    def show_help(self):
        self.write_output(
            """usage: scp [-346BCpqrTv] [-c cipher] [-F ssh_config] [-i identity_file]\r
            [-J destination] [-l limit] [-o ssh_option] [-P port]\r
            [-S program] source ... target\r
"""
        )