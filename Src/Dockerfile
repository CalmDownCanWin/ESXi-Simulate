FROM python:3.9

WORKDIR /app

COPY Shell_Commands /app/Shell_Commands
COPY Services /app/Services
COPY Settings /app/Settings
COPY Logs /app/Logs
COPY setup.py /app

#RUN apt-get update && apt-get install -y dnsutils 
RUN pip install --no-cache-dir rich paramiko requests && \
    pip install . && \
    rm -rf build *.egg-info &&  \
    pip install scapy

# Filesystem 
RUN mkdir /app/data

# Download
#UN mkdir /app/downloads


ENV PYTHONPATH=/app/Shell_Commands:/app/Services:/app/Settings:/app/Logs 

EXPOSE 2222 4227 514

#RUNNING Honeypot
CMD ["bash"] 
