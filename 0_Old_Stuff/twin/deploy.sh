#!/bin/bash

# Enable and start Wazuh agent service
echo "SYSTEMCTL COMMANDS"
systemctl daemon-reload
systemctl enable wazuh-agent
service wazuh-agent start
tail -n 10 /var/ossec/logs/ossec.log
echo "WAZUH AGENT IS RUNNING"

# Start MiniNet
service openvswitch-switch start

# Dummy process to keep container running
tail -f /dev/null