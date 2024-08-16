#Config
TELNET_PORT = 23
SYSLOG_PORT = 514
HTTPS_PORT = 443
VMOTION_PORT = 8000
ISCSI_PORT = 3260
SSH_PORT = 2222
OPENSLP_PORT = 4227

# Creds
VALID_USERS = {
    "root": "root",
    "admin": "adminpassword",
    "user": "userpassword"
}

# path to RSA key pub
RSA_PUB_KEY_PATH = "/app/Services"  

# path to RSA key
RSA_KEY_PATH = "/app/Services"

#SSH Banner
SSH_BANNER = b"""OpenSSH 8.3 (protocol 2.0)"""


# Server Banner
SERVER_BANNER = b"""The time and date of this login have been sent to the system logs.\r

WARNING:\r
   All commands run on the ESXi shell are logged and may be included in\r
   support bundles. Do not provide passwords directly on the command line.\r
   Most tools can prompt for secrets or accept them from standard input.\r

VMware offers supported, powerful system administration tools.  Please\r
see www.vmware.com/go/sysadmintools for details.\r

The ESXi Shell can be disabled by an administrative user. See the\r
vSphere Security documentation for more information.\r"""


LOG_ROOT = "/app/Logs"

POC_DATABASE = {
    "ESXiArgs": {
        "signature": "'arg1' : b'127.0.0.1'", # The characteristic string in the request
    },
    # Add other poc here
}

# SSH Fingerprint 
from utils import get_ssh_fingerprint_from_file
SSH_FINGERPRINT = get_ssh_fingerprint_from_file(RSA_KEY_PATH)

