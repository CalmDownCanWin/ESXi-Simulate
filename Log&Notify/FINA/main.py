from filesystem_monitor import monitor_filesystem
from db import create_database, log_filesystem_change
from Report import generate_daily_report

def main():
    """Hàm chính điều khiển chương trình."""
    create_database()
    for change in monitor_filesystem():
        log_filesystem_change(change['action'], change['details'])
        # Xử lý thay đổi ở đây, ví dụ: gửi email, ghi log chi tiết hơn,...
    generate_daily_report()

if __name__ == "__main__":
    main()