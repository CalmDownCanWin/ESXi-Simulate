import socket
import threading
from config import DCUI_PORT, DCUI_BANNER
from command_handler import handle_command
from utils import send_message_to_soc

def handle_dcui_client(client_socket, address):
    """Xử lý kết nối DCUI."""
    print(f"[DCUI] Kết nối từ {address}")
    
    # Đảm bảo DCUI_BANNER là bytes
    if isinstance(DCUI_BANNER, str):
        banner = DCUI_BANNER.encode()
    else:
        banner = DCUI_BANNER

    try:
        client_socket.send(banner)  # Sử dụng DCUI_BANNER từ config
        client_socket.send(b"Enter username: ")
        username = client_socket.recv(1024).decode().strip()
        client_socket.send(b"Enter password: ")
        password = client_socket.recv(1024).decode().strip()

        print(f"[DCUI] {address} - Username: {username}, Password: {password}")
        send_message_to_soc(f"[DCUI] {address} - Username: {username}, Password: {password}")

        client_socket.send(b"Welcome to VMware ESXi DCUI\n")
        client_socket.send(b"dcui> ")

        while True:
            try:
                command = client_socket.recv(1024).decode().strip()
                if not command:
                    print(f"[DCUI] {address} - Command is empty. Breaking.")
                    break
                print(f"[DCUI] {address} - Command: {command}")

                # Sử dụng command_handler để xử lý lệnh
                response = handle_command(command, "DCUI", address)
                client_socket.send(response.encode())
                client_socket.send(b"dcui> ")
            except Exception as e:
                print(f"[DCUI] Lỗi trong khi xử lý lệnh: {e}")
                break
    except Exception as e:
        print(f"[DCUI] Lỗi: {e}")
    finally:
        client_socket.close()

def run_dcui_server():
    """Khởi động DCUI server giả lập."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(('', DCUI_PORT))  # Sử dụng DCUI_PORT từ config
            sock.listen()
            print(f"[DCUI] Honeypot DCUI đang lắng nghe trên cổng {DCUI_PORT}")
            
            while True:
                client_socket, address = sock.accept()
                print(f"[DCUI] Chấp nhận kết nối từ {address}")
                threading.Thread(target=handle_dcui_client, args=(client_socket, address)).start()
        except Exception as e:
            print(f"[DCUI] Lỗi khi bind hoặc listen trên cổng {DCUI_PORT}: {e}")

if __name__ == "__main__":
    run_dcui_server()
