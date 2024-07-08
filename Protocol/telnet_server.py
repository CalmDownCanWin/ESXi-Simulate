import socket
import threading
from config import SYSLOG_PORT
from utils import send_message_to_soc, log_event

def handle_syslog_message(data, address):
    """Xử lý thông điệp syslog giả mạo."""
    try:
        message = data.decode('utf-8')
        print(f"[Syslog] Nhận thông điệp từ {address}: {message}")
        send_message_to_soc(f"[Syslog] Nhận thông điệp từ {address}: {message}")

        # --- Deception (Tùy chọn) ---
        # Ví dụ: Tạo message syslog giả mạo
        # fake_message = f"<134>1 192.168.1.10 fakehost - - [origin software=\"sshd\" swVersion=\"OpenSSH_7.6p1 Ubuntu-4ubuntu0.5\"] Invalid user test from 192.168.1.2 port 52484"
        # send_message_to_soc(f"[Syslog] Gửi message giả mạo đến {address}: {fake_message}")
        # sock.sendto(fake_message.encode(), address)

    except UnicodeDecodeError as e:
        log_event(f"[Syslog] Lỗi khi decode thông điệp từ {address}: {e}", level=logging.ERROR)
    except Exception as e:
        log_event(f"[Syslog] Lỗi khi xử lý thông điệp từ {address}: {e}", level=logging.ERROR)

def run_syslog_server():
    """Khởi động syslog server giả mạo."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            sock.bind(('', SYSLOG_PORT))
            print(f"[Syslog] Syslog server giả mạo đang lắng nghe trên cổng {SYSLOG_PORT}")
        except Exception as e:
            log_event(f"[Syslog] Lỗi khi bind cổng {SYSLOG_PORT}: {e}", level=logging.ERROR)
            return

        while True:
            try:
                data, address = sock.recvfrom(1024)
                threading.Thread(target=handle_syslog_message, args=(data, address)).start()
            except Exception as e:
                log_event(f"[Syslog] Lỗi khi nhận dữ liệu: {e}", level=logging.ERROR)

if __name__ == "__main__":
    run_syslog_server()
