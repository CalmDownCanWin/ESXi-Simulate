import sqlite3
import datetime
from configure import DATABASE_FILE 

def generate_daily_report():
    """Tạo báo cáo thay đổi hệ thống file hàng ngày."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM changes
        WHERE timestamp >= date('now', '-1 day')
    ''')
    changes = cursor.fetchall()

    conn.close()

    if changes:
        with open("filesystem_changes_report.txt", "w") as f:
            f.write(f"Báo cáo thay đổi hệ thống file (ngày {datetime.date.today()} )\n")
            f.write("-" * 40 + "\n")
            for change in changes:
                f.write(f"Hành động: {change[1]}\n")
                f.write(f"Tên file: {change[2]}\n")
                f.write(f"Phần mở rộng: {change[3]}\n")
                f.write(f"Kích thước: {change[4]}\n")
                f.write(f"Hash: {change[5]}\n")
                f.write(f"Quyền truy cập: {change[6]}\n")
                f.write(f"Thời gian: {change[7]}\n")
                f.write("-" * 40 + "\n")
    else:
        print("Không có thay đổi nào trong hệ thống file ngày hôm nay.")