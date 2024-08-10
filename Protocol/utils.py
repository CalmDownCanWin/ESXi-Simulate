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
