import threading
import time
from filesystem_monitor import monitor_filesystem
from db import create_database  # Import hàm tạo database

# --- Tùy chọn ---
ENABLE_LOG_MONITORING = False 
STOP_MONITORING = False  

def show_menu():
    """Hiển thị menu tùy chọn."""
    print("\n--- Menu ---")
    print("1. Bật/Tắt theo dõi log")
    print("2. Thoát")

def handle_choice(choice):
    """Xử lý lựa chọn từ menu."""
    global ENABLE_LOG_MONITORING, STOP_MONITORING

    if choice == '1':
        ENABLE_LOG_MONITORING = not ENABLE_LOG_MONITORING
        print(f"Theo dõi log: {'Bật' if ENABLE_LOG_MONITORING else 'Tắt'}")
        if ENABLE_LOG_MONITORING:
            # Khởi động lại thread nếu được bật lại
            monitor_thread = threading.Thread(target=monitor_filesystem)
            monitor_thread.daemon = True
            monitor_thread.start()
        else:
            # Dừng theo dõi nếu tắt
            STOP_MONITORING = True
    elif choice == '2':
        print("Thoát chương trình...")
        STOP_MONITORING = True
        # Đợi thread theo dõi kết thúc (nếu đang chạy)
        if ENABLE_LOG_MONITORING:
            monitor_thread.join()
        exit()
    else:
        print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    # Tạo database
    create_database()

    # Khởi tạo thread theo dõi file system (nếu được bật)
    if ENABLE_LOG_MONITORING:
        monitor_thread = threading.Thread(target=monitor_filesystem)
        monitor_thread.daemon = True
        monitor_thread.start()

    # Vòng lặp menu
    while True:
        show_menu()
        choice = input("Nhập lựa chọn của bạn: ")
        handle_choice(choice)
        time.sleep(1)