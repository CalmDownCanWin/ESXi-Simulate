import paramiko
import datetime
import os

def get_logs_from_esxi(host, username, password, log_files, output_dir="logs"):
    """Kết nối đến ESXi host, lấy các file log và lưu vào thư mục chỉ định."""

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for log_file in log_files:
            try:
                stdin, stdout, stderr = ssh.exec_command(f"cat {log_file}")
                log_content = stdout.read().decode()

                # Tạo tên file log dựa trên tên file gốc và thời gian hiện tại
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                output_filename = os.path.join(output_dir, f"{os.path.basename(log_file)}_{timestamp}.txt")

                with open(output_filename, "w", encoding="utf-8") as f:
                    f.write(log_content)

                print(f"Đã lưu log '{log_file}' vào '{output_filename}'")
            except Exception as e:
                print(f"Lỗi khi lấy log '{log_file}': {e}")

        ssh.close()
    except Exception as e:
        print(f"Lỗi kết nối đến ESXi host '{host}': {e}")

# Danh sách các file log bạn muốn lấy
log_files = [
    "/var/log/vmkernel.log",
    "/var/log/hostd.log",
    "/var/run/log/vpxa.log",
    # Thêm các file log khác nếu cần
]

# Thông tin kết nối đến ESXi host
esxi_host = "208.100.26.133"
esxi_username = "root"
esxi_password = "admin@123"

# Thư mục để lưu file log (mặc định là thư mục "logs" trong thư mục hiện tại)
output_directory = "logs"

get_logs_from_esxi(esxi_host, esxi_username, esxi_password, log_files, output_directory)