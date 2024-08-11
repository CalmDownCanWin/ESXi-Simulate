import random
import string
import hashlib
from difflib import unified_diff
import socket

def generate_random_mac():
    """Tạo một địa chỉ MAC ngẫu nhiên."""
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return bytes(mac)


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

def get_file_content(filepath):
    """Đọc nội dung của file, xử lý lỗi nếu có."""
    try:
        with open(filepath, "r") as f:
            return f.readlines()
    except Exception as e:
        return [f"Lỗi khi đọc file: {e}\n"]  # Trả về list để tương thích với unified_diff


def get_file_diff(filepath, previous_hash):
    """Lấy nội dung thay đổi của file sử dụng difflib."""
    try:
        current_content = get_file_content(filepath)
        # Tạo nội dung giả lập cho file trước đó dựa trên hash
        previous_content = [f"# Hash: {previous_hash}\n"]
        diff = "".join(unified_diff(previous_content, current_content, lineterm=''))
        return diff
    except Exception as e:
        return f"Lỗi khi lấy nội dung thay đổi: {e}"

def send_message_to_soc(message, host, port):
    """Gửi thông báo đến SOC qua UDP."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            sock.sendto(message.encode(), (host, port))
        except Exception as e:
            print(f"Lỗi khi gửi thông báo đến SOC: {e}")