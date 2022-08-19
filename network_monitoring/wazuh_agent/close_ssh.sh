#!/bin/bash

docker exec -d hmi bash -c "service ssh stop"

# Logging the active response call 
time=$(LANG=en_us_88591;  date +"%b %d %T") # Aug 18 11:32:56
echo "$time agent_ranjid close_ssh.sh: SSH port closed on HMI by active response." >> /var/ossec/logs/ar_ssh.log
