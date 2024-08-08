import os
import random
import string
import datetime
import uuid
import subprocess
import shutil

def generate_random_string(length):
    """Create a random character series."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def create_config_file(path, filename, content):
    """Create a configuration file with random content. """
    # Create folders if not existed
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as f:
        f.write(content)

def create_directory(path):
  try:
    os.makedirs(path, exist_ok=True)  
  except OSError as e:
    print(f"Error when creating folders:{e}")


def create_hosts_file(path):
    """Create fake file /etc /hosts."""
    content = """
    127.0.0.1 localhost
    ::1 localhost ip6-localhost ip6-loopback
    192.168.1.100   esx-host-name
    Use code with caution.
    ff02::1 ip6-allnodes
    ff02::2 ip6-allrouters

    # IMPORTANT: Do not modify this file!
    # This file is managed by vCenter Server. 
    # Any changes will be overwritten.
    """

    # Add more fake items
    for _ in range(5): 
        fake_ip = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        fake_hostname = f"fake-server-{generate_random_string(5)}.corp"
        content += f"\n{fake_ip} {fake_hostname}"  

    # Important service simulation
    fake_services = {
        "vcenter": "10.10.10.11",
        "backup-server": "10.10.10.12",
        "domain-controller": "10.10.10.13"
    }
    for name, ip in fake_services.items():
        content += f"\n{ip} {name}.internal" 

    create_config_file(path, "hosts", content)

def create_fake_datastore(base_path, datastore_name,size_gb):
    """Simulate the Datastore by creating folders and files. """
    datastore_path = os.path.join(base_path, "vmfs", "volumes", datastore_name)
    os.makedirs(datastore_path, exist_ok=True)
    # Check if there is a file in Datastore_path directory
    if os.listdir(datastore_path):
        return 
    filename = str(uuid.uuid4())  #Create random uuid
    with open(os.path.join(datastore_path, filename), 'w') as f:
        f.write(f"Fake Size: {size_gb} GB\n")  # More fake size information

def create_sshd_config(path, fake_port=None, allowed_ips=None):
    """Create file/etc/ssh/sshd_config."""
    content = f"""
    # Fake SSHD Config - Version 7.0.3.1 (Deception)
    # running from inetd

    Port {fake_port if fake_port else 22}
    HostKey /etc/ssh/ssh_host_rsa_key
    HostKey /etc/ssh/ssh_host_ecdsa_key

    # Fips mode restricts ciphers (Deception - Weakened Security)
    FipsMode no 

    # Fake rekey values
    RekeyLimit 5G, 2H

    SyslogFacility auth
    LogLevel info

    # Deception - Allow root login 
    PermitRootLogin yes

    PrintMotd yes

    TCPKeepAlive yes

    # Key algorithms (Deception - Older, potentially weaker algorithms)
    KexAlgorithms diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
    HostKeyAlgorithms ssh-rsa,ssh-dss
    Ciphers aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,arcfour
    MACs hmac-md5,hmac-sha1

    # Deception - PAM disabled, PasswordAuthentication enabled
    UsePAM no
    PasswordAuthentication yes

    Banner /etc/issue.fake # File không tồn tại

    # Fake subsystem path
    Subsystem sftp /usr/lib/openssh/sftp-server.fake

    AuthorizedKeysFile /etc/ssh/keys-%u/authorized_keys

    # Timeout values (Deception - Increased timeouts)
    ClientAliveCountMax 5
    ClientAliveInterval 300

    # Fake connection limits
    MaxStartups 5:15:50

    # Forwarding options (Deception - Allowed for interaction)
    AllowTcpForwarding yes
    AllowStreamLocalForwarding yes 

    IgnoreRhosts yes
    HostbasedAuthentication no
    PermitEmptyPasswords no
    PermitUserEnvironment no
    StrictModes yes
    Compression no
    GatewayPorts no
    X11Forwarding no
    # AcceptEnv
    PermitTunnel no

    # The settings are disabled when Build OpenSSH:
    #GSSAPIAuthentication no
    #KerberosAuthentication no 
    """

    if allowed_ips:
        content += "\nAllowUsers " + " ".join(allowed_ips)  # IP access limit
    create_config_file(path, "sshd_config", content)

def create_vmware_lic(path):
    """Create file /etc/vmware/vmware.lic."""
    license_key = generate_random_string(32)
    expiry_date = (datetime.datetime.now() + datetime.timedelta(days=365*10)).strftime("%Y-%m-%d") # 10 years later
    callback_url = "http://your-server.com/collect_ransomware_data?id=12345" # Information collection
    content = f"""
    # VMware ESXi License
    LICENSE={license_key}
    FEATURES=vSphere,vMotion,vSAN,NSX,vCenter,vCloud
    VERSION=ESXi 7.0 Update 3 (Build 19482537)
    EXPIRY={expiry_date}

    # Deception Information (Ẩn)
    CALLBACK_URL={callback_url}
    """
    create_config_file(path, "vmware.lic", content)
    
def create_ssh_keys(path):
    """Create fake SSH key files (if not exist)."""
    os.makedirs(path, exist_ok=True)

    rsa_key_path = f"{path}/ssh_host_rsa_key"
    ecdsa_key_path = f"{path}/ssh_host_ecdsa_key"

    #Check if the key has existed
    if not (os.path.exists(rsa_key_path) and os.path.exists(ecdsa_key_path)):
        # Create RSA Key
        subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", rsa_key_path, "-N", ""], check=True)
        #Create ECDSA Key
        subprocess.run(["ssh-keygen", "-t", "ecdsa", "-b", "521", "-f", ecdsa_key_path, "-N", ""], check=True)
    else:
        print(f"The SSH key existed at: {path}")

def create_log_file(path, filename):
    """Create a log file with random content."""
    with open(os.path.join(path, filename), 'w') as f:
        for _ in range(10):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} - [VMkernel] {generate_random_string(10)} logged in from {generate_random_string(15)}\n")

def create_vmdk_file(path, vm_name):
    """Create fake VMDK file."""
    for _ in range(random.randint(2, 5)):  # Create 2-5 VMDK files for each VM
        vmdk_name = f"{vm_name}.vmdk"
        with open(os.path.join(path, vmdk_name), 'w') as f:
            f.write("KDM\n")
            f.write("version=1\n")
            f.write("CID=00000000-0000-0000-0000-000000000000\n")
            f.write(f"parent = \"{generate_random_string(36)}\"\n")
            f.write(f"createType = \"twoGBMaxExtent\"")
            # Add tokens for VMDK
            token = f"http://example.com/{uuid.uuid4()}.aspx"
            f.write(f"token = {token}\n")

def create_flat_vmdk(path, vm_name, size_gb):
    """Create virtual VMDK file with the desired size."""
    file_path = os.path.join(path, f"{vm_name}-flat.vmdk")
    with open(file_path, 'wb') as f:
        f.truncate(size_gb * 1024 * 1024 * 1024)  # 1GB = 1024MB = 1024*1024KB = 1024*1024*1024B

def delete_esx_files(base_path):
    """Delete files and folders have been created earlier."""
    try:
        shutil.rmtree(base_path)
        print(f"Delete all files and folders in: {base_path}")
    except FileNotFoundError:
        print(f"No folder found: {base_path}")
    except PermissionError:
        print(f"There is no right to delete folders: {base_path}")

def create_fake_file(file_path, file_size_in_bytes):
    """Create a fake file with a large size on Linux."""
    # Convert file_size_in_bytes into truncate format (for example: 1g, 100m)
    file_size_str = f"{file_size_in_bytes // (1024 * 1024)}M"  # Suppose the size is calculated in MB
    try:
        subprocess.run(["truncate", "-s", file_size_str, file_path])
        print(f"Created fake files: {file_path} with size {file_size_str}.")
    except FileNotFoundError:
        print(f"The 'truncate' tool is not found.Please install 'truncate' before running.")
        

def create_symlinks(base_path, symlinks):
    for link_name, target in symlinks.items():
        link_path = os.path.join(base_path, link_name)
        target_path = os.path.join(base_path, target)

        #Check if the link has existed
        if os.path.exists(link_path):
            print(f"Link '{link_name}' already exist.")
            continue

        try:
            os.symlink(target_path, link_path)
            print(f"Created links'{link_name}' point to'{target}'.")
        except OSError as e:
            print(f"Error when creating links '{link_name}': {e}")


        
        
        
        
        
        
        
        
