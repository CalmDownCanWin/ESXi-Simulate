import threading
import time
import argparse

from Logs.Log_to_Splunk import log_event
from Services.ssh2 import run_ssh_server
from Services.openslp import run_openslp_server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', type=str, required=True, help='IP Address')
    args = parser.parse_args()

    # Khởi tạo luồng cho SSH server
    ssh_thread = threading.Thread(target=run_ssh_server, args=(args.address,))
    ssh_thread.daemon = True  # Cho phép chương trình kết thúc khi luồng này còn chạy
    ssh_thread.start()

    # Khởi tạo luồng cho OpenSLP server
    openslp_thread = threading.Thread(target=run_openslp_server, args=(args.address,))
    openslp_thread.daemon = True
    openslp_thread.start()

    # Duy trì luồng chính để chương trình không kết thúc ngay lập tức
    while True:
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_event(f"\nTerminated.....")