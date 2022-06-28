#!/bin/bash

echo "########## Executing deploy script! ##########"
status=$?
if [ $status -ne 0 ]; then
    echo "Failed to start container!"
    exit $status
fi

# Start suricata
echo "########## Starting suricata! ##########"

suricata -i eth0 -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start suricata: $status"
  exit $status
fi



# Enable and start Wazuh agent service
echo "########## Starting wazuh agent! ##########"

/var/ossec/bin/wazuh-control start
status=$?
if [ $status -ne 0 ]; then
    echo "Failed to deploy Wazuh: $status"
    exit $status
fi

# Dummy process to keep container running
echo "########## Dummy process started! ##########"
tail -f /dev/null