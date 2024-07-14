import sqlite3

DB_FILE = "honeypot.db"

def create_database():
    """Tạo database và các bảng nếu chưa tồn tại."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Bảng HTTP logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS http_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            method TEXT,
            path TEXT,
            query_params TEXT
        )
    """)

    # Bảng SSH logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ssh_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            command TEXT
        )
    """)

    # Bảng Telnet logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telnet_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            command TEXT
        )
    """)

    # Bảng DCUI logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dcui_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            username TEXT,
            password TEXT,
            command TEXT
        )
    """)

    # Bảng Syslog logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS syslog_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            message TEXT
        )
    """)

    # Bảng vMotion logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vmotion_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT
        )
    """)

    # Bảng iSCSI logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS iscsi_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT
        )
    """)
    # Bảng esxcli logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS esxcli_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            command TEXT
        )
    """)

    # Bảng vimcmd logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vimcmd_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            command TEXT
        )
    """)

    # Bảng vmdumper logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vmdumper_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            command TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filesystem_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            action TEXT,
            filename TEXT,
            size INTEGER,
            hash TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# Khởi tạo database khi module được import
create_database()