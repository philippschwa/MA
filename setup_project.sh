#!/bin/bash

# Install dependencies
sudo apt-get update -y 
sudo apt install -y g++ python3 python3-pip cmake python3-setuptools git tcpdump uml-utilities bridge-utils jq iproute2

# Install ns3
git clone https://gitlab.com/nsnam/ns-3-allinone.git && cd ns-3-allinone \
&& ./download.py -n ns-3.36 \
&& ./build.py

# Install wazuh agent
sudo curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | apt-key add - 
sudo echo "deb https://packages.wazuh.com/4.x/apt/ stable main" | tee -a /etc/apt/sources.list.d/wazuh.list 
sudo apt-get update 
sudo WAZUh_MANAGER="123.123.0.2" apt-get install -y wazuh-agent
sudo echo "wazuh-agent hold" | dpkg --set-selections

# Install Suricata
sudo apt install -y software-properties-common 
sudo apt-get update
sudo add-apt-repository ppa:oisf/suricata-stable 
sudo apt-get update && apt-get install -y suricata

# Copy custom config files for agent and suricata
sudo cp ns3_docker/config/suricata.yaml /etc/suricata/suricata.yaml
sudo cp ns3_docker/config/ossec.conf /var/ossec/etc/ossec.conf
sudo cp ns3_docker/rules/ /etc/suricata/rules/


# Start suricata and wazuh
sudo systemctl daemon-reload
sudo systemctl enable suricata
sudo systemctl enable wazuh-agent
#sudo systemctl start wazuh-agent
#sudo systemctl start suricata
