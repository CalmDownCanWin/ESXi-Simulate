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
        if path == ".." and self.cwd != self.root:  # Xử lý "cd .."
            self.cwd = os.path.dirname(self.cwd)
        elif os.path.isdir(new_path) and new_path.startswith(self.root):  # Giới hạn truy cập
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
        if path.startswith("/"):
            return path
        else:
            return os.path.join(self.cwd, path)

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
