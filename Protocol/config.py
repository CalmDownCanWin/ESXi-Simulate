# Cấu hình cho mô phỏng SSH
OPENSLP_PORT = 427
SERVER_IP = "192.168.79.133"
# Cổng SSH


TELNET_PORT = 23
SYSLOG_PORT = 514
HTTPS_PORT = 443

#ssh
#INTERFACE = "eth0"
# Người dùng hợp lệ và mật khẩu tương ứng
SSH_PORT = 22
VALID_USERS = {
    "root": "root",
    "admin": "adminpassword",
    "user": "userpassword"
}
# ... (Các cấu hình khác)
# ... (Các cấu hình khác)

SERVER_BANNER = b"""The time and date of this login have been sent to the system logs.\r

WARNING:\r
   All commands run on the ESXi shell are logged and may be included in\r
   support bundles. Do not provide passwords directly on the command line.\r
   Most tools can prompt for secrets or accept them from standard input.\r

VMware offers supported, powerful system administration tools.  Please\r
see www.vmware.com/go/sysadmintools for details.\r

The ESXi Shell can be disabled by an administrative user. See the\r
vSphere Security documentation for more information.\r"""
LOG_ROOT = ""
# Đường dẫn đến RSA key pub
RSA_PUB_KEY_PATH = "test_rsa.key.pub"  # Thay đổi đường dẫn nếu cần

# Đường dẫn đến RSA key
RSA_KEY_PATH = "test_rsa.key"  # Thay đổi đường dẫn nếu cần

# SSH Banner
SSH_BANNER = b"SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.5"

# SSH Fingerprint (lấy từ file RSA key)
from utils import get_ssh_fingerprint_from_file
SSH_FINGERPRINT = get_ssh_fingerprint_from_file(RSA_KEY_PATH)

# Telnet banner giả mạo
TELNET_BANNER =  b"SSH-2.0-OpenSSH_8.8\r\n"

TEMPLATE_FOLDER = "templates"
STATIC_FOLDER = "static"

POC_DATABASE = {
    "ESXiArgs": {
        "signature": "'arg1' : b'127.0.0.1'",  # Chuỗi đặc trưng trong request
    },
    # Thêm các PoC khác vào đây
}
