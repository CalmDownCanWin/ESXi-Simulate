import logging
import paramiko

def send_message_to_soc(message):
    # Dummy implementation for sending a message to a socket or a monitoring system
    print(f"Monitoring: {message}")

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
def DisconnectException(Exception):
    pass
   
def disconnect_attacker():
    raise DisconnectException()
