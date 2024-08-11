import logging
import paramiko

def send_message_to_soc(message):
    # Dummy implementation for sending a message to a socket or a monitoring system
    print(f"Sending message: {message}")

def log_event(message, level=logging.INFO, filename="honeypot.log"):
    """Ghi log thông tin vào file."""
    logging.basicConfig(filename=filename, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    if level == logging.INFO:
        logging.info(message)
    elif level == logging.WARNING:
        logging.warning(message)
    elif level == logging.ERROR:
        logging.error(message)
    elif level == logging.DEBUG:
        logging.debug(message)
def get_ssh_fingerprint_from_file(key_path):
    """Lấy fingerprint từ file RSA key."""
    try:
        key = paramiko.RSAKey.from_private_key_file(key_path)
        fingerprint = key.get_fingerprint().hex(':')  
        return fingerprint
    except Exception as e:
        logging.error(f"[!] Lỗi khi lấy fingerprint từ file: {e}")
        return None
def generate_random_mac():
    # Tạo một địa chỉ MAC ngẫu nhiên
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
