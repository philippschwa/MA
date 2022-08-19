#!/bin/bash

# Start Syslog and SSH service
service rsyslog start
service ssh start

# Start ARP Sniffer
python3 ./arp_sniffer.py &

# Write SSH logs to sshd.log
tail -f /var/log/sshd.log | tee -a logs/sshd.log

# keep container running 
tail -f /dev/null