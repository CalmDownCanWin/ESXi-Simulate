import logging
import paramiko

def send_message_to_soc(message):
    # Dummy implementation for sending a message to a socket or a monitoring system
    print(f"Sending message: {message}")

def log_event(message, level=logging.INFO):
    # Log the event with the specified logging level
    if level == logging.DEBUG:
        logging.debug(message)
    elif level == logging.WARNING:
        logging.warning(message)
    elif level == logging.ERROR:
        logging.error(message)
    else:
        logging.info(message)
def get_ssh_fingerprint_from_file(key_path):
    """fingerprint from file RSA key."""
    try:
        key = paramiko.RSAKey.from_private_key_file(key_path)
        fingerprint = key.get_fingerprint().hex(':')  
        return fingerprint
    except Exception as e:
        logging.error(f"[!]Error: fingerprint: {e}")
        return None
def generate_random_mac():
    # Create a random Mac address
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return bytes(mac)

def generate_random_string(length=10):
    "" "" Create a random string with a given length. "" ""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_random_ip():
    "" "Create a random IP address." ""
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def format_mac_address(mac, separator=":"):
    "" "Convert Mac address to the desired format." ""
    if isinstance(mac, bytes):
        mac = mac.hex()
    return separator.join(mac[i:i+2] for i in range(0, len(mac), 2))
def DisconnectException(Exception):
    pass
   
def disconnect_attacker():
    raise DisconnectException()
