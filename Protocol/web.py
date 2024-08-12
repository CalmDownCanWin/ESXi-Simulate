import socket
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import os
import subprocess
from config import SERVER_IP, HTTPS_PORT

def generate_self_signed_certificate(certfile, keyfile):
    """tạoSelfSignedCertificate"""
    if not os.path.exists(certfile) or not os.path.exists(keyfile):
        os.system(f"openssl req -x509 -newkey rsa:4096 -nodes -out {certfile} -keyout {keyfile} -days 365 -subj '/CN={socket.gethostname()}'")
        print(f"Generated self-signed certificate: {certfile}")
    else:
        print(f"Using existing certificate: {certfile}")

def run_https_server(ip_address, port, html_dir, keyfile, certfile):
    """Start https server.

    Args:
        SERVER_IP: IP address to bind server.
        port: port to listen.
        html_dir: The folder contains HTML and JS files.
        keyfile: The path to the private key file (for example: key.pem).
        certfile: The path to the Certificate file (for example: cert.pem).
    """
    class MyHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=html_dir, **kwargs)

    httpd = HTTPServer((ip_address, port), MyHandler)

    # Sử dụng SSL/TLS
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=keyfile, certfile=certfile, server_side=True)

    print(f"HTTPS server started on {ip_address}:{port}, serving from {html_dir}")
    httpd.serve_forever()
    
def create_virtual_ip(ip_address):
    """Create virtual IP address if not exist on any interface."""
    try:
        # Get a list of all network interfaces
        output = subprocess.check_output(["ip", "link"], stderr=subprocess.STDOUT).decode()
        interfaces = [line.split(":")[1].strip() for line in output.splitlines() if ":" in line]

        # Check if the IP address exists on any interface yet
        ip_exists = False
        for interface in interfaces:
            try:
                subprocess.check_output(["ip", "addr", "show", "dev", interface], stderr=subprocess.STDOUT)
                if ip_address in output:
                    ip_exists = True
                    break
            except subprocess.CalledProcessError:
                pass

        if not ip_exists:
            # IP address does not exist, created new on the first interface
            print(f"Creating virtual IP address: {ip_address} on interface eth0")
            os.system(f"sudo ip addr add {ip_address}/24 dev eth0") 
        else:
            print(f"IP address {ip_address} already exists.")

    except Exception as e:
        log_event(f"[ERROR] Failed to create virtual IP: {e}", level=logging.ERROR)
if __name__ == "__main__":
    html_dir = "web"
    keyfile = "key.pem"
    certfile = "cert.pem"

    # Create a Certificate if not existed
    generate_self_signed_certificate(certfile, keyfile)

    # Create virtual IP address if not existed
    create_virtual_ip(SERVER_IP)

    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_https_server, args=(SERVER_IP, HTTPS_PORT, html_dir, keyfile, certfile))
    server_thread.start()
