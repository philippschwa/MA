#!/bin/bash

echo "########## deploy.sh - Container Started ##########"
status=$?
if [ $status -ne 0 ]; then
    echo "Failed to echo Container Started!"
    exit $status
fi


# Wazuh Befehle

# Enable and start Wazuh agent service
#echo "SYSTEMCTL COMMANDS"
#systemctl daemon-reload
#systemctl enable wazuh-agent
#service wazuh-agent start
#tail -n 10 /var/ossec/logs/ossec.log
#echo "WAZUH AGENT IS RUNNING"
status=$?
if [ $status -ne 0 ]; then
    echo "Failed to deploy Wazuh!"
    exit $status
fi


# Dummy process to keep container running
echo "########## Dummy process started! ##########"
tail -f /dev/null