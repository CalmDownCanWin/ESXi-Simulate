import socket
import threading
from config import DCUI_PORT, DCUI_BANNER
from command_handler import handle_command
from utils import send_message_to_soc

def handle_dcui_client(client_socket, address):
    """DCUI connection handling."""
    print(f"[DCUI] Connect from {address}")
    client_socket.send(DCUI_BANNER) 
    client_socket.send(b"Enter username: ")
    username = client_socket.recv(1024).decode().strip()
    client_socket.send(b"Enter password: ")
    password = client_socket.recv(1024).decode().strip()

    print(f"[DCUI] {address} - Username: {username}, Password: {password}")
    send_message_to_soc(f"[DCUI] {address} - Username: {username}, Password: {password}")

    client_socket.send(b"Welcome to VMware ESXi DCUI\n")
    client_socket.send(b"dcui> ")
    while True:
        try:
            command = client_socket.recv(1024).decode().strip()
            if not command:
                break

            # Use command_handler to handle commands
            response = handle_command(command, "DCUI", address)
            client_socket.send(response.encode())
            client_socket.send(b"dcui> ")
        except Exception as e:
            print(f"[DCUI] Erro: {e}")
            break
    client_socket.close()

def run_dcui_server():
    """Start the DCUI emulator server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', DCUI_PORT))
        sock.listen()
        print(f"[DCUI] DCUI honeypot is listening on port {DCUI_PORT}")
        while True:
            client_socket, address = sock.accept()
            threading.Thread(target=handle_dcui_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    run_dcui_server()
