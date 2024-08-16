import logging
import os
import pty
import socket
import subprocess
import threading
import random
import time
import re
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Shell_Commands')))  

import ESXi_fs as fs 
from scapy.all import *
from config import OPENSLP_PORT, SERVER_IP, POC_DATABASE
from utils import send_message_to_soc, log_event
from ssh2 import handle_esxi_honeypot, fs_honeypot

# --- OpenSLP Deception ---

# List of fake service
FAKE_SERVICES = [
    {
        "service_type": "service:test",
        "service_url": "http://fake-esxi.local/test",
        "attributes": "(attr1=val1),(attr2=val2)",
    },
    {
        "service_type": "service:example",
        "service_url": "https://fake-esxi.local/example",
        "attributes": "(attr3=val3)",
    },
]

# --- ESXi Shell Mocking ---
def handle_esxi_shell(client_socket, address):
    """import logging
import os
import pty
import socket
import subprocess
import threading
import random
import time
import re
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Shell_Commands')))  

import ESXi_fs as fs 
from scapy.all import *
from config import OPENSLP_PORT, SERVER_IP, POC_DATABASE
from utils import send_message_to_soc, log_event
from ssh2 import handle_esxi_honeypot, fs_honeypot

# --- OpenSLP Deception ---

# List of fake service
FAKE_SERVICES = [
    {
        "service_type": "service:test",
        "service_url": "http://fake-esxi.local/test",
        "attributes": "(attr1=val1),(attr2=val2)",
    },
    {
        "service_type": "service:example",
        "service_url": "https://fake-esxi.local/example",
        "attributes": "(attr3=val3)",
    },
]

# --- ESXi Shell Mocking ---
def handle_esxi_shell(client_socket, address):
    """Mô phỏng shell của ESXi."""
    log_event(f"[ESXi Shell] Connection {address}")

   # Create Pseudo-Terminal and execute Honeypot's Shell
    master, slave = pty.openpty()
    shell_command = ["/bin/bash"]  

    shell_process = subprocess.Popen(shell_command, stdin=slave, stdout=slave, stderr=slave)

    # Input/output redirect between socket and pseudo-terminal
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            os.write(master, data)

            output = os.read(master, 1024)
            client_socket.send(output)
        except Exception as e:
            log_event(f"[ESXi Shell] Error: {e}", level=logging.ERROR)
            break

    shell_process.terminate()
    client_socket.close()

def handle_openslp_exploit(client_socket, address):
    "" "Simulation of OpenSLP gap and creating shell." ""
    client_ip = address[0]
    print(f"[OpenSLP Exploit] Connection {address}")
    log_event(f"[OpenSLP Exploit] Connection {address}")

    # Simulation time to exploit blossomsg
    delay = random.uniform(2, 5) 
    for i in range(int(delay)):
        print(f"[OpenSLP Exploit] Exploiting... {int(delay - i)}s remaining", end='\r')
        time.sleep(1)
    print(" " * 50, end='\r')  

    try:
        # Successful simulation
        print(f"[OpenSLP Exploit] Exploit successful! Spawning shell for {address}...")
        log_event(f"[OpenSLP Exploit] Exploit successful! Spawning shell for {address}...")

        # Create a simulator
        #handle_esxi_honeypot(client_socket, client_ip, fs_honeypot)

    except Exception as e:
        log_event(f"[OpenSLP Exploit] Error: {e}", level=logging.ERROR)
        client_socket.close()
MARKER = b"\xef\xbe\xad\xde"
def handle_openslp_request(client_socket, address):
    "" "Processing fake OpenSLP requirements (TCP)." ""

    try:
        data = client_socket.recv(1024)
        log_event(f"[OpenSLP] checking file of payload: {len(data)} > 10")

        # Kiểm tra PoC dựa trên signature
        request_str = data.decode('utf-8', errors='ignore')
        # for poc_name, poc_info in POC_DATABASE.items():
        #     if "signature" in poc_info and re.search(poc_info["signature"], request_str):
        #         log_event(f"[OpenSLP] Detected PoC: {poc_name} from {address} with signature: {poc_info['signature']}")
        #         send_message_to_soc(f"[OpenSLP] Detected PoC: {poc_name} from {address} with signature: {poc_info['signature']}")
        #         # Record log in honeypot.log
        #         with open("honeypot.log", "a") as f:
        #             f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Detected PoC: {poc_name}\n")
        #         with open("honeypot.log", "a") as f:
        #             f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Payload: {data.hex()}\n")
        #         # Start the thread processing shell of fake ESXI
        #         #threadingThread(target=handleEsxiShell,Args=(clientSocket,Address))Start()
        #         return
        
        # Analysis of requirements and extract information
        request_parts = request_str.split(" ")
        request_type = request_parts[0]
        
       # Processing regular OpenLP requests
        if request_type == "SrvRqst":
            # Service search requirements
            service = random.choice(FAKE_SERVICES)
            fake_response = f"SrvRply {service['service_type']} {service['service_url']} {service['attributes']}\r\n".encode()
        elif request_type == "AttrRqst":
            # Request to get the properties of the service
            fake_response = b"AttrRply (attr1=fake),(attr2=value)\r\n"
        else:
            if len(data) > 10:
                client_socket.send(MARKER)
                log_event(f"[OpenSLP] Sent marker to {address} (payload size: {len(data)})")
                log_event(f"[OpenSLP] Detected potential ESXi exploit attempt.")
                # Write Payload into the Honeypot.log file
                with open("honeypot.log", "a") as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Payload: {data.hex()}\n")

                # Switch to handling of vulnerability simulation
                handle_openslp_exploit(client_socket, address)
                return    
            else:
            	fake_response = b"OpenSLP-Error: Unsupported request type\r\n"

        client_socket.send(fake_response)

        try:
            request_str = data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                request_str = data.decode('latin-1')  
            except UnicodeDecodeError:
                try:
                    request_str = data.decode('ascii') 
                except UnicodeDecodeError:
                    log_event(f"[OpenSLP] Error decoding request: Unable to decode data.", level=logging.ERROR)
                    return
  

        log_event(f"[OpenSLP] Request from {address}: {request_str}")
        send_message_to_soc(f"[OpenSLP] Request from {address}: {request_str}")
        

        # POC test
        for poc_name, poc_info in POC_DATABASE.items():
            if "signature" in poc_info and poc_info["signature"] in request_str:
                log_event(f"[OpenSLP] Detected PoC: {poc_name} from {address}")
                send_message_to_soc(f"[OpenSLP] Detected PoC: {poc_name} from {address}")
            elif "service_type" in poc_info and poc_info["service_type"] in request_str:
                log_event(f"[OpenSLP] Detected PoC: {poc_name} from {address}")
                send_message_to_soc(f"[OpenSLP] Detected PoC: {poc_name} from {address}")

    except UnicodeDecodeError as e:
        log_event(f"[OpenSLP] Error decoding request from {address}: {e}", level=logging.ERROR)
    except Exception as e:
        log_event(f"[OpenSLP] Error handling request: {e}", level=logging.ERROR)


def run_openslp_server():
    "" "Open OpenSLP server fake." "" "
    # Starting TCP server
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.bind((SERVER_IP, OPENSLP_PORT))
    sock_tcp.listen(1)
    print(f"[OpenSLP] The OpenLP is listening to the gate {OPENSLP_PORT} (TCP)")
    log_event(f"[OpenSLP] OpenSLP server started on port {OPENSLP_PORT} (TCP)")

    while True:
        try:
            client_socket, client_address = sock_tcp.accept()
            log_event(f"[INFO] Accepted connection from {client_address}")
            client_handler = threading.Thread(target=handle_openslp_request, args=(client_socket, client_address))
            client_handler.start()
        except Exception as e:
            log_event(f"[SSH] Error accepting connection: {e}", level=logging.ERROR)


if __name__ == "__main__":
    run_openslp_server()."""
    log_event(f"[ESXi Shell] Connection {address}")

   # Create Pseudo-Terminal and execute Honeypot's Shell
    master, slave = pty.openpty()
    shell_command = ["/bin/bash"]  

    shell_process = subprocess.Popen(shell_command, stdin=slave, stdout=slave, stderr=slave)

    # Input/output redirect between socket and pseudo-terminal
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            os.write(master, data)

            output = os.read(master, 1024)
            client_socket.send(output)
        except Exception as e:
            log_event(f"[ESXi Shell] Error: {e}", level=logging.ERROR)
            break

    shell_process.terminate()
    client_socket.close()

def handle_openslp_exploit(client_socket, address):
    "" "Simulation of OpenSLP gap and creating shell." ""
    client_ip = address[0]
    print(f"[OpenSLP Exploit] Connection {address}")
    log_event(f"[OpenSLP Exploit] Connection {address}")

    # Simulation time to exploit blossomsg
    delay = random.uniform(2, 5) 
    for i in range(int(delay)):
        print(f"[OpenSLP Exploit] Exploiting... {int(delay - i)}s remaining", end='\r')
        time.sleep(1)
    print(" " * 50, end='\r')  

    try:
        # Successful simulation
        print(f"[OpenSLP Exploit] Exploit successful! Spawning shell for {address}...")
        log_event(f"[OpenSLP Exploit] Exploit successful! Spawning shell for {address}...")

        # Create a simulator
        #handle_esxi_honeypot(client_socket, client_ip, fs_honeypot)

    except Exception as e:
        log_event(f"[OpenSLP Exploit] Error: {e}", level=logging.ERROR)
        client_socket.close()
MARKER = b"\xef\xbe\xad\xde"
def handle_openslp_request(client_socket, address):
    "" "Processing fake OpenSLP requirements (TCP)." ""

    try:
        data = client_socket.recv(1024)
        log_event(f"[OpenSLP] checking file of payload: {len(data)} > 10")

        # Kiểm tra PoC dựa trên signature
        request_str = data.decode('utf-8', errors='ignore')
        # for poc_name, poc_info in POC_DATABASE.items():
        #     if "signature" in poc_info and re.search(poc_info["signature"], request_str):
        #         log_event(f"[OpenSLP] Detected PoC: {poc_name} from {address} with signature: {poc_info['signature']}")
        #         send_message_to_soc(f"[OpenSLP] Detected PoC: {poc_name} from {address} with signature: {poc_info['signature']}")
        #         # Record log in honeypot.log
        #         with open("honeypot.log", "a") as f:
        #             f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Detected PoC: {poc_name}\n")
        #         with open("honeypot.log", "a") as f:
        #             f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Payload: {data.hex()}\n")
        #         # Start the thread processing shell of fake ESXI
        #         #threadingThread(target=handleEsxiShell,Args=(clientSocket,Address))Start()
        #         return
        
        # Analysis of requirements and extract information
        request_parts = request_str.split(" ")
        request_type = request_parts[0]
        
       # Processing regular OpenLP requests
        if request_type == "SrvRqst":
            # Service search requirements
            service = random.choice(FAKE_SERVICES)
            fake_response = f"SrvRply {service['service_type']} {service['service_url']} {service['attributes']}\r\n".encode()
        elif request_type == "AttrRqst":
            # Request to get the properties of the service
            fake_response = b"AttrRply (attr1=fake),(attr2=value)\r\n"
        else:
            if len(data) > 10:
                client_socket.send(MARKER)
                log_event(f"[OpenSLP] Sent marker to {address} (payload size: {len(data)})")
                log_event(f"[OpenSLP] Detected potential ESXi exploit attempt.")
                # Write Payload into the Honeypot.log file
                with open("honeypot.log", "a") as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Payload: {data.hex()}\n")

                # Switch to handling of vulnerability simulation
                handle_openslp_exploit(client_socket, address)
                return    
            else:
            	fake_response = b"OpenSLP-Error: Unsupported request type\r\n"

        client_socket.send(fake_response)

        try:
            request_str = data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                request_str = data.decode('latin-1')  
            except UnicodeDecodeError:
                try:
                    request_str = data.decode('ascii') 
                except UnicodeDecodeError:
                    log_event(f"[OpenSLP] Error decoding request: Unable to decode data.", level=logging.ERROR)
                    return
  

        log_event(f"[OpenSLP] Request from {address}: {request_str}")
        send_message_to_soc(f"[OpenSLP] Request from {address}: {request_str}")
        

        # POC test
        for poc_name, poc_info in POC_DATABASE.items():
            if "signature" in poc_info and poc_info["signature"] in request_str:
                log_event(f"[OpenSLP] Detected PoC: {poc_name} from {address}")
                send_message_to_soc(f"[OpenSLP] Detected PoC: {poc_name} from {address}")
            elif "service_type" in poc_info and poc_info["service_type"] in request_str:
                log_event(f"[OpenSLP] Detected PoC: {poc_name} from {address}")
                send_message_to_soc(f"[OpenSLP] Detected PoC: {poc_name} from {address}")

    except UnicodeDecodeError as e:
        log_event(f"[OpenSLP] Error decoding request from {address}: {e}", level=logging.ERROR)
    except Exception as e:
        log_event(f"[OpenSLP] Error handling request: {e}", level=logging.ERROR)


def run_openslp_server():
    "" "Open OpenSLP server fake." "" "
    # Starting TCP server
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.bind((SERVER_IP, OPENSLP_PORT))
    sock_tcp.listen(1)
    print(f"[OpenSLP] The OpenLP is listening to the gate {OPENSLP_PORT} (TCP)")
    log_event(f"[OpenSLP] OpenSLP server started on port {OPENSLP_PORT} (TCP)")

    while True:
        try:
            client_socket, client_address = sock_tcp.accept()
            log_event(f"[INFO] Accepted connection from {client_address}")
            client_handler = threading.Thread(target=handle_openslp_request, args=(client_socket, client_address))
            client_handler.start()
        except Exception as e:
            log_event(f"[SSH] Error accepting connection: {e}", level=logging.ERROR)


if __name__ == "__main__":
    run_openslp_server()
