import socket
import threading
from config import DCUI_PORT, DCUI_BANNER
from command_handler import handle_command
from utils import send_message_to_soc

def handle_dcui_client(client_socket, address):
    "" "DCUI connectivity processing." ""
    print(f"[DCUI] Connection {address}")
    
    # Make sure DCUI_BANNER is bytes
    if isinstance(DCUI_BANNER, str):
        banner = DCUI_BANNER.encode()
    else:
        banner = DCUI_BANNER

    try:
        client_socket.send(banner) 
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
                    print(f"[DCUI] {address} - Command is empty. Breaking.")
                    break
                print(f"[DCUI] {address} - Command: {command}")

                # Use Command_handler to handle commands
                response = handle_command(command, "DCUI", address)
                client_socket.send(response.encode())
                client_socket.send(b"dcui> ")
            except Exception as e:
                print(f"[DCUI] Error during command processing: {e}")
                break
    except Exception as e:
        print(f"[DCUI] Error: {e}")
    finally:
        client_socket.close()

def run_dcui_server():
    """Start the DCUI server simulating."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(('', DCUI_PORT)) 
            sock.listen()
            print(f"[DCUI] Honeypot dcui is listening to the port {DCUI_PORT}")
            
            while True:
                client_socket, address = sock.accept()
                print(f"[DCUI] Accept connection from {address}")
                threading.Thread(target=handle_dcui_client, args=(client_socket, address)).start()
        except Exception as e:
            print(f"[DCUI] Error when bind or listen on the port {DCUI_PORT}: {e}")

if __name__ == "__main__":
    run_dcui_server()
