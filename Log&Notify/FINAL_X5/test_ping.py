import ESXi_fs as fs
import ESXi_command as cmd
import random
import time
import re

class ESXiPingCommand(cmd.SimpleCommand):
    """
    Lệnh ping mô phỏng cho honeypot ESXi.
    """
    def __init__(self, cmd, args, cwd, fs, environ=None, stdin=None):
        super().__init__(cmd, args, cwd, fs, environ, stdin)
        self.host = None
        self.count = 4  # Số lượng packet mặc định
        self.interval = 1  # Khoảng thời gian giữa các packet mặc định
        self.timeout = None
        self.packet_size = 56  # Kích thước packet mặc định
        self.ttl = 64  # TTL mặc định

    def run(self):
        if "-h" in self.args or "--help" in self.args:
            self.show_help()
            return

        self.parse_args()
        if not self.host:
            self.stderr = "ping: missing host"
            self.returncode = 1
            return

        # Mô phỏng ping
        print(f"PING {self.host} ({self.host}): {self.packet_size} data bytes\n")
        for i in range(self.count):
            if self.timeout and time.time() - self.start_time > self.timeout:
                print(f"ping: timeout - No reply from {self.host}\n")
                break
            delay = random.uniform(0.1, 0.5) * self.interval
            time.sleep(delay)
            print(f"64 bytes from {self.host}: icmp_seq={i + 1} ttl={self.ttl} time={delay * 1000:.1f} ms\n")

        print(f"\n--- {self.host} ping statistics ---\n")
        print(f"{self.count} packets transmitted, {self.count} received, 0% packet loss, time {(self.count - 1) * self.interval:.0f}ms\n")

    def parse_args(self):
        """
        Phân tích arguments của lệnh ping.
        """
        for i, arg in enumerate(self.args):
            if arg == "-c":
                try:
                    self.count = int(self.args[i + 1])
                except (IndexError, ValueError):
                    self.stderr = "ping: bad number of packets to transmit."
                    self.returncode = 1
                    return
            elif arg == "-i":
                try:
                    self.interval = float(self.args[i + 1])
                except (IndexError, ValueError):
                    self.stderr = "ping: bad interval value."
                    self.returncode = 1
                    return
            elif arg == "-W":
                try:
                    self.timeout = float(self.args[i + 1])
                    self.start_time = time.time()
                except (IndexError, ValueError):
                    self.stderr = "ping: bad timeout value."
                    self.returncode = 1
                    return
            elif arg == "-s":
                try:
                    self.packet_size = int(self.args[i + 1])
                except (IndexError, ValueError):
                    self.stderr = "ping: bad packet size value."
                    self.returncode = 1
                    return
            elif arg == "-t":
                try:
                    self.ttl = int(self.args[i + 1])
                except (IndexError, ValueError):
                    self.stderr = "ping: bad ttl value."
                    self.returncode = 1
                    return
            elif not arg.startswith("-"):
                # Giả sử argument cuối cùng là host
                self.host = arg

    def show_help(self):
        """
        Hiển thị thông tin trợ giúp.
        """
        self.write_output(
            """ping [args] [host]
   args:
      -4               use IPv4 (default)
      -6               use IPv6
      -c <count>       set packet count
      -d               set DF bit (IPv4) or disable fragmentation (IPv6)
      -D               vmkernel TCP stack debug mode
      -i <interval>    set interval (secs)
      -I <interface>   outgoing interface - for IPv6 scope or IPv4
                       bypasses routing lookup
      -N <next_hop>    set IP*_NEXTHOP - bypasses routing lookup
                       for IPv4, -I option is required
      -s <size>        set the number of ICMP data bytes to be sent.
                       The default is 56, which translates to a 64 byte
                       ICMP frame when added to the 8 byte ICMP header.
                       (Note: these sizes does not include the IP header).
      -t <ttl>         set IPv4 Time To Live or IPv6 Hop Limit
      -v               verbose
      -W <timeout>     set timeout to wait if no responses are
                       received (secs)

      -X               XML output format for esxcli framework.
      -S               The network stack instance name. If unspecified
                       the default netstack instance is used.
   NOTE: In vmkernel TCP debug mode, vmkping traverses
         VSI and pings various configured addresses.
"""
        )