import socket
import threading
import random
import time
from config import VMOTION_PORT, ISCSI_PORT
from utils import send_message_to_soc, generate_random_mac

# --- vMotion Deception ---

def handle_vmotion_connection(client_socket, address):
    """Processing fake VMotion connection."""
    print(f"[vMotion] Connection {address}")
    send_message_to_soc(f"[vMotion] Connection {address}")

    # Deception: Send some fake data
    # And then close the connection to simulate the error
    fake_data = b"VMOTION\x00\x01\x00\x00" + generate_random_mac()
    print(f"[vMotion] Sending data: {fake_data}")
    try:
        client_socket.send(fake_data)
    except Exception as e:
        print(f"[vMotion] Error when sending data: {e}")
    time.sleep(random.uniform(0.5, 2)) 
    client_socket.close()
    print(f"[vMotion] Connection {address} closed")

def run_vmotion_server():
    """Start the fake VMotion server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', VMOTION_PORT))  
        sock.listen()
        print(f"[vMotion] The fake VMotion is listening to the port {VMOTION_PORT}")
        while True:
            client_socket, address = sock.accept()
            threading.Thread(target=handle_vmotion_connection, args=(client_socket, address)).start()

# --- iSCSI Deception ---

def handle_iscsi_connection(client_socket, address):
    """Fake ISCSI connection processing."""
    print(f"[iSCSI] Connection {address}")
    send_message_to_soc(f"[iSCSI] Connection {address}")

    # Deception: Returns fake login response
    fake_response = b"iSCSI\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    print(f"[iSCSI] Sending data: {fake_response}")
    try:
        client_socket.send(fake_response)
    except Exception as e:
        print(f"[iSCSI] Error when sending data: {e}")
    client_socket.close()
    print(f"[iSCSI] Connection {address} closed")

def run_iscsi_server():
    """Start ISCSI server fake."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', ISCSI_PORT)) 
        sock.listen()
        print(f"[iSCSI] iSCSI The fake is listening to the port {ISCSI_PORT}")
        while True:
            client_socket, address = sock.accept()
            threading.Thread(target=handle_iscsi_connection, args=(client_socket, address)).start()

# --- Run the servers ---

def run_vmkernel_server():
    """Start fake network services."""
    vmotion_thread = threading.Thread(target=run_vmotion_server)
    iscsi_thread = threading.Thread(target=run_iscsi_server)
    vmotion_thread.start()
    iscsi_thread.start()

if __name__ == "__main__":
    run_vmkernel_server()
