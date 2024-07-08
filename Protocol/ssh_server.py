import socket
import threading
from config import SSH_PORT, SSH_BANNER
from command_handler import handle_command
from utils import send_message_to_soc

def handle_ssh_client(client_socket, address):
    """Xử lý kết nối SSH."""
    print(f"[SSH] Kết nối từ {address}")

    # Đảm bảo SSH_BANNER là bytes
    if isinstance(SSH_BANNER, str):
        banner = SSH_BANNER.encode()
    else:
        banner = SSH_BANNER

    try:
        client_socket.send(banner)
        client_socket.send(b"user@honeypot:~$ ")
        
        while True:
            try:
                command = client_socket.recv(1024).decode().strip()
                if not command:
                    break

                # Sử dụng command_handler để xử lý lệnh
                response = handle_command(command, "SSH", address)
                client_socket.send(response.encode())
                client_socket.send(b"user@honeypot:~$ ")
            except Exception as e:
                print(f"[SSH] Lỗi trong khi xử lý lệnh: {e}")
                break
    except Exception as e:
        print(f"[SSH] Lỗi: {e}")
    finally:
        client_socket.close()

def run_ssh_server():
    """Khởi động SSH server giả lập."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(('', SSH_PORT))  # Sử dụng SSH_PORT từ config
            sock.listen()
            print(f"[SSH] Honeypot SSH đang lắng nghe trên cổng {SSH_PORT}")
            
            while True:
                client_socket, address = sock.accept()
                print(f"[SSH] Chấp nhận kết nối từ {address}")
                threading.Thread(target=handle_ssh_client, args=(client_socket, address)).start()
        except Exception as e:
            print(f"[SSH] Lỗi khi bind hoặc listen trên cổng {SSH_PORT}: {e}")

if __name__ == "__main__":
    run_ssh_server()
