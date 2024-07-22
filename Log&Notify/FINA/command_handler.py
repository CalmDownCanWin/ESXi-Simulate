# from file_folder import list_files, read_file

def handle_command(command, protocol, address):
    # ...
    if command == "ls":
        # files = list_files("/tmp")
        # return "  ".join(files) + "\r\n"
        return "  file1.txt  directory1\r\n"  # Trả về kết quả giả định
    elif command.startswith("cat"):
        # filepath = command.split(" ")[1]
        # return read_file(filepath) + "\r\n"
        return "Nội dung file giả mạo\r\n"  # Trả về kết quả giả định
    # ...
