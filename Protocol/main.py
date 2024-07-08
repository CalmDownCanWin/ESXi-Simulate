import threading
from http_server import run_deception_server
from dcui_server import run_dcui_server
from ssh_server import run_ssh_server
from telnet_server import run_telnet_server
from syslog_server import run_syslog_server
from vmkernel_server import run_vmkernel_server

def run_all_servers():
    """Khởi động tất cả các dịch vụ giả mạo."""
    http_thread = threading.Thread(target=run_deception_server)
    dcui_thread = threading.Thread(target=run_dcui_server)
    ssh_thread = threading.Thread(target=run_ssh_server)
    telnet_thread = threading.Thread(target=run_telnet_server)
    syslog_thread = threading.Thread(target=run_syslog_server)
    vmkernel_thread = threading.Thread(target=run_vmkernel_server)

    http_thread.start()
    dcui_thread.start()
    ssh_thread.start()
    telnet_thread.start()
    syslog_thread.start()
    vmkernel_thread.start()

    print("Tất cả các dịch vụ giả mạo đã được khởi động.")

if __name__ == "__main__":
    run_all_servers()