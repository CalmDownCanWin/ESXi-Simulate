# Cổng cho các dịch vụ
SSH_PORT = 2222
#HTTP_PORT = 8080
TELNET_PORT = 2323
DCUI_PORT = 5900
SYSLOG_PORT = 514
VMOTION_PORT = 8000  
ISCSI_PORT = 3261   


# Banner giả mạo (sử dụng banner ESXi thật nếu có thể)
SSH_BANNER = b"SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.5\r\n"
TELNET_BANNER = b"Ubuntu 20.04.1 LTS\n"
DCUI_BANNER = b"""
DCUI: VMware ESXi 6.5.0 (Build 5969303)
"""

# Thông tin ESXi giả mạo
FAKE_ESXI_INFO = {
    "hostname": "esxi-honeypot.local",
    "version": "6.7.0",
    "build": "14320388",
    # ... thêm thông tin giả mạo khác
}

# Địa chỉ và cổng của SOC server
SOC_HOST = "127.0.0.1"
SOC_PORT = 5000

HTTP_PORT = 8443
FAKE_ESXI_INFO = {
    "hostname": "fake-esxi.local",
    "version": "7.0",
    "uptime": "1024 hours",
    "datastores": ["datastore1", "datastore2"]
}
SSL_CERT = "/home/iaw301/certificate.pem"  # Đường dẫn tới file chứng chỉ SSL tự ký
SSL_KEY = "/home/iaw301/privatekey.pem"    # Đường dẫn tới file khóa riêng SSL tự ký
