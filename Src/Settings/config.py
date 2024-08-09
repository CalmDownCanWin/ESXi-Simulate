#Config

SSH_PORT = 2222

# Creds
VALID_USERS = {
    "root": "root",
    "admin": "adminpassword",
    "user": "userpassword"
}

# path to RSA key pub
RSA_PUB_KEY_PATH = ""  

# path to RSA key
RSA_KEY_PATH = ""

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


LOG_ROOT = ""

# SSH Fingerprint 
from utils import get_ssh_fingerprint_from_file
SSH_FINGERPRINT = get_ssh_fingerprint_from_file(RSA_KEY_PATH)

