import sqlite3
import datetime
from configure import DATABASE_FILE_SYSTEM

def create_database():
    """Tạo database và bảng nếu chưa tồn tại."""
    conn = sqlite3.connect(DATABASE_FILE_SYSTEM)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            filename TEXT,
            extension TEXT,
            size INTEGER,
            hash TEXT,
            permissions TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_filesystem_change(action, details):
    """Ghi log thay đổi hệ thống file vào database SQLite."""
    conn = sqlite3.connect(DATABASE_FILE_SYSTEM)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO changes (action, filename, extension, size, hash, permissions, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (action, details.get('filename'), details.get('extension'), details.get('size'), 
          details.get('hash'), details.get('permissions'), datetime.datetime.now()))

    conn.commit()
    conn.close()