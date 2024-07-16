import sqlite3

DB_FILE = "honeypot.db"

def create_table(conn, create_table_sql):
    """Tạo bảng trong database."""
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Exception as e:
        print(f"Lỗi khi tạo bảng: {e}")

def create_database():
    """Tạo database và các bảng nếu chưa tồn tại."""
    conn = sqlite3.connect(DB_FILE)

    # Tạo các bảng log
    create_table(conn, """
        CREATE TABLE IF NOT EXISTS http_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            method TEXT,
            path TEXT,
            query_params TEXT
        )
    """)
    create_table(conn, """
        CREATE TABLE IF NOT EXISTS ssh_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            command TEXT
        )
    """)
    create_table(conn, """
        CREATE TABLE IF NOT EXISTS telnet_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            command TEXT
        )
    """)
    create_table(conn, """
        CREATE TABLE IF NOT EXISTS dcui_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            username TEXT,
            password TEXT,
            command TEXT
        )
    """)
    create_table(conn, """
        CREATE TABLE IF NOT EXISTS syslog_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            message TEXT
        )
    """)
    create_table(conn, """
        CREATE TABLE IF NOT EXISTS vmotion_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT
        )
    """)
    create_table(conn, """
        CREATE TABLE IF NOT EXISTS iscsi_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT
        )
    """)
    create_table(conn, """
        CREATE TABLE IF NOT EXISTS esxcli_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            command TEXT
        )
    """)
    create_table(conn, """
        CREATE TABLE IF NOT EXISTS vimcmd_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            command TEXT
        )
    """)
    create_table(conn, """
        CREATE TABLE IF NOT EXISTS vmdumper_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            command TEXT
        )
    """)
    create_table(conn, """
        CREATE TABLE IF NOT EXISTS filesystem_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            action TEXT,
            filename TEXT,
            size INTEGER,
            hash TEXT,
            permissions TEXT,
            previous_permissions TEXT,
            previous_size INTEGER,
            previous_hash TEXT
        )
    """)

    conn.close()

# Khởi tạo database khi module được import
create_database()