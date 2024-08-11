import os
#ESXI ROOT
ESXI_ROOT = "/home/test/Desktop/Dockerfile/ESXi_1/"

#LOG CONFIGURATION
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_FILE = "attack_logs.json"
MAX_QUEUE_SIZE = 10000

#SPLUNK TCP CONFIGURATION
SPLUNK_HOST = os.environ.get("SPLUNK_HOST", "") #add SPLUNK host 
SPLUNK_PORT = os.environ.get("SPLUNK_PORT", "") #add SPLUNK port

#SPLUNK HEC CONFIGURATION
SPLUNK_TOKEN = os.environ.get("SPLUNK_TOKEN", "dd85867d-0ec2-4189-bc8d-96fcaec97e8d") 
SPLUNK_INDEX = os.environ.get("SPLUNK_INDEX", "	esxi_log") 
SPLUNK_SOURCE = os.environ.get("SPLUNK_SOURCE", "event_logger") 