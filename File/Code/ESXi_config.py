import os
import random
import string
import datetime
import uuid
import subprocess
import shutil

def generate_random_string(length):
    """Tạo một chuỗi ký tự ngẫu nhiên."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def create_config_file(path, filename, content):
    """Tạo file cấu hình với nội dung ngẫu nhiên."""
    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as f:
        f.write(content)

def create_directory(path):
  try:
    os.makedirs(path, exist_ok=True)  
  except OSError as e:
    print(f"Lỗi khi tạo thư mục: {e}")

def create_passwd_file(path):
    """Tạo file /etc/vmware/passwd giả mạo."""
    content = """
    # Thông tin tài khoản người dùng (Deception)
    root:x:0:0:Administrator:/:/bin/sh
    dcui:x:100:100:DCUI User:/:/bin/sh
    vpxuser:x:500:100:VMware VirtualCenter administration account:/:/bin/sh
    daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
    sys:x:3:3:sys:/dev:/usr/sbin/nologin
    adm:x:4:4:adm:/var/adm:/usr/sbin/nologin
    lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
    mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
    uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
    operator:x:11:0:operator:/root:/sbin/nologin
    games:x:12:100:games:/usr/games:/usr/sbin/nologin
    gopher:x:13:30:gopher:/usr/lib/gopher-data:/usr/sbin/nologin
    ftp:x:14:50:FTP User:/var/ftp:/usr/sbin/nologin
    vcsa:x:69:69:virtual console:/dev:/sbin/nologin
    ntp:x:38:38::/etc/ntp:/sbin/nologin
    nscd:x:28:28:NSCD Daemon:/:/usr/sbin/nologin
    dbus:x:81:81:System message bus:/:/usr/sbin/nologin
    avahi:x:70:70:Avahi daemon:/:/usr/sbin/nologin
    rpcuser:x:29:29:RPC Service User:/var/lib/nfs:/usr/sbin/nologin
    nfsnobody:x:65534:65534:Anonymous NFS User:/var/lib/nfs:/usr/sbin/nologin
    postfix:x:89:89::/var/spool/postfix:/usr/sbin/nologin
    sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/usr/sbin/nologin
    messagebus:x:18:18::/var/run/dbus:/usr/sbin/nologin
    polkitd:x:999:998:User for polkitd:/:/usr/sbin/nologin
    usbmuxd:x:113:113:usbmuxd user:/:/usr/sbin/nologin

    # Fake users (Deception)
    fakeuser1:x:1000:1000::/home/fakeuser1:/bin/bash
    fakeuser2:x:1001:1001::/home/fakeuser2:/bin/false 
    backupuser:x:1002:1002::/backup:/bin/bash
    """

    create_config_file(path, "passwd", content)

def create_hosts_file(path):
    """Tạo file /etc/hosts giả mạo."""
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

    # Thêm nhiều mục giả mạo
    for _ in range(5): 
        fake_ip = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        fake_hostname = f"fake-server-{generate_random_string(5)}.corp"
        content += f"\n{fake_ip} {fake_hostname}"  

    # Mô phỏng dịch vụ quan trọng
    fake_services = {
        "vcenter": "10.10.10.11",
        "backup-server": "10.10.10.12",
        "domain-controller": "10.10.10.13"
    }
    for name, ip in fake_services.items():
        content += f"\n{ip} {name}.internal" 

    create_config_file(path, "hosts", content)

def create_fake_datastore(base_path, datastore_name,size_gb):
    """Mô phỏng datastore bằng cách tạo thư mục và file."""
    datastore_path = os.path.join(base_path, "vmfs", "volumes", datastore_name)
    os.makedirs(datastore_path, exist_ok=True)
    # Kiểm tra xem đã có file trong thư mục datastore_path hay chưa
    if os.listdir(datastore_path):
        return 
    filename = str(uuid.uuid4())  # Tạo UUID ngẫu nhiên
    with open(os.path.join(datastore_path, filename), 'w') as f:
        f.write(f"Fake Size: {size_gb} GB\n")  # Thêm thông tin kích thước giả

def create_sshd_config(path, fake_port=None, allowed_ips=None):
    """Tạo file /etc/ssh/sshd_config giả mạo."""
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

    # Các thiết lập bị vô hiệu hóa khi build OpenSSH:
    #GSSAPIAuthentication no
    #KerberosAuthentication no 
    """

    if allowed_ips:
        content += "\nAllowUsers " + " ".join(allowed_ips)  # Giới hạn truy cập IP

    create_config_file(path, "sshd_config", content)

def create_vmware_lic(path):
    """Tạo file /etc/vmware/vmware.lic giả mạo."""
    license_key = generate_random_string(32)
    expiry_date = (datetime.datetime.now() + datetime.timedelta(days=365*10)).strftime("%Y-%m-%d") # 10 năm sau
    callback_url = "http://your-server.com/collect_ransomware_data?id=12345" # URL thu thập thông tin

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
    """Tạo các file SSH key giả mạo (nếu chưa tồn tại)."""
    os.makedirs(path, exist_ok=True)

    rsa_key_path = f"{path}/ssh_host_rsa_key"
    ecdsa_key_path = f"{path}/ssh_host_ecdsa_key"

    # Kiểm tra nếu key đã tồn tại
    if not (os.path.exists(rsa_key_path) and os.path.exists(ecdsa_key_path)):
        # Tạo RSA key
        subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", rsa_key_path, "-N", ""], check=True)
        # Tạo ECDSA key
        subprocess.run(["ssh-keygen", "-t", "ecdsa", "-b", "521", "-f", ecdsa_key_path, "-N", ""], check=True)
    else:
        print(f"Các key SSH đã tồn tại tại: {path}")

def create_log_file(path, filename):
    """Tạo file log với nội dung ngẫu nhiên."""
    with open(os.path.join(path, filename), 'w') as f:
        for _ in range(10):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} - [VMkernel] {generate_random_string(10)} logged in from {generate_random_string(15)}\n")

def create_vmdk_file(path, vm_name):
    """Tạo file VMDK giả mạo."""
    for _ in range(random.randint(2, 5)):  # Tạo 2-5 file VMDK cho mỗi VM
        vmdk_name = f"{vm_name}.vmdk"
        with open(os.path.join(path, vmdk_name), 'w') as f:
            f.write("KDM\n")
            f.write("version=1\n")
            f.write("CID=00000000-0000-0000-0000-000000000000\n")
            f.write(f"parent = \"{generate_random_string(36)}\"\n")
            f.write(f"createType = \"twoGBMaxExtent\"")
            # Thêm token cho VMDK
            token = f"http://example.com/{uuid.uuid4()}.aspx"
            f.write(f"token = {token}\n")

def create_flat_vmdk(path, vm_name, size_gb):
    """Tạo file VMDK ảo với kích thước mong muốn."""
    file_path = os.path.join(path, f"{vm_name}-flat.vmdk")
    with open(file_path, 'wb') as f:
        f.truncate(size_gb * 1024 * 1024 * 1024)  # 1GB = 1024MB = 1024*1024KB = 1024*1024*1024B

def create_vmx_file(domain, path, vm_name_window, template_path="S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\Window 10.vmx"):
    """Tạo file VMX giả mạo với token ẩn."""
    file_id = str(uuid.uuid4()).replace("-", "")
    vmx_name = f"{vm_name_window}.vmx"
    vmx_file = os.path.join(path, vmx_name)

    # Kiểm tra xem file mẫu có tồn tại không
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"File mẫu '{template_path}' không tồn tại.")

    # Sao chép file mẫu
    with open(template_path, "rb") as f_in, open(vmx_file, "wb") as f_out:
        f_out.write(f_in.read())

    # # Thêm token vào file VMX (cách ẩn hơn)
    # with zipfile.ZipFile(vmx_file, "a") as zf:
    #     xml_data = zf.read("vmx.xml")
    #     root = ET.fromstring(xml_data)

    #     # Tìm thẻ "extraConfig" (nếu có) và thêm token
    #     extra_config_element = root.find(".//extraConfig")
    #     if extra_config_element is not None:
    #         token = f"http://{domain}/{file_id}.aspx"
    #         extra_config_element.set("token", token)
    #     else:
    #         # Nếu không tìm thấy thẻ "extraConfig", tạo thẻ mới và thêm token
    #         extra_config_element = ET.Element("extraConfig")
    #         extra_config_element.set("token", token)
    #         root.append(extra_config_element)

    #     zf.writestr("vmx.xml", ET.tostring(root, encoding='unicode'))

    return vmx_file

def create_script(path, filename):
    """Tạo script giả mạo."""
    with open(os.path.join(path, filename), 'w') as f:
        f.write("# This is a sample script\n")
        f.write("echo \"Hello, world!\"\n")


def generate_log_entry(attacker_ip, timestamp=None):
    """Tạo một dòng log Cowrie giả mạo."""
    if timestamp is None:
        timestamp = datetime.datetime.now().isoformat()

    # Tạo các thông tin ngẫu nhiên cho dòng log
    event_type = random.choice(["SSH"])
    event_action = random.choice(["login", "command", "disconnect"])
    username = random.choice(["admin", "root", "user"])
    command = random.choice(["ls", "pwd", "whoami", "uname -a", "date"])

    # Tạo dòng log
    log_entry = f"{timestamp} {event_type} {event_action} from {attacker_ip} as {username} [{command}]"
    return log_entry

def delete_esx_files(base_path = "/ESXI 7/"):
    """Xóa file và folder đã được tạo trước đó."""
    try:
        shutil.rmtree(base_path)
        print(f"Đã xóa tất cả file và folder trong: {base_path}")
    except FileNotFoundError:
        print(f"Không tìm thấy thư mục: {base_path}")
    except PermissionError:
        print(f"Không có quyền xóa thư mục: {base_path}")

def create_fake_file(file_path, file_size_in_bytes):
    """Tạo file giả mạo với kích thước lớn trên Linux."""
    # Chuyển đổi file_size_in_bytes thành định dạng cho truncate (ví dụ: 1G, 100M)
    file_size_str = f"{file_size_in_bytes // (1024 * 1024)}M"  # Giả sử kích thước tính bằng MB
    try:
        subprocess.run(["truncate", "-s", file_size_str, file_path])
        print(f"Đã tạo file giả mạo: {file_path} với kích thước {file_size_str}.")
    except FileNotFoundError:
        print(f"Công cụ 'truncate' không được tìm thấy. Vui lòng cài đặt 'truncate' trước khi chạy.")
        
        
        
        
        
        
        
        
        
        
