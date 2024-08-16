OPENSLP_PORT = 427
SERVER_IP = ""
TELNET_PORT = 23
SYSLOG_PORT = 514
HTTPS_PORT = 443
VMOTION_PORT = 8000
ISCSI_PORT = 3260

DCUI_PORT = 5900
DCUI_BANNER = b"""
DCUI: VMware ESXi 7.5.0 (Build 5969303)
"""

# Valid user and corresponding password
SSH_PORT = 22
VALID_USERS = {
    "root": "root",
    "admin": "adminpassword",
    "user": "userpassword"
}

SERVER_BANNER = b"""The time and date of this login have been sent to the system logs.\r

WARNING:\r
   All commands run on the ESXi shell are logged and may be included in\r
   support bundles. Do not provide passwords directly on the command line.\r
   Most tools can prompt for secrets or accept them from standard input.\r

VMware offers supported, powerful system administration tools.  Please\r
see www.vmware.com/go/sysadmintools for details.\r

The ESXi Shell can be disabled by an administrative user. See the\r
vSphere Security documentation for more information.\r"""
LOG_ROOT = ""
# The path to RSA Key Pub
RSA_PUB_KEY_PATH = "test_rsa.key.pub" 

# The path to RSA Key
RSA_KEY_PATH = "test_rsa.key"  

# SSH Banner
SSH_BANNER = b"SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.5"

# SSH Fingerprint (Taken from the RSA Key file)
from utils import get_ssh_fingerprint_from_file
SSH_FINGERPRINT = get_ssh_fingerprint_from_file(RSA_KEY_PATH)

# Telnet Banner fake
TELNET_BANNER =  b"SSH-2.0-OpenSSH_8.8\r\n"

TEMPLATE_FOLDER = "templates"
STATIC_FOLDER = "static"

POC_DATABASE = {
    "ESXiArgs": {
        "signature": "'arg1' : b'127.0.0.1'", # The characteristic string in the request
    },
    # Add other poc here
}
