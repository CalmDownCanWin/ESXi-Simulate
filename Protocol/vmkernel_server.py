import socket
import threading
import random
import time
from config import VMOTION_PORT, ISCSI_PORT
from utils import send_message_to_soc, generate_random_mac

# --- vMotion Deception ---

def handle_vmotion_connection(client_socket, address):
    """Xử lý kết nối vMotion giả mạo."""
    print(f"[vMotion] Kết nối từ {address}")
    send_message_to_soc(f"[vMotion] Kết nối từ {address}")

    # Deception: Gửi một số dữ liệu giả mạo 
    # và sau đó đóng kết nối để mô phỏng lỗi
    fake_data = b"VMOTION\x00\x01\x00\x00" + generate_random_mac()
    print(f"[vMotion] Sending data: {fake_data}")
    try:
        client_socket.send(fake_data)
    except Exception as e:
        print(f"[vMotion] Lỗi khi gửi dữ liệu: {e}")
    time.sleep(random.uniform(0.5, 2))  # Tạo độ trễ ngẫu nhiên
    client_socket.close()
    print(f"[vMotion] Kết nối từ {address} đã bị đóng")

def run_vmotion_server():
    """Khởi động vMotion server giả mạo."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', VMOTION_PORT))  # Sử dụng VMOTION_PORT từ config
        sock.listen()
        print(f"[vMotion] vMotion giả mạo đang lắng nghe trên cổng {VMOTION_PORT}")
        while True:
            client_socket, address = sock.accept()
            threading.Thread(target=handle_vmotion_connection, args=(client_socket, address)).start()

# --- iSCSI Deception ---

def handle_iscsi_connection(client_socket, address):
    """Xử lý kết nối iSCSI giả mạo."""
    print(f"[iSCSI] Kết nối từ {address}")
    send_message_to_soc(f"[iSCSI] Kết nối từ {address}")

    # Deception: Trả về Login Response giả mạo
    fake_response = b"iSCSI\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    print(f"[iSCSI] Sending data: {fake_response}")
    try:
        client_socket.send(fake_response)
    except Exception as e:
        print(f"[iSCSI] Lỗi khi gửi dữ liệu: {e}")
    client_socket.close()
    print(f"[iSCSI] Kết nối từ {address} đã bị đóng")

def run_iscsi_server():
    """Khởi động iSCSI server giả mạo."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', ISCSI_PORT))  # Sử dụng ISCSI_PORT từ config
        sock.listen()
        print(f"[iSCSI] iSCSI giả mạo đang lắng nghe trên cổng {ISCSI_PORT}")
        while True:
            client_socket, address = sock.accept()
            threading.Thread(target=handle_iscsi_connection, args=(client_socket, address)).start()

# --- Khởi chạy các server ---

def run_vmkernel_server():
    """Khởi động các dịch vụ mạng giả mạo."""
    vmotion_thread = threading.Thread(target=run_vmotion_server)
    iscsi_thread = threading.Thread(target=run_iscsi_server)
    vmotion_thread.start()
    iscsi_thread.start()

if __name__ == "__main__":
    run_vmkernel_server()
