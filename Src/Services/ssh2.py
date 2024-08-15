import socket
import threading
import paramiko
import logging
import os
import shlex
import time
import random
import argparse

from datetime import datetime


from Settings.config import SSH_PORT, VALID_USERS, SERVER_BANNER, RSA_KEY_PATH, RSA_PUB_KEY_PATH, LOG_ROOT
from Settings.utils import send_message_to_soc, log_event, DisconnectException
from Log.Log_to_Splunk import log_command, log_recon, log_login

from Shell_Commands import ESXi_fs as fs
from Shell_Commands.test_cat import ESXiCatCommand
from Shell_Commands.test_ls import ESXiLsCommand
from Shell_Commands.test_ping import ESXiPingCommand
from Shell_Commands.test_chmod import ESXiChmodCommand 
from Shell_Commands.test_wget import ESXiWgetCommand
from Shell_Commands.test_scp import ESXiScpCommand
from Shell_Commands.test_env import ESXiEnvCommand
from Shell_Commands.test_which import ESXiWhichCommand
from Shell_Commands.test_uname import ESXiUnameCommand

from Shell_Commands.test_vmdumper import ESXiVmdumperCommand
from Shell_Commands.test_vimcmd import ESXiVimCmdCommand
from Shell_Commands.test_esxcli import ESXiEsxcliCommand
from Shell_Commands.test_sh import ESXiShCommand
from Shell_Commands.test_python import ESXiPythonCommand

from Shell_Commands.test_fs_cmd import *

# Class_Command
COMMAND_MAP = {
    "cat": ESXiCatCommand,
    "ls" : ESXiLsCommand,
    "cd" : ESXiCdCommand,
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
    "chmod": ESXiChmodCommand,
    "wget" : ESXiWgetCommand,
    "scp" : ESXiScpCommand, 
    "echo" : ESXiEchoCommand,
    "head" : ESXiHeadCommand,
    "tail" : ESXiTailCommand,
    "python": ESXiPythonCommand,
    "env": ESXiEnvCommand,
    "which": ESXiWhichCommand,
    "uname": ESXiUnameCommand   
}

# Logging
logging.basicConfig(
    filename=os.path.join(LOG_ROOT, 'honeypot.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# RSA_key for IP
IP_TRACKER_FILE = os.path.join(LOG_ROOT, 'ip_tracker.txt')

# Check and store IP
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



# SSH Server implementation
class Server(paramiko.ServerInterface):
    def __init__(self,client_ip):
        self.event = threading.Event()
        self.client_ip = client_ip

    def check_channel_request(self, kind, chanid):
        log_event(f"[SSH] Channel request: {kind}")
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        log_event(f"[SSH] Authentication attempt for user: {username}")
        if username in VALID_USERS and VALID_USERS[username] == password:
            log_event(f"[SSH] Authentication successful for user: {username}")
            log_login(
                client_ip = self.client_ip,
                username = username,
                password = password,
                status = "Successfully!"
            )
            send_message_to_soc(f"[SSH] Attempts with {username}:{password} - Successfully")
            return paramiko.AUTH_SUCCESSFUL
        log_event(f"[SSH] Authentication failed for user: {username}")
        log_login(
            client_ip = self.client_ip,
            username = username,
            password = password,
            status = "Failed!"
        )
        send_message_to_soc(f"[SSH] Attempts with {username}:{password} - Failed!")
        return paramiko.AUTH_FAILED

    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        log_event(f"[SSH] PTY request on channel {channel}")
        return True # PTY

    def check_channel_shell_request(self, channel):
        log_event(f"[SSH] Shell request on channel {channel}")
        self.event.set()
        return True # shell
    
    def check_channel_exec_request(self, channel, command):
        command = str(command)
        log_event(f"[SSH] Command {command} executed on channel {channel}")
        return True


def handle_esxi_honeypot(channel, client_ip, fs_honeypot):
    """shell ESXi honeypot."""
    waiting_for_input = False
    python_input = False
    while True:
        try:
            # Start Shell
            cwd = os.path.relpath(fs_honeypot.getcwd(), fs_honeypot.root)
            if cwd == '.' and not waiting_for_input:
                cwd = '~'
                channel.send(f"[root@LuaGa:{cwd}] ".encode())
            else:
                channel.send(f"[root@LuaGa:/{cwd}] ".encode())
            user_input = ""
            while True:
                data = channel.recv(1)  # Input 
                if data == '\r' or data == '\n':
                    break
                elif data == b'\r':  # Enter
                    channel.send(b"\r")
                    break
                elif data == b'\x03':  # Ctrl+C
                    user_input = ""  
                    channel.send(f"^C".encode()) 
                    break
                elif data == b'\x7f' or data == b'\x08':   # Delete
                    if user_input:
                        user_input = user_input[:-1]
                        channel.send(b"\b \b")
                elif data == b"\x1b":  
                    next_byte = channel.recv(1) 
                    if next_byte == b"[":
                        direction_byte = channel.recv(1) 
                        if direction_byte in [b"A", b"B"]: 
                            pass  
                        else:   
                            channel.send(data + next_byte + direction_byte)
                    else:
                        channel.send(data + next_byte)
                elif data:
                    user_input += data.decode()
                    channel.send(data)

            user_input = user_input.strip()
            channel.send(b"\r\n")
            
            logging.debug(f"Received input: {user_input}")

             # --- Handle_redirection ---
            redirect_output = None
            if " > " in user_input:
                user_input, redirect_output = user_input.split(" > ", 1)
                append_output = False
            elif " >> " in user_input:
                user_input, redirect_output = user_input.split(" >> ", 1)
                append_output = True
         
            # Analyze command and arguments
            parts = shlex.split(user_input)
            if not parts:
                continue
            if parts[0].startswith("./") and not parts[0].startswith("/"):
                command = "sh"
                args = parts
            else:
                command = parts[0]
                args = parts[1:]
                
            # log to .json
            log_command(
                commands=command,
                arguments=args,
                cwd=fs_honeypot.getcwd(),
                client_ip=client_ip,
            )
            logging.debug(f"[DEBUG] Command received: {command}")
            send_message_to_soc(f"[Filesystem] Action in '{os.path.relpath(fs_honeypot.getcwd(), fs_honeypot.root)}', filesystem_path: '{fs_honeypot.getcwd()}' ")
            send_message_to_soc(f"[Command executed] Command '{command}' used with arguments '{args}'")
            # Find class_command trong COMMAND_MAP
            command_class = COMMAND_MAP.get(command)
            logging.debug(f"[DEBUG] Command class found: {command_class}")
            if command_class:
            
            # Open file output
                if redirect_output:
                    try:
                        mode = "a" if append_output else "w"
                        outfile = fs_honeypot.open(redirect_output, mode)
                    except (fs.FileNotFoundError, PermissionError) as e:
                        channel.send(f"{command}: {redirect_output}: {e}\n".encode())
                        continue
                else:
                    outfile = None
            
            # if "cat" and handle_redirection
                if command == "cat" and outfile:
                    waiting_for_input = True

            # Executing command
                command_obj = command_class(command, args, fs_honeypot.getcwd(), fs_honeypot)
                logging.debug(f"[DEBUG] Command object created: {command_obj}")
                
                #command_obj.outfile = outfile  
                command_obj.chan = channel 
            
                command_obj.run()

                if command == "cat" and outfile:
                    while True:
                        data = channel.recv(1)
                        if data == b"\x04":  # Ctrl+D
                            outfile.close()
                            channel.send(b"\n")
                            waiting_for_input = False # end
                            break
                        elif data:
                            if data == b'\r':  
                                channel.send(b"\r\n")
                            outfile.write(data.decode())
                            channel.send(data)
                elif command == "echo" and outfile:
                    outfile.write(command_obj.get_output())
                
                elif command == "python"and len(args) == 0: # Chế độ interactive
                        channel.send("Python 3.5.2 (default, Nov 17 2016, 17:05:23)\r\n".encode())
                        channel.send("[GCC 5.4.0 20160609] on linux\r\n".encode())
                        channel.send("Type \"help\", \"copyright\", \"credits\" or \"license\" for more information.\r\n".encode())
                        channel.send(">>> ".encode())
                        python_input = True
                    
                else:
            # send output and error
                    logging.debug(f"Sending output: {command_obj.get_output()}")
                    channel.send(command_obj.get_output().encode() + b"\r")
                    
                    logging.debug(f"Sending error: {command_obj.get_error()}")
                    if command_obj.get_error():
                        channel.send(command_obj.get_error().encode() + b"\r\n")
                
                if outfile: 
                    outfile.close()

                if python_input:
                    while True:
                        try:
                            user_input = channel.recv(1024).decode().strip()
                            if not user_input:
                                continue

                            channel.send(user_input.encode() + b'\r\n')
                            
                            if user_input.strip().lower() == "exit()" or user_input == "\x04":
                                python_input = False
                                break

                            # Mô phỏng xử lý
                            time.sleep(random.uniform(2,5))
                            channel.send(">>> ".encode())


                        except (KeyboardInterrupt):
                            channel.send("KeyboardInterrupt\r\n ")
                            python_input = False
                            break

                
            elif command == 'exit':
                channel.send("\nBye...\r\n")
                break
            else:
                channel.send(f'-sh: {command}: not found\n'.encode() + b"\r")

        except Exception as e:
            logging.exception(f"[SSH] Error during command processing:")
            break

        except KeyboardInterrupt:
            channel.send("\nExiting shell....\r\n")
            break

def handle_client(client_socket, client_address):
    log_event(f"[SSH] New connection from {client_address}")
    send_message_to_soc(f"[SSH] New connection from {client_address}")

    client_ip = client_address[0]
    connection_time = datetime.utcnow()

    try:
        with paramiko.Transport(client_socket) as transport:
            transport.load_server_moduli()
            
            # RSA_keys from file
            try:
                rsa_key = paramiko.RSAKey(filename=RSA_KEY_PATH)
            except Exception as e:
                log_event(f"[SSH] Error loading RSA key: {e}", level=logging.ERROR)
                return

            transport.add_server_key(rsa_key)

            # check ip
            is_new_ip = check_and_store_ip(client_ip)

            # new IP
            if is_new_ip:
                try:
                    with open(RSA_PUB_KEY_PATH, 'r') as pub_key_file:
                        rsa_pub_key = pub_key_file.read()
                except Exception as e:
                    log_event(f"[SSH] Error reading RSA public key: {e}", level=logging.ERROR)
                    return

                chan = transport.accept(20)
                if chan is None:
                    log_event(f"[SSH] No channel from {client_address}", level=logging.WARNING)
                    return

                # Public key
                chan.send(f"Public RSA Key: {rsa_pub_key}\r\n".encode('utf-8'))


            server = Server(client_ip=client_ip)
            try:
                #transport.local_version = 'OpenSSH 8.3 (protocol 2.0)'
                transport.start_server(server=server)
            except paramiko.SSHException as e:
                log_event(f"[SSH] SSH negotiation failed: {e}", level=logging.ERROR)
                return

            chan = transport.accept(100)
            if chan is None:
                log_event(f"[SSH] No channel from {client_address}", level=logging.WARNING)
                return

            # Banner
            #time.sleep(7)
            chan.send(SERVER_BANNER + b"\r\n\n")
            
            fs_honeypot = fs.SimpleFS(root="")
            handle_esxi_honeypot(chan, client_ip, fs_honeypot)
            
            
    except DisconnectException:
            chan.send(b'Connection closed. \n')
            chan.close()
    except Exception as e:
        logging.exception(f"[SSH] Error handling connection from {client_address}:")
    finally:
        disconnection_time = datetime.utcnow() 
        duration = (disconnection_time - connection_time).total_seconds() 
        
        log_recon(
            client_ip=client_ip,
            client_port=client_address[1],
            duration=duration,
        )
        client_socket.close()


def run_ssh_server(ip_address):
    """SSH_Server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip_address, SSH_PORT))
    server_socket.listen(5)
    log_event(f"[INFO] SSH server listening on {ip_address}:{SSH_PORT}")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            log_event(f"[INFO] Accepted connection from {client_address}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
        except Exception as e:
            log_event(f"[SSH] Error accepting connection: {e}", level=logging.ERROR)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argumentmentument('-a', '--address', type=str, required=True, help='IP Address')
    args = parser.parse_args()
    try:
        threading.Thread(target=run_ssh_server, args=(args.address,)).start()
    except KeyboardInterrupt:
        print(f"\nTerminated.....")
