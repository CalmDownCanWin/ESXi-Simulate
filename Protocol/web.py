import socket
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import os
import subprocess
from config import SERVER_IP, HTTPS_PORT

def generate_self_signed_certificate(certfile, keyfile):
    """Tạo self-signed certificate."""
    if not os.path.exists(certfile) or not os.path.exists(keyfile):
        os.system(f"openssl req -x509 -newkey rsa:4096 -nodes -out {certfile} -keyout {keyfile} -days 365 -subj '/CN={socket.gethostname()}'")
        print(f"Generated self-signed certificate: {certfile}")
    else:
        print(f"Using existing certificate: {certfile}")

def run_https_server(ip_address, port, html_dir, keyfile, certfile):
    """Khởi động HTTPS server.

    Args:
        SERVER_IP: Địa chỉ IP để bind server.
        port: Cổng để lắng nghe.
        html_dir: Thư mục chứa file HTML và JS.
        keyfile: Đường dẫn đến file private key (ví dụ: key.pem).
        certfile: Đường dẫn đến file certificate (ví dụ: cert.pem).
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
    """Tạo địa chỉ IP ảo nếu chưa tồn tại trên bất kỳ interface nào."""
    try:
        # Lấy danh sách tất cả các interface mạng
        output = subprocess.check_output(["ip", "link"], stderr=subprocess.STDOUT).decode()
        interfaces = [line.split(":")[1].strip() for line in output.splitlines() if ":" in line]

        # Kiểm tra xem địa chỉ IP đã tồn tại trên interface nào chưa
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
            # Địa chỉ IP chưa tồn tại, tạo mới trên interface đầu tiên
            print(f"Creating virtual IP address: {ip_address} on interface eth0")
            os.system(f"sudo ip addr add {ip_address}/24 dev eth0")  # Thay subnet mask nếu cần
        else:
            print(f"IP address {ip_address} already exists.")

    except Exception as e:
        log_event(f"[ERROR] Failed to create virtual IP: {e}", level=logging.ERROR)
if __name__ == "__main__":
    html_dir = "web"
    keyfile = "key.pem"
    certfile = "cert.pem"

    # Tạo certificate nếu chưa tồn tại
    generate_self_signed_certificate(certfile, keyfile)

    # Tạo địa chỉ IP ảo nếu chưa tồn tại
    create_virtual_ip(SERVER_IP)

    # Khởi động server trong một thread riêng
    server_thread = threading.Thread(target=run_https_server, args=(SERVER_IP, HTTPS_PORT, html_dir, keyfile, certfile))
    server_thread.start()
