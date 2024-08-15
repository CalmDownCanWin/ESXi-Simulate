import logging
import os
import pty
import socket
import subprocess
import threading
import random
import time
import re
import argparse

from Settings.config import OPENSLP_PORT, POC_DATABASE, LOG_ROOT
from Settings.utils import send_message_to_soc, log_event
from ssh2 import handle_esxi_honeypot, fs_honeypot

# --- OpenSLP Deception ---

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
    """Emulate ESXI Shell."""
    log_event(f"[ESXi Shell] Connection from {address}")

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
    """Simulate exploiting vulnerability and spawning shell!"""
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
        handle_esxi_honeypot(client_socket, client_ip, fs_honeypot)

    except Exception as e:
        log_event(f"[OpenSLP Exploit] Error: {e}", level=logging.ERROR)
        client_socket.close()


def handle_openslp_request(client_socket, address):
    """Request is coming!"""

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
                with open(os.path.join(LOG_ROOT,"honeypot.log"), "a") as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Detected PoC: {poc_name}\n")
                with open(os.path.join(LOG_ROOT,"honeypot.log"), "a") as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Payload: {data.hex()}\n")
                # Bắt đầu thread xử lý shell của ESXi giả mạo
                threading.Thread(target=handle_esxi_shell, args=(client_socket, address)).start()
                return
        
        # Phân tích yêu cầu và trích xuất thông tin
        request_parts = request_str.split(" ")
        request_type = request_parts[0]
        
        # Xử lý các request OpenSLP thông thường
        if request_type == "SrvRqst":
            # Yêu cầu tìm kiếm dịch vụ
            service = random.choice(FAKE_SERVICES)
            fake_response = f"SrvRply {service['service_type']} {service['service_url']} {service['attributes']}\r\n".encode()
        elif request_type == "AttrRqst":
            # Yêu cầu lấy thuộc tính của service
            fake_response = b"AttrRply (attr1=fake),(attr2=value)\r\n"
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

        if len(data) > 10:
            log_event(f"[OpenSLP] Detected potential ESXi exploit attempt.")
            # Ghi payload vào file honeypot.log
            with open(os.path.join(LOG_ROOT,"honeypot.log"), "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Payload: {data.hex()}\n")

            # Chuyển sang xử lý mô phỏng khai thác lỗ hổng
            handle_openslp_exploit(client_socket, address)
            return      

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

def run_openslp_server(SERVER_IP):
    """Start Server"""
    # Khởi tạo server TCP
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.bind((SERVER_IP, OPENSLP_PORT))
    sock_tcp.listen(1)
    print(f"[OpenSLP] OpenSLP is listening on port {OPENSLP_PORT} (TCP)")
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
    parser = argparse.ArgumentParser()
    parser.add_argumentmentument('-a', '--address', type=str, required=True, help='IP Address')
    args = parser.parse_args()
    try:
        threading.Thread(target=run_openslp_server, args=(args.address,)).start()
    except KeyboardInterrupt:
        print(f"\nTerminated.....")
