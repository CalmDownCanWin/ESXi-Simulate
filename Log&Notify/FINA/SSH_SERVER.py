import socket
import threading
from command_handler import handle_command
from LOG_TO_SPLUNK import log_attack

SSH_PORT = 2222
SSH_BANNER = b"SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.5\r\n"

def handle_ssh_client(client_socket, address):
    """Xử lý kết nối SSH."""

    # Ghi log kết nối SSH
    log_attack(event_type="ssh_connection", attacker_address=address[0], attacker_port=address[1])

    try:
        # Gửi banner SSH
        client_socket.send(SSH_BANNER)

        # Mô phỏng prompt đăng nhập
        client_socket.send(b"login as: ")
        username = client_socket.recv(1024).decode().strip()
        client_socket.send(b"Password: ")
        password = client_socket.recv(1024).decode().strip()

        # Ghi log thông tin đăng nhập
        log_attack(event_type="ssh_login_attempt", username=username, password=password, attacker_address=address[0], attacker_port=address[1])

        # Validate username/password (tuỳ chỉnh logic)
        is_authenticated = authenticate(username, password) 

        if is_authenticated:
            log_attack(event_type="ssh_login_success", username=username, attacker_address=address[0], attacker_port=address[1])
            client_socket.send(b"Authentication successful!\r\n")
            client_socket.send(b"user@honeypot:~$ ")
            
            while True:
                try:
                    command = client_socket.recv(1024).decode().strip()
                    if not command:
                        break

                    # Ghi log lệnh SSH được thực thi
                    log_attack(event_type="ssh_command", command=command, username=username, attacker_address=address[0], attacker_port=address[1])

                    response = handle_command(command, "SSH", address)
                    client_socket.send(response.encode())
                    client_socket.send(b"user@honeypot:~$ ")

                except Exception as e:
                    log_attack(event_type="ssh_command_error", command=command, error=str(e), attacker_address=address[0], attacker_port=address[1])
                    break

        else:
            log_attack(event_type="ssh_login_failed", username=username, attacker_address=address[0], attacker_port=address[1])
            client_socket.send(b"Authentication failed!\r\n")
            client_socket.close()

    except Exception as e:
        log_attack(event_type="ssh_error", error=str(e), attacker_address=address[0], attacker_port=address[1])
        client_socket.close()

def authenticate(username, password):
    """Kiểm tra username/password (thay thế bằng logic của bạn)."""
    # Ví dụ: Kiểm tra với danh sách user/password cứng 
    VALID_USERS = {"root": "password123"} 
    return username in VALID_USERS and VALID_USERS[username] == password

def run_ssh_server():
    """Khởi động SSH server giả lập."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', SSH_PORT))
        sock.listen()
        print(f"[SSH] Honeypot SSH listening on port {SSH_PORT}")
        while True:
            client_socket, address = sock.accept()
            threading.Thread(target=handle_ssh_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    run_ssh_server()