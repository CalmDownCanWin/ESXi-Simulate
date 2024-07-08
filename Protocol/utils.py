import socket
import random
import logging
import string

from config import SOC_HOST, SOC_PORT

# Cấu hình logging
logging.basicConfig(filename="honeypot.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
# utils.py
def send_message_to_soc(message):
    print(message)

#def send_message_to_soc(message):
#   """Gửi thông báo đến SOC."""
#    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#       try:
#           sock.connect((SOC_HOST, SOC_PORT))
#           sock.sendall(message.encode())
#       except:
#           logging.error("[!] Lỗi kết nối đến SOC.")

def generate_random_mac():
    # Tạo một địa chỉ MAC ngẫu nhiên
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return bytes(mac)

def log_event(message, level=logging.INFO):
    """Ghi log sự kiện vào file."""
    logging.log(level, message)

def generate_random_string(length=10):
    """Tạo chuỗi ngẫu nhiên với độ dài cho trước."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_random_ip():
    """Tạo địa chỉ IP ngẫu nhiên."""
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def format_mac_address(mac, separator=":"):
    """Chuyển đổi MAC address sang định dạng mong muốn."""
    if isinstance(mac, bytes):
        mac = mac.hex()
    return separator.join(mac[i:i+2] for i in range(0, len(mac), 2))
