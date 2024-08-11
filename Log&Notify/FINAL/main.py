import threading
from file_monitor import monitor_files
from service_monitor import monitor_services

if __name__ == "__main__":
    threading.Thread(target=monitor_files).start()
    threading.Thread(target=monitor_services).start() 