import ESXi_fs as fs
import ESXi_command as cmd
import time
import re
import os
import hashlib
import random
import error_handler as er 

class ESXiWgetCommand(cmd.SimpleCommand):
    """
    /bin/wget
    """
    def __init__(self, cmd, args, cwd, fs, environ=None, stdin=None):
        super().__init__(cmd, args, cwd, fs, environ, stdin)
        self.url = None
        self.outfile = None
        self.quiet = False

    def run(self):
        if "--help" in self.args or "-h" in self.args:
            self.show_help()
            return

        self.parse_args()
        if not self.url:
            self.stderr = "wget: missing URL"
            self.returncode = 1
            return

        # Emulate Download
        self.simulate_download()

    def parse_args(self):
        for i, arg in enumerate(self.args):
            if arg == "-q" or arg == "--quiet":
                self.quiet = True
            elif arg == "-O" or arg == "--output-document":
                try:
                    self.outfile = self.args[i + 1]
                except IndexError:
                    self.stderr = "wget: missing filename after '-O'"
                    self.returncode = 1
                    return
            elif not arg.startswith("-"):
                self.url = arg
                break

    def simulate_download(self):
        # Fake contents
        fake_content = b"Got u man! What do u want?\n"
        file_size = len(fake_content)

        # create file if not 
        if not self.outfile:
            url_parts = self.url.split("/")
            filename = url_parts[-1] if url_parts[-1] else "index.html"

        # path/to/download_file
        filepath = self.fs.resolve_path(filename)

        # Start Downloading
        if not self.quiet:
            self.write_output(f"--{time.strftime('%Y-%m-%d %H:%M:%S')}--  {self.url}\r\n",end='',flush=True)
            self.write_output(f"Resolving {self.url}... done.\r\n",end='',flush=True)
            self.write_output(f"Connecting to {self.url}... connected.\r\n",end='',flush=True)
            self.write_output("HTTP request sent, awaiting response... 200 OK\r\n",end='',flush=True)
            self.write_output(f"Length: {file_size} ({sizeof_fmt(file_size)}) [text/plain]\r\n",end='',flush=True)
            self.write_output(f"Saving to: '{filename}'\r\n",end='',flush=True)

        # Process
        total_chunks = random.randint(5, 15)
        chunk_size = file_size // total_chunks
        for i in range(total_chunks):
            if not self.quiet:
                progress = (i + 1) * chunk_size
                percent = int(progress / file_size * 100)
                speed = random.randint(10, 50)  # KB/s
                
                self.write_output(
                    f"\r{percent:3d}% [{'=' * (percent // 5)}>{' ' * (20 - percent // 5)}] {progress}/{file_size} {speed}K/s\r\n",end='',flush=True
                )
            time.sleep(random.uniform(0.1, 0.5))  # Download time

        if not self.quiet:
            self.write_output(f"\r100% [{'=' * 20}] {file_size}/{file_size} {speed}K/s\r\n",end='',flush=True)
            self.write_output("\n")


        # Saved download_files
        try:
            with self.fs.open(filepath, "wb") as f:
                f.write(fake_content)

            if not self.quiet:
                self.write_output(f"'{filename}' saved [{file_size}/{file_size}]\r\n",end='',flush=True)
        except (FileNotFoundError, PermissionError):
            self.stderr = er.Wget_error(self.url)
            self.returncode = 1

    def show_help(self):
        self.write_output(
            """Usage: wget [-c|--continue] [--spider] [-q|--quiet] [-O|--output-document FILE]\r
        [--header 'header: value'] [-Y|--proxy on/off] [-P DIR]\r
        [-S|--server-response] [-U|--user-agent AGENT] URL...\r

Retrieve files via HTTP or FTP\r

        --spider        Only check URL existence: $? is 0 if exists\r
        -c              Continue retrieval of aborted transfer\r
        -q              Quiet\r
        -P DIR          Save to DIR (default .)\r
        -S              Show server response\r
        -O FILE         Save to FILE ('-' for stdout)\r
        -U STR          Use STR for User-Agent header\r
        -Y on/off       Use proxy\r
"""
        )


def sizeof_fmt(num: float) -> str:
    for x in ["bytes", "K", "M", "G", "T"]:
        if num < 1024.0:
            return f"{num:.1f}{x}"
        num /= 1024.0
    raise Exception()

