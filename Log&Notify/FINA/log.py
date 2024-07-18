import sqlite3
import datetime 

def log_filesystem_change(action, details):
    """Ghi log thay đổi hệ thống file vào database SQLite."""
    conn = sqlite3.connect('filesystem_changes.db')
    cursor = conn.cursor()

    filename = details.get('filename', 'N/A')
    extension = details.get('extension', 'N/A')
    size = details.get('size', 'N/A')
    hash = details.get('hash', 'N/A')
    permissions = details.get('permissions', 'N/A')

    cursor.execute('''
        INSERT INTO changes (action, filename, extension, size, hash, permissions, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (action, filename, extension, size, hash, permissions, datetime.datetime.now()))

    conn.commit()
    conn.close()