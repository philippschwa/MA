#!/bin/bash

service rsyslog start
service ssh start

status=$?
if [ $status -ne 0 ]; then
    echo "Failed to execute deploy script!"
    exit $status
fi

tail -f /var/log/sshd.log | tee -a logs/sshd.log

# Dummy process to keep container running
tail -f /dev/null