import os

# === CẤU HÌNH SSH ===
SSH_PORT = 2222
HONEYPOT_ROOT = "/home/test/Desktop/ESXI 7/"

# Thông tin đăng nhập
VALID_USERS = {
    "root": "root", # Thay đổi mật khẩu mặc định
    "admin": "AnotherStrongPassword2@", # Thay đổi mật khẩu mặc định
    "user": "EvenStrongerPassword3#" # Thay đổi mật khẩu mặc định
}

# Đường dẫn đến khóa RSA (bảo mật thông tin này!)
RSA_PUB_KEY_PATH = "/home/test/Desktop/TEST/abc.pub"
RSA_KEY_PATH = "/home/test/Desktop/TEST/abc"

# SSH Banner - Mô phỏng ESXi
SSH_BANNER = b"SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.5"

# Tự động lấy SSH Fingerprint từ khóa RSA
from utils import get_ssh_fingerprint_from_file
SSH_FINGERPRINT = get_ssh_fingerprint_from_file(RSA_KEY_PATH)

# === CẤU HÌNH GHI LOG ===
LOG_ROOT = "/home/test/Desktop/FINAL_X5/HONEYPOT/"
FILE_LOG_DIR = os.path.join(LOG_ROOT, "files")
MAX_QUEUE_SIZE = 10000

# === CẤU HÌNH THÔNG BÁO EMAIL ===
ADMIN_EMAIL = "your_email@example.com"  # Thay bằng địa chỉ email của bạn
SMTP_SERVER = "smtp.example.com"  # Thay bằng máy chủ SMTP của bạn
SMTP_PORT = 587
SMTP_USERNAME = "your_username"  # Nếu cần
SMTP_PASSWORD = "your_password"  # Nếu cần

# === CẤU HÌNH RANSOMWARE ===
ENABLE_RANSOMWARE_DETECTION = True
RANSOMWARE_HASH_DB = {
    # Cập nhật cơ sở dữ liệu hash ransomware thường xuyên
    "84c82835a5d21bbcf75a8170f4f0d29554d4d2e2e74136c3ea97ce8b340ff0d0": "WannaCry",
    "344166b234848c23b4a6e3c53c09e37239b1386f9b6c32442a2ab06360316362": "Locky",
    "3b9662c551095757412198449f5286642378a6a460f0279411937612387127a1": "Petya",
    "49c18c3a9c45c1789c5b9d53a127a8a6093252afa401728a7a245e70b8274301": "Cerber",
    "44d88612fea8a8f36de82e1278abb02f7b94d72806858a0789ec5d71d39a8b1f": "CryptoLocker",
    "7846f839530d1897c398b94614c50d1687d41099884f2ddb9c917455597759ed": "GandCrab",
    "d79617465c2572b480194550752b478a60d758e740807a4b4f8705f3df1030d0": "Ryuk",
    "9fc5e56e338411a42a3966c6366018317448d8ee091802f138a4171493f8b2f1": "REvil (Sodinokibi)",
    "414c42c1476067623f99732a4980f1680a4064c1b7a7633150c30b88455038d7": "Maze",
    "0932277431b475a32e195757412198449f5286642378a6a460f0279411937612": "Netwalker",
    # ...
}

# === CẤU HÌNH GIÁM SÁT FILE ===
SENSITIVE_DIRS = [
    os.path.join(HONEYPOT_ROOT, "etc"),
    os.path.join(HONEYPOT_ROOT, "var/log"),
    os.path.join(HONEYPOT_ROOT, "vmfs/volumes") # Thư mục chứa máy ảo
]

IGNORE_PATTERNS = [
    ".goutputstream-",
    ".swp",
    "*.save"
]

ACCESS_THRESHOLD = 5

# === NGƯỠNG ENTROPY ===
ENTROPY_THRESHOLDS = {
    "default": {
        "normal": 6.0,
        "suspicious": 7.0 
    },
    ".txt": {
        "normal": 5.0,
        "suspicious": 7.0
    },
    ".doc": {
        "normal": 5.0,
        "suspicious": 7.0
    },
    ".docx": {
        "normal": 7.0,
        "suspicious": 7.5
    },
    ".pdf": {
        "normal": 5.0,
        "suspicious": 7.0
    },
    ".jpg": {
        "normal": 7.0,
        "suspicious": 7.5
    },
    ".png": {
        "normal": 7.0,
        "suspicious": 7.5
    },
    ".exe": {
        "normal": 6.0,
        "suspicious": 7.5
    },
    # ... (Thêm các loại file khác và ngưỡng entropy tương ứng) ...
}

# === CẤU HÌNH SPLUNK ===
SPLUNK_HOST = "208.100.26.134"
SPLUNK_PORT = 514

# === CẤU HÌNH MỨC ĐỘ GHI LOG VÀ BẢO MẬT ===
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
SECURE_LOG_ENABLED = False  # Bật TLS cho kết nối Splunk
TLS_CERT_PATH = "path/to/your/cert.pem"  # Đường dẫn đến chứng chỉ TLS (nếu SECURE_LOG_ENABLED)
TLS_KEY_PATH = "path/to/your/key.pem"  # Đường dẫn đến khóa TLS (nếu SECURE_LOG_ENABLED)

# === CẤU HÌNH GHI LOG THEO MỨC ĐỘ NGUY HIỂM ===
LOG_CONFIG = {
    "NORMAL": {
        "file_path": os.path.join(FILE_LOG_DIR, "normal_logs.json"),
        "splunk_enabled": False,
        "email_enabled": False
    },
    "WARNING": {
        "file_path": os.path.join(FILE_LOG_DIR, "warning_logs.json"),
        "splunk_enabled": True,
        "email_enabled": False
    },
    "DANGEROUS": {
        "file_path": os.path.join(FILE_LOG_DIR, "attack_logs.json"),
        "splunk_enabled": True,
        "email_enabled": True
    }
}