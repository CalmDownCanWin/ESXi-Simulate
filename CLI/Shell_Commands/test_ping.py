import ESXi_fs as fs
import ESXi_command as cmd
import random
import time
import re

class ESXiPingCommand(cmd.SimpleCommand):
    """
    /bin/ping
    """
    def __init__(self, cmd, args, cwd, fs, environ=None, stdin=None):
        super().__init__(cmd, args, cwd, fs, environ, stdin)
        self.host = None
        self.count = 4  # packet default
        self.interval = 1  # default packet time
        self.timeout = None
        self.packet_size = 56  # packet size default
        self.ttl = 64  # TTL default

    def run(self):
        if "-h" in self.args or "--help" in self.args:
            self.show_help()
            return

        self.parse_args()
        if not self.host:
            self.stderr = "ping: missing host"
            self.returncode = 1
            return

        # Emulate Ping
        self.write_output(f"PING {self.host} ({self.host}): {self.packet_size} data bytes\r\n", flush=True)
        for i in range(self.count):
            if self.timeout and time.time() - self.start_time > self.timeout:
                self.write_output(f"ping: timeout - No reply from {self.host}\r\n", flush=True)
                break
            delay = random.uniform(0.1, 0.5) * self.interval
            time.sleep(delay)
            self.write_output(f"64 bytes from {self.host}: icmp_seq={i + 1} ttl={self.ttl} time={delay * 1000:.1f} ms\r\n",end='', flush=True)

        self.write_output(f"\n--- {self.host} ping statistics ---\r\n",end='',flush=True)
        self.write_output(f"{self.count} packets transmitted, {self.count} received, 0% packet loss, time {(self.count - 1) * self.interval:.0f}ms\r\n",end='',flush=True)


    def parse_args(self):
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
                self.host = arg



    def show_help(self):
        self.write_output(
            """ping [args] [host]\r\n
   args:\r\n
      -4               use IPv4 (default)\r\n
      -6               use IPv6\r\n
      -c <count>       set packet count\r\n
      -d               set DF bit (IPv4) or disable fragmentation (IPv6)\r\n
      -D               vmkernel TCP stack debug mode\r\n
      -i <interval>    set interval (secs)\r\n
      -I <interface>   outgoing interface - for IPv6 scope or IPv4\r\n
                       bypasses routing lookup\r\n
      -N <next_hop>    set IP*_NEXTHOP - bypasses routing lookup\r\n
                       for IPv4, -I option is required\r\n
      -s <size>        set the number of ICMP data bytes to be sent.\r\n
                       The default is 56, which translates to a 64 byte\r\n
                       ICMP frame when added to the 8 byte ICMP header.\r\n
                       (Note: these sizes does not include the IP header).\r\n
      -t <ttl>         set IPv4 Time To Live or IPv6 Hop Limit\r\n
      -v               verbose\r\n
      -W <timeout>     set timeout to wait if no responses are\r\n
                       received (secs)\r\n

      -X               XML output format for esxcli framework.\r\n
      -S               The network stack instance name. If unspecified\r\n
                       the default netstack instance is used.\r\n
   NOTE: In vmkernel TCP debug mode, vmkping traverses\r\n
         VSI and pings various configured addresses.\r\n
"""
        )