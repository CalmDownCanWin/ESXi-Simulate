import socket
import ssl
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from config import HTTP_PORT, FAKE_ESXI_INFO, SSL_CERT, SSL_KEY

class DeceptionHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def handle_request(self, method):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # Định nghĩa các route deception
        deception_routes = {
            "/api/host": self.deceive_host_api,
            # ... Thêm các route khác nếu cần thiết
        }

        handler = deception_routes.get(parsed_url.path)
        if handler:
            handler(method, query_params)
        else:
            self.send_error(404, "Not Found")

    def deceive_host_api(self, method, query_params):
        if method == "GET" and 'sensitive' in query_params:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(FAKE_ESXI_INFO).encode())  # Sử dụng FAKE_ESXI_INFO từ config
        else:
            self.send_error(403, "Access denied")

    # ... Thêm các function deception khác nếu cần thiết

class DeceptionHTTPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        # Sử dụng SSL/TLS
        self.socket = ssl.wrap_socket(self.socket, 
                                      server_side=True,
                                      certfile=SSL_CERT,  # Sử dụng SSL_CERT từ config
                                      keyfile=SSL_KEY)   # Sử dụng SSL_KEY từ config

def run_deception_server(port=HTTP_PORT):  # Sử dụng HTTP_PORT từ config
    """Khởi động HTTP server cho deception."""
    server_address = ('', port)
    httpd = DeceptionHTTPServer(server_address, DeceptionHTTPRequestHandler)
    print(f"Deception HTTP server đang lắng nghe trên cổng {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_deception_server()
