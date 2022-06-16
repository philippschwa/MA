#!/bin/bash

echo "########## Executing deploy script ##########"
status=$?
if [ $status -ne 0 ]; then
    echo "Failed to start container!"
    exit $status
fi

# Start suricata
echo "########## Starting suricata ##########"
suricata -i eth0 -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start suricata: $status"
  exit $status
fi



# Enable and start Wazuh agent service
#systemctl daemon-reload
#systemctl enable wazuh-agent
#service wazuh-agent start
#tail -n 10 /var/ossec/logs/ossec.log
#echo "WAZUH AGENT IS RUNNING"

/var/ossec/bin/wazuh-control start
echo "########## Starting wazuh agent ##########"
status=$?
if [ $status -ne 0 ]; then
    echo "Failed to deploy Wazuh: $status"
    exit $status
fi

echo "background jobs running, listening for changes"

# Dummy process to keep container running
echo "########## Dummy process started! ##########"
tail -f /dev/null