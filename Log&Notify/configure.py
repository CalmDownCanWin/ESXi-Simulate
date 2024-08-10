import os
#ESXI ROOT
ESXI_ROOT = "D:\ZALO"

#LOG CONFIGURATION
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_FILE = "attack_logs.json"
MAX_QUEUE_SIZE = 10000

#SPLUNK TCP CONFIGURATION
SPLUNK_HOST = os.environ.get("SPLUNK_HOST", "") #add SPLUNK host 
SPLUNK_PORT = os.environ.get("SPLUNK_PORT", "") #add SPLUNK port
