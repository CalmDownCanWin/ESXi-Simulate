import socket
import threading
import paramiko
import logging
import os
import shlex
import time
import re
import uuid
import datetime
import hashlib
from collections import defaultdict

from config import SSH_PORT, VALID_USERS, SSH_BANNER, RSA_KEY_PATH, RSA_PUB_KEY_PATH, HONEYPOT_ROOT, ENTROPY_THRESHOLDS
from utils import disconnect_attacker, log_event, DisconnectException
from event_logger import attack_log, log_event, log_ssh_event
from behavior_analyzer import BehaviorAnalyzer

import ESXi_fs as fs
from test_cat import ESXiCatCommand
from test_ls import ESXiLsCommand
from test_ping import ESXiPingCommand
from test_wget import ESXiWgetCommand
from test_scp import ESXiScpCommand

from test_vmdumper import ESXiVmdumperCommand
from test_vimcmd import ESXiVimCmdCommand
from test_esxcli import ESXiEsxcliCommand
from test_sh import ESXiShCommand
from test_python import ESXiPythonCommand

from test_fs_cmd import *

# Ánh xạ tên command với class command
COMMAND_MAP = {
    "cat": ESXiCatCommand,
    "ls": ESXiLsCommand,
    "cd": ESXiCdCommand,
    "pwd": ESXiPwdCommand,
    "mkdir": ESXiMkdirCommand,
    "rmdir": ESXiRmdirCommand,
    "touch": ESXiTouchCommand,
    "cp": ESXiCpCommand,
    "rm": ESXiRmCommand,
    "mv": ESXiMvCommand,
    "clear": ESXiClearCommand,
    "ping": ESXiPingCommand,
    "vmdumper": ESXiVmdumperCommand,
    "vim-cmd": ESXiVimCmdCommand,
    "esxcli": ESXiEsxcliCommand,
    "sh": ESXiShCommand,
    "wget": ESXiWgetCommand,
    "scp": ESXiScpCommand,
    "echo": ESXiEchoCommand,
    "head": ESXiHeadCommand,
    "tail": ESXiTailCommand,
    "python": ESXiPythonCommand
}

# Cấu hình logging
logging.basicConfig(
    filename='honeypot.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Danh sách các địa chỉ IP ảo để lắng nghe
IP_ADDRESSES = [""]

# File lưu trữ các địa chỉ IP đã hiển thị khóa RSA
IP_TRACKER_FILE = 'ip_tracker.txt'

# Khởi tạo BehaviorAnalyzer
behavior_analyzer = BehaviorAnalyzer(sensitive_dirs=["/etc", "/var/log", "/vmfs/volumes"])

# Hàm để kiểm tra và lưu trữ địa chỉ IP
def check_and_store_ip(client_ip):
    if not os.path.exists(IP_TRACKER_FILE):
        open(IP_TRACKER_FILE, 'w').close()

    with open(IP_TRACKER_FILE, 'r') as file:
        tracked_ips = file.read().splitlines()

    if client_ip not in tracked_ips:
        with open(IP_TRACKER_FILE, 'a') as file:
            file.write(client_ip + '\n')
        return True
    return False

# Class để lưu trữ thông tin phiên kết nối
class SSHSession:
    def __init__(self, client_ip, username):
        self.session_id = str(uuid.uuid4())
        self.client_ip = client_ip
        self.username = username
        self.start_time = datetime.datetime.utcnow().isoformat()
        self.end_time = None
        self.commands = []
        self.accessed_files = []
        self.file_access_count = defaultdict(lambda: {"count": 0, "last_access": None, "commands": []})

    def add_command(self, command):
        self.commands.append(
            {"timestamp": datetime.datetime.utcnow().isoformat(), "command": command}
        )

    def add_accessed_file(self, filepath, action, old_hash=None, new_hash=None):
        ransomware_name = None
        if action == "modify":
            new_hash = self.calculate_file_hash(filepath)
            if old_hash != new_hash:
                ransomware_name = self.check_ransomware(new_hash)

        self.accessed_files.append(
            {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "filepath": filepath,
                "action": action,
                "old_hash": old_hash,
                "new_hash": new_hash,
                "ransomware_name": ransomware_name
            }
        )

        # Phân tích hành vi file
        event = {
            "filepath": filepath,
            "action": action,
            "old_hash": old_hash,
            "new_hash": new_hash,
        }
        self.analyze_file_behavior(event)
        
        # Cập nhật số lần truy cập file
        self.file_access_count[filepath]["count"] += 1
        self.file_access_count[filepath]["last_access"] = datetime.datetime.utcnow().isoformat()
        self.file_access_count[filepath]["commands"].extend(cmd[1] for cmd in self.commands)

    def analyze_file_behavior(self, event):
        """Phân tích hành vi file."""
        global behavior_analyzer
        is_suspicious, reason = behavior_analyzer.analyze_event(event)
        if is_suspicious:
            log_event(
                "File Monitor",
                "suspicious_activity",
                f"Suspicious file activity detected: {reason}",
                session=self,
                severity="DANGEROUS",
                additional_info={"suspicion_reason": reason}
            )
            disconnect_attacker()  # Ngắt kết nối attacker (tùy chọn)

    def close_session(self):
        """Đóng session và ghi nhận thời gian kết thúc."""
        self.end_time = datetime.datetime.utcnow().isoformat()
        log_event("SSH", "session_closed", "Session closed", session=self, severity="NORMAL")

# Dictionary để lưu trữ session
sessions = {}

# SSH Server implementation
class Server(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.event = threading.Event()
        self.client_ip = client_ip

    def check_channel_request(self, kind, chanid):
        logging.debug(f"[SSH] Channel request: {kind}") # Đã sửa: Thay log_event bằng logging.debug
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        logging.debug(f"[SSH] Authentication attempt for user: {username}") # Đã sửa: Thay log_event bằng logging.debug
        if username in VALID_USERS and VALID_USERS[username] == password:
            logging.debug(f"[SSH] Authentication successful for user: {username}") # Đã sửa: Thay log_event bằng logging.debug
            return paramiko.AUTH_SUCCESSFUL
        logging.debug(f"[SSH] Authentication failed for user: {username}") # Đã sửa: Thay log_event bằng logging.debug
        return paramiko.AUTH_FAILED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        logging.debug(f"[SSH] PTY request on channel {channel}") # Đã sửa: Thay log_event bằng logging.debug
        return True

    def check_channel_shell_request(self, channel):
        logging.debug(f"[SSH] Shell request on channel {channel}") # Đã sửa: Thay log_event bằng logging.debug
        self.event.set()
        return True

    def check_channel_exec_request(self, channel, command):
        command = str(command)
        logging.debug(f"[SSH] Command {command} executed on channel {channel}") # Đã sửa: Thay log_event bằng logging.debug
        return True

def handle_esxi_honeypot(channel, client_ip, fs_honeypot, session):
    """Shell ESXi honeypot."""
    while True:
        try:
            # Nhận input từ người dùng
            cwd = os.path.relpath(fs_honeypot.getcwd(), fs_honeypot.root)
            if cwd == '.':
               cwd = '~'
            channel.send(f"[root@LuaGa:{cwd}] ".encode())
            user_input = ""
            while True:
                data = channel.recv(1)  # Đọc từng ký tự
                if data == '\r' or data == '\n':
                    break
                elif data == b'\r':  # Kết thúc dòng khi nhận Enter
                    channel.send(b"\r")
                    break
                elif data == b'\x03':  # Xử lý Ctrl+C
                    raise KeyboardInterrupt
                elif data == b'\x7f' or data == b'\x08':   # Delete char
                    if user_input:
                        user_input = user_input[:-1]
                        channel.send(b"\b \b")
                elif data == b"\x1b":  # Escape sequence (bắt đầu bằng ESC)
                    next_byte = channel.recv(1)  # Nhận byte tiếp theo
                    if next_byte == b"[":  # Escape sequence cho arrow keys
                        direction_byte = channel.recv(1) 
                        if direction_byte in [b"A", b"B"]:  # Up Arrow hoặc Down Arrow
                            # Không làm gì cả (vô hiệu hóa arrow keys)
                            pass  
                        else:
                            # Xử lý các escape sequence khác (nếu cần)
                            channel.send(data + next_byte + direction_byte)
                    else:
                        # Xử lý các escape sequence khác (nếu cần)
                        channel.send(data + next_byte)
                elif data:
                    user_input += data.decode()
                    channel.send(data)

            user_input = user_input.strip()
            channel.send(b"\r\n")
            
            logging.debug(f"Received input: {user_input}")
         
            # Phân tích command và arguments
            parts = shlex.split(user_input)

            # Escape các ký tự đặc biệt trong arguments
            for i in range(1, len(parts)):
                parts[i] = re.escape(parts[i])

            # Gộp lại thành chuỗi lệnh
            escaped_user_input = " ".join(parts)

            if not parts:
                continue
            if parts[0].startswith("./") and not parts[0].startswith("/"):
                command = "sh"
                args = parts
            else:
                command = parts[0]
                args = parts[1:]
                
            # Ghi log command
            log_event(
                "SSH", 
                "command_executed", 
                f"Command executed: {escaped_user_input}", 
                session=session, 
                severity="NORMAL",
                additional_info={
                    "command": command,
                    "arguments": args,
                    "cwd": fs_honeypot.getcwd()
                }
            )

            # Thêm command vào session
            session.add_command(escaped_user_input)

            logging.debug(f"[DEBUG] Command received: {command}")
            # Tìm class command trong COMMAND_MAP
            command_class = COMMAND_MAP.get(command)
            logging.debug(f"[DEBUG] Command class found: {command_class}")
            if command_class:

                # Tạo instance SimpleCommand và thực thi command
                command_obj = command_class(command, args, fs_honeypot.getcwd(), fs_honeypot, session)
                logging.debug(f"[DEBUG] Command object created: {command_obj}")

                command_obj.run()

                # In output và lỗi
                logging.debug(f"Sending output: {command_obj.get_output()}")
                channel.send(command_obj.get_output().encode() + b"\r\n")
                
                logging.debug(f"Sending error: {command_obj.get_error()}")
                if command_obj.get_error():
                    channel.send(command_obj.get_error().encode() + b"\r\n")
                    
            elif command == 'exit':
                channel.send("\nBye...\r\n")
                break
            else:
                channel.send(f'Command not found: {command}\n'.encode() + b"\r")

        except Exception as e:
            logging.exception(f"[SSH] Error during command processing:")
            break

        except KeyboardInterrupt:
            channel.send("\nExiting shell....\r\n")
            break

def handle_client(client_socket, client_address):
    # Đã sửa: Sử dụng severity cho log_event
    log_event("SSH", "new_connection", f"[SSH] New connection from {client_address}", severity="INFO")
    log_ssh_event(client_address[0], None, None)  # Log the initial connection with no command

    client_ip = client_address[0]
    session = None
    chan = None  # Khởi tạo chan

    try:
        with paramiko.Transport(client_socket) as transport:
            transport.load_server_moduli()
            
            # Tải khóa RSA từ file
            try:
                rsa_key = paramiko.RSAKey(filename=RSA_KEY_PATH)
            except Exception as e:
                log_event("SSH", "rsa_key_error", f"[SSH] Error loading RSA key: {e}", severity="ERROR")
                return

            transport.add_server_key(rsa_key)

            # Kiểm tra và lưu trữ địa chỉ IP
            is_new_ip = check_and_store_ip(client_ip)

            # Hiển thị khóa RSA công khai nếu là kết nối từ địa chỉ IP mới
            if is_new_ip:
                try:
                    with open(RSA_PUB_KEY_PATH, 'r') as pub_key_file:
                        rsa_pub_key = pub_key_file.read()
                except Exception as e:
                    log_event("SSH", "rsa_key_error", f"[SSH] Error reading RSA public key: {e}", severity="ERROR")
                    return

                chan = transport.accept(20)
                if chan is None:
                    log_event("SSH", "no_channel", f"[SSH] No channel from {client_address}", severity="WARNING")
                    return

                # Gửi khóa RSA công khai
                chan.send(f"Public RSA Key: {rsa_pub_key}\r\n".encode('utf-8'))

            server = Server(client_ip=client_ip)
            try:
                transport.start_server(server=server)
            except paramiko.SSHException as e:
                log_event("SSH", "ssh_negotiation_failed", f"[SSH] SSH negotiation failed: {e}", severity="ERROR")
                return
            except EOFError:
                log_event("SSH", "client_disconnected", f"[SSH] Client disconnected prematurely: {client_address}", severity="WARNING")
                return

            chan = transport.accept(100)
            if chan is None:
                log_event("SSH", "no_channel", f"[SSH] No channel from {client_address}", severity="WARNING")
                return

            # Gửi banner giả mạo
            chan.send(SSH_BANNER + b"\r\n")

            # Fake last login
            chan.send(b"Last login: Mon Jan 1 00:00:00 2023 from 192.168.1.1\n\r")
            
            fs_honeypot = fs.SimpleFS(root= HONEYPOT_ROOT)

            # Giả sử xác thực thành công
            username = "root"  # Hoặc bất kỳ username hợp lệ nào

            # Khởi tạo SSHSession
            session = SSHSession(client_ip, username)
            sessions[client_ip] = session
            log_event("SSH", "session_started", "Session started", session=session, severity="NORMAL")

            handle_esxi_honeypot(chan, client_ip, fs_honeypot, session)

    except DisconnectException:
        log_event("SSH", "client_disconnected", f"[SSH] Client disconnected: {client_address}", severity="INFO")
        if chan:
            chan.send(b'Connection closed.\n')
            chan.close()
    except Exception as e:
        logging.exception(f"[SSH] Error handling connection from {client_address}:")
    finally:
        if session:
            session.close_session()
        client_socket.close()

def run_ssh_server(ip_address):
    """Khởi động máy chủ SSH trên một địa chỉ IP cụ thể."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip_address, SSH_PORT))
    server_socket.listen(5)
    log_event("SSH", "server_listening", f"[INFO] SSH server listening on {ip_address}:{SSH_PORT}", severity="INFO")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            log_event("SSH", "connection_accepted", f"[INFO] Accepted connection from {client_address}", severity="INFO")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
        except Exception as e:
            log_event("SSH", "connection_error", f"[SSH] Error accepting connection: {e}", severity="ERROR")

if __name__ == "__main__":
    # Khởi chạy một máy chủ SSH cho mỗi địa chỉ IP trong danh sách
    for ip in IP_ADDRESSES:
        try:
            threading.Thread(target=run_ssh_server, args=(ip,)).start()
        except KeyboardInterrupt:
            print(f"\nTerminated.....")