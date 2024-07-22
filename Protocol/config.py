# Cấu hình cho mô phỏng SSH
# Cổng SSH
SSH_PORT = 22
TELNET_PORT = 23
SYSLOG_PORT = 514
DCUI_PORT = 5901
# Người dùng hợp lệ và mật khẩu tương ứng
VALID_USERS = {
    "root": "root",
    "admin": "adminpassword",
    "user": "userpassword"
}
# ... (Các cấu hình khác)
# ... (Các cấu hình khác)

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

