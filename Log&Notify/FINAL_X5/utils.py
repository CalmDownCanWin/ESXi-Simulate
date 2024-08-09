import logging
import paramiko
import os
import json
import socket
import time
import hashlib
import difflib
import math
import zlib
from collections import defaultdict

def log_event(message, level=logging.INFO):
    # Log the event with the specified logging level
    if level == logging.DEBUG:
        logging.debug(message)
    elif level == logging.WARNING:
        logging.warning(message)
    elif level == logging.ERROR:
        logging.error(message)
    else:
        logging.info(message)

def get_ssh_fingerprint_from_file(key_path):
    """Lấy fingerprint từ file RSA key."""
    try:
        key = paramiko.RSAKey.from_private_key_file(key_path)
        fingerprint = key.get_fingerprint().hex(':')  
        return fingerprint
    except Exception as e:
        logging.error(f"[!] Lỗi khi lấy fingerprint từ file: {e}")
        return None
    
def check_ransomware_hash(file_hash, ransomware_hash_db):
    """Kiểm tra hash của file trong cơ sở dữ liệu ransomware."""
    if file_hash in ransomware_hash_db:
        return True, ransomware_hash_db[file_hash]
    return False, None

def get_file_diff(filepath1, filepath2):
    """So sánh hai file và trả về nội dung khác biệt."""
    try:
        with open(filepath1, 'r') as file1, open(filepath2, 'r') as file2:
            diff = difflib.unified_diff(file1.readlines(), file2.readlines(), lineterm='')
            return list(diff)
    except (FileNotFoundError, PermissionError) as e:
        return [f"Error: {e}"]


def calculate_file_hash(self, filepath):
    """
    Calculates the SHA256 hash of a file.
    """
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def calculate_entropy(self, filepath):
    """
    Calculates the Shannon entropy of a file.
    """
    with open(filepath, 'rb') as f:
        data = f.read()
    if not data:
        return 0.0
    byte_counts = defaultdict(lambda: 0)
    for byte in data:
        byte_counts[byte] += 1
    total_bytes = len(data)
    entropy = 0.0
    for count in byte_counts.values():
        probability = count / total_bytes
        entropy -= probability * math.log2(probability)
    return entropy


def calculate_file_checksum(filename, algorithm="crc32"):
    """Calculate file checksum."""
    hash_obj = zlib.crc32 if algorithm == "crc32" else hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def is_potential_ransomware(self, filepath):
    """
    Checks if the file is a potential ransomware executable.
    """
    # Check based on file extension (add more extensions as needed)
    if filepath.lower().endswith((".exe", ".dll", ".scr", ".pif")):
        return True

    # Check based on entropy (adjust threshold if needed)
    entropy = self.calculate_entropy(filepath)
    if entropy > 7.5:  # High entropy might indicate potential executable
        return True

    return False

def is_file_encrypted(self, filepath):
    """
    Checks if the file is encrypted (basic check).
    """
    # Check if the file size is significantly reduced compared to the original size
    original_size = self.file_info.get(filepath, {}).get("size")
    if original_size:
        current_size = os.path.getsize(filepath)
        if current_size < original_size * 0.1:  # 10% reduction in size might indicate encryption
            return True

    # Implement more robust encryption detection methods here (e.g., checking for known encryption algorithms)
    return False


def DisconnectException(Exception):
    pass
   
def disconnect_attacker():
    raise DisconnectException()

# Thêm hàm `sizeof_fmt` để hiển thị kích thước file theo định dạng dễ đọc
def sizeof_fmt(num: float) -> str:
    for x in ["bytes", "K", "M", "G", "T"]:
        if num < 1024.0:
            return f"{num:.1f}{x}"
        num /= 1024.0
    return f"{num:.1f}P" # Nếu lớn hơn 1024 TB, hiển thị đơn vị PB