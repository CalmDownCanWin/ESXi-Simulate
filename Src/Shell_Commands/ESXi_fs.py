import os
import shutil

class FileNotFoundError(Exception):
    pass

class FileExistsError(Exception):
    pass

class SimpleFS:
    def __init__(self, root="/"):
        self.root = root
        self.cwd = root
        self.files = {} 
        self.files["/"] = {"type": "dir", "contents": []}

    def chdir(self, path):
        new_path = self.resolve_path(path)

        # root path
        new_path = os.path.abspath(new_path)

        # sub-dir
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
        """resolve path on root."""
        if path.startswith("/") and not os.path.exists(path):
            # check /path
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

    def mkfile(self, path, uid=0, gid=0, size=0, mode=33188): 
        """new file"""
        path = self.resolve_path(path)
        if not self.exists(path):
            self.files[path] = {"type": "file", "uid": uid, "gid": gid, "size": size, "mode": mode}
            parent_dir = os.path.dirname(path)
            if parent_dir != path:
                self.files[parent_dir]["contents"].append(os.path.basename(path))
        else:
            raise FileExistsError

    def write_file(self, filename, content):
        with open(self.resolve_path(filename), "wb") as f:
            f.write(content)
    
    def update_realfile(self, filename, real_file):
        pass
        

