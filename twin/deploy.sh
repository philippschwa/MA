#!/bin/bash

#### WAZUH AGENT INSTALLATION ####

# Add the Wazuh repository to download the official packages
curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | apt-key add -
echo "deb https://packages.wazuh.com/4.x/apt/ stable main" | tee -a /etc/apt/sources.list.d/wazuh.list
apt-get update

# Setting hostname and install agent
echo "INSTALL WAZUH AGENT"
WAZUH_MANAGER="wazuh-manager" apt-get install -y wazuh-agent
#echo "MOVE CONFIGURATION FILE ossec.conf"
#mv ./ossec.conf /var/ossec/etc/ossec.conf

# Enable and start Wazuh agent service
echo "SYSTEMCTL COMMANDS"
systemctl daemon-reload
systemctl enable wazuh-agent
systemctl start wazuh-agent
tail -n 10 /var/ossec/logs/ossec.log
echo "WAZUH UP"

#### MINI NET INSTALLATION ####
tail -f /dev/null