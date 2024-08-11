import sqlite3
from datetime import datetime, timedelta

DATABASE_FILE = 'filesystem_changes.db'  # Tên file database

def generate_daily_report():
    """Tạo báo cáo thay đổi trong vòng 24h qua."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Lấy thời gian 24h trước
    twenty_four_hours_ago = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%S')
    
    cursor.execute(
        '''
        SELECT * FROM changes
        WHERE timestamp >= ?
        ''',
        (twenty_four_hours_ago,)
    )
    changes = cursor.fetchall()
    conn.close()

    print("=== Báo cáo thay đổi hệ thống file ===")
    print(f"Từ: {twenty_four_hours_ago} đến hiện tại\n")
    
    if changes:
        for change in changes:
            print(f"Thời gian: {change[1]}")
            print(f"Hành động: {change[2]}")
            print(f"Đường dẫn: {change[3]}")
            print(f"Chi tiết: {change[4]}\n")
    else:
        print("Không có thay đổi nào được ghi nhận.")