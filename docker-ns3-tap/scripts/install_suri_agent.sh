#!/bin/sh

# download and install wazuh agent
curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | apt-key add - 
echo "deb https://packages.wazuh.com/4.x/apt/ stable main" | tee -a /etc/apt/sources.list.d/wazuh.list 
apt-get update 
WAZUh_MANAGER="123.123.0.2" apt-get install -y wazuh-agent
echo "wazuh-agent hold" | dpkg --set-selections

# install suricata and update rules
apt install -y software-properties-common 
apt-get update
add-apt-repository ppa:oisf/suricata-stable 
apt-get update && apt-get install -y suricata iproute2 jq

# suricata-update -o /etc/suricata/rules

# copy custom config files for agent and suricata
cp ../config/suricata.yaml /etc/suricata/suricata.yaml
cp ../config/ossec.conf /var/ossec/etc/ossec.conf
cp ../rules/ /etc/suricata/rules/

# start suricata service --> bridge node1, later all bridges used in simulation
systemctl daemon-reload
systemctl enable suricata
systemctl start suricata

# sollte über config datei einstellbar sein, welche bridges gemonitored werden sollen
#suricata -i br-node1 -D

# start wazuh agent
systemctl daemon-reload
systemctl enable wazuh-agent
systemctl start wazuh-agent