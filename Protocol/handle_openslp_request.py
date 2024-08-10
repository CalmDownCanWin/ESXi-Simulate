import logging
import os
import pty
import socket
import subprocess
import threading
import random
import time
import re
from config import OPENSLP_PORT, SERVER_IP
from utils import send_message_to_soc, log_event
from poc_database import POC_DATABASE  # Nhập POC_DATABASE

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

def handle_openslp_request_udp(data, address):
    """Xử lý yêu cầu OpenSLP giả mạo (UDP)."""
    try:
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

        # Phân tích yêu cầu và trích xuất thông tin
        request_parts = request_str.split(" ")
        request_type = request_parts[0]

        # Kiểm tra xem payload có lớn hơn 10 byte hay không
        log_event(f"[OpenSLP] checking size of payload: {len(data)} > 10")
        if len(data) > 10:
            log_event(f"[OpenSLP] Detected potential ESXi exploit attempt.")

            # Tạo socket và lắng nghe kết nối từ payload
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind(('', random.randint(1025, 65535)))  # Chọn cổng ngẫu nhiên
                sock.listen(1)
                client_socket, _ = sock.accept()

                # Khởi động thread xử lý shell của ESXi giả mạo
                threading.Thread(target=handle_esxi_shell, args=(client_socket, address)).start()
            return

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

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(fake_response, address)

    except UnicodeDecodeError as e:
        log_event(f"[OpenSLP] Error decoding request from {address}: {e}", level=logging.ERROR)
    except Exception as e:
        log_event(f"[OpenSLP] Error handling request: {e}", level=logging.ERROR)

def handle_openslp_request_tcp(client_socket, address):
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
                threading.Thread(target=handle_esxi_shell, args=(client_socket, address)).start()
                return

        if len(data) > 10:
            log_event(f"[OpenSLP] Detected potential ESXi exploit attempt.")
            
            # Ghi payload vào file honeypot.log
            with open("honeypot.log", "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {address}: Payload: {data.hex()}\n")

            # Khởi động thread xử lý shell của ESXi giả mạo
            threading.Thread(target=handle_esxi_shell, args=(client_socket, address)).start()
            return        
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

        # Phân tích yêu cầu và trích xuất thông tin
        request_parts = request_str.split(" ")
        request_type = request_parts[0]

        # Kiểm tra xem payload có lớn hơn 10 byte hay không


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

    except UnicodeDecodeError as e:
        log_event(f"[OpenSLP] Error decoding request from {address}: {e}", level=logging.ERROR)
    except Exception as e:
        log_event(f"[OpenSLP] Error handling request: {e}", level=logging.ERROR)

def run_openslp_server():
    """Khởi động OpenSLP server giả mạo."""
    # Khởi tạo server UDP
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.bind((SERVER_IP, OPENSLP_PORT))
    print(f"[OpenSLP] OpenSLP giả mạo đang lắng nghe trên cổng {OPENSLP_PORT} (UDP)")
    log_event(f"[OpenSLP] OpenSLP server started on port {OPENSLP_PORT} (UDP)")
    threading.Thread(target=lambda: listen_udp(sock_udp)).start()

    # Khởi tạo server TCP
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.bind((SERVER_IP, OPENSLP_PORT))
    sock_tcp.listen(1)
    print(f"[OpenSLP] OpenSLP giả mạo đang lắng nghe trên cổng {OPENSLP_PORT} (TCP)")
    log_event(f"[OpenSLP] OpenSLP server started on port {OPENSLP_PORT} (TCP)")
    threading.Thread(target=lambda: listen_tcp(sock_tcp)).start()

def listen_udp(sock_udp):
    while True:
        data, address = sock_udp.recvfrom(1024)
        threading.Thread(target=handle_openslp_request_udp, args=(data, address)).start()

def listen_tcp(sock_tcp):
    while True:
        client_socket, address = sock_tcp.accept()
        threading.Thread(target=handle_openslp_request_tcp, args=(client_socket, address)).start()

if __name__ == "__main__":
    run_openslp_server()
