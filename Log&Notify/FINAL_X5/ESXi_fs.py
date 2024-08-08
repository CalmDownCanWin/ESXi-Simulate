import os
import shutil

class FileNotFoundError(Exception):
    pass

class SimpleFS:
    def __init__(self, root="/"):
        self.root = root
        self.cwd = root

    def chdir(self, path):
        new_path = self.resolve_path(path)

        # Sử dụng os.path.abspath để đơn giản hóa đường dẫn
        new_path = os.path.abspath(new_path)

        # Kiểm tra new_path có phải là thư mục con của root hay không
        real_root = os.path.realpath(self.root)
        real_new_path = os.path.realpath(new_path)
        if not real_new_path.startswith(real_root):
            self.cwd = self.root
            return
        if os.path.isdir(real_new_path):
            self.cwd = new_path
        else:
            raise FileNotFoundError

    def getcwd(self):
        return self.cwd

    def listdir(self, path):
        path = self.resolve_path(path)
        if os.path.isdir(path):
            return os.listdir(path)
        else:
            raise FileNotFoundError

    def open(self, filename, mode):
        path = self.resolve_path(filename)
        return open(path, mode)

    def resolve_path(self, path):
        """Phân giải đường dẫn dựa trên root."""
        if path.startswith("/") and not os.path.exists(path):
            # Nếu là đường dẫn tuyệt đối KHÔNG tồn tại trên hệ thống thật, 
            # coi đó là đường dẫn trong filesystem giả lập.
            path = os.path.join(self.root, path[1:]) 
        else:
            path = os.path.join(self.cwd, path)
        return os.path.normpath(path)
        
    def exists(self, path):
        return os.path.exists(self.resolve_path(path))

    def isfile(self, path):
        return os.path.isfile(self.resolve_path(path))

    def isdir(self, path):
        return os.path.isdir(self.resolve_path(path))

    def remove(self, path):
        path = self.resolve_path(path)
        if os.path.isfile(path):
            os.remove(path)
        else:
            raise FileNotFoundError

    def mkdir(self, path):
        os.mkdir(self.resolve_path(path))

    def rmdir(self, path):
        os.rmdir(self.resolve_path(path))

    def copy(self, source, destination):
        source = self.resolve_path(source)
        destination = self.resolve_path(destination)
        if os.path.isfile(source):
            shutil.copy2(source, destination)
        elif os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            raise FileNotFoundError

    def rename(self, old_path, new_path):
        os.rename(self.resolve_path(old_path), self.resolve_path(new_path))

    def write_file(self, filename, content):
        """
        Ghi nội dung vào file.
        """
        with open(self.resolve_path(filename), "wb") as f:
            f.write(content)
    
    def update_realfile(self, filename, real_file):
        """
        Cập nhật real file cho file trong honeypot.
        """
        # Không thực hiện gì trong simple_fs
        pass
        

