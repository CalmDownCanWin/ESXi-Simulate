import os

# Cấu hình thư mục log
FILE_LOG_DIR = "logs"

# Cấu hình giám sát
ESXI_ROOT = "/home/test/Desktop/ESXI 7/"  # Thay đổi đường dẫn tới thư mục ESXi của bạn
SERVICES_TO_MONITOR = ["hostd", "vpxa", "ssh"]

# Cấu hình Splunk (UDP)
SPLUNK_HOST = os.environ.get("SPLUNK_HOST", None)  # Địa chỉ IP Splunk server
SPLUNK_PORT = int(os.environ.get("SPLUNK_PORT", 514))  # Port Splunk

# Cấu hình chung
MAX_QUEUE_SIZE = 10000

IGNORE_PATTERNS = [".goutputstream-*", "*.swp", "*.tmp"]  # Danh sách pattern cần bỏ qua