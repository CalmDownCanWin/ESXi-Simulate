import ESXi_fs as fs
import ESXi_command as cmd

import error_handler as er

import re
import shlex 
import random
import time
import os 



    # Dictionary for patterns
SUSPICIOUS_PATTERNS = [
     "esxcli", "vim-cmd", "vmdumper", "find", "ls", "mv", "cp", "tar", "touch", "rm"
]

class ESXiShCommand(cmd.SimpleCommand):
    """
    /bin/sh
    """

    def run(self):
        if self.check_arguments(1):
            script_file = self.args[0]
        try:
            # Check
            if not self.fs.isfile(script_file):
                self.stderr = f"-sh: {script_file}: not found"
                self.returncode = 127
                return
            with self.fs.open(script_file, "r") as f:
                    script = f.read()

            time.sleep(0.5)

            # Analyze script
            matched_pattern, target_path, encrypt_extension = self.analyze_script(script)

            if matched_pattern:
                # Create Fake file
                if target_path and encrypt_extension:
                    print("encrypting!")
                    self.create_fake_encrypted_files(target_path, encrypt_extension)
                elif target_path is None and encrypt_extension:
                    target_path = '/'
                    print("encrypting!")
                    self.create_fake_encrypted_files(target_path, encrypt_extension)
                else:
                    self.stderr = er.Error()
                    self.returncode = 1
            else:
                # Fake Error
                self.stderr = er.Error()
                self.returncode = 1

        
        except (PermissionError) as e:
            if isinstance(e, PermissionError):    
                er.Permission_Denied(script_file)


    def analyze_script(self, script):
        """Analyze for finding command, path, extension"""
        matched_command = set()
        target_path = None
        encrypt_extension = None

        delay = random.uniform(3, 7) 
         

        for line in script.splitlines():
            for command in SUSPICIOUS_PATTERNS:
                if command in line:
                    matched_command.add(command)
                    print("Warning!!! Suspicious_Command Found")
                    #time.sleep(delay)
                    

        if "find" in matched_command:  
            for line in script.splitlines():
                if "find" in line:
                    target_path = self.analyze_find_command(line) 
                    if target_path: 
                        break

        if "mv" in matched_command or "cp" in matched_command:
            for line in script.splitlines():
                if "mv" in line or "cp" in line:
                    _, encrypt_extension = self.analyze_mv_cp_command(line)
                    if encrypt_extension:
                        break
        
        if "touch" in matched_command and not encrypt_extension:
            for line in script.splitlines():
                if "touch" in line:
                    encrypt_extension = self.analyze_touch_command(line)
                    if encrypt_extension:
                        break

        if any(cmd in matched_command for cmd in ["esxcli", "vim-cmd", "vmdumper", "tar", "touch", "rm"]):
            for line in script.splitlines():
                if any(cmd in line for cmd in ["esxcli", "vim-cmd", "vmdumper", "tar", "touch", "rm"]):
                    target_path = self.analyze_path_command(line)
                    if target_path:
                        break


        print(f"Target Path: {target_path}")
        print(f"Encrypt Extension: {encrypt_extension}")

        return matched_command, target_path, encrypt_extension
    
    def analyze_find_command(self, line):
        target_path = None
        match = re.search(r"find\s+(.+?)\s", line)
        if match:
            target_path = match.group(1).strip()
        
        return target_path

    def analyze_mv_cp_command(self, line):
        target_path = None
        encrypt_extension = None
        match = re.search(r"(mv|cp)\s+(.+?)\s+(.+)", line)
        if match:
            target_path = match.group(2).strip() 
            encrypt_extension = os.path.splitext(match.group(3).strip())[1][1:].replace('"','') 
        return target_path, encrypt_extension
    
    def analyze_touch_command(self, line):
        encrypt_extension = None
        match = re.search(r"touch\s+\"(.+?)\"", line)
        if match:
            filename = match.group(1).strip()
            encrypt_extension = os.path.splitext(filename)[1][1:].replace('"','') 
        return encrypt_extension

    def analyze_path_command(self, line):
        target_path = None
        match = re.search(r"(/\S+)", line) 
        if match:
            target_path = match.group(1).strip()
        return target_path


    def create_fake_encrypted_files(self, target_path, encrypt_extension):
        """Fake file.encrypted_extension in target_path"""
        common_targets = ["/vmfs/volumes", "/var/log", "/etc"] 

        if target_path == "/":
            for target_dir in common_targets:
                if target_dir == '/vmfs/volumes':
                    if self.fs.isdir(target_dir):
                        for datastore in self.fs.listdir(target_dir):
                            datastore_path = os.path.join(target_dir, datastore)
                            if self.fs.isdir(datastore_path):
                                for vm_folder in self.fs.listdir(datastore_path):
                                    vm_name = os.path.join(datastore_path, vm_folder)
                                    if self.fs.isdir(vm_name):
                                        for vm_file in self.fs.listdir(vm_name):
                                            fake_file = os.path.join(vm_name,vm_file) + f".{encrypt_extension}"
                                            self.fs.rename(os.path.join(vm_name, vm_file), fake_file)
                                            print(f"encrypted files in {target_dir}")
                else:
                    if self.fs.isdir(target_dir):
                        for filename in self.fs.listdir(target_dir):
                            fake_file = os.path.join(target_dir, filename) + f".{encrypt_extension}"
                            self.fs.rename(os.path.join(target_dir,filename), fake_file)
                            print(f"encrypted files in {common_targets}")

        elif self.fs.isdir(target_path):
            for datastore in self.fs.listdir(target_path):
                datastore_path = os.path.join(target_path, datastore)
                if self.fs.isdir(datastore_path):
                    for vm_folder in self.fs.listdir(datastore_path):
                        vm_name = os.path.join(datastore_path, vm_folder)
                        if self.fs.isdir(vm_name):
                            for vm_file in self.fs.listdir(vm_name):
                                fake_file = os.path.join(vm_name,vm_file) + f".{encrypt_extension}"
                                self.fs.rename(os.path.join(vm_name, vm_file), fake_file)
                                print(f"encrypted files in {target_path}")

        elif self.fs.isfile(target_path):
            fake_file = target_path + f".{encrypt_extension}"
            self.fs.rename(target_path, fake_file) 
            print("encrypted files!")

        else:
            print("nothing!")
            pass