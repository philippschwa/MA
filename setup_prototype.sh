#!/bin/bash

# Install dependencies
apt-get update -y 
DEBIAN_FRONTEND=noninteractive apt install -y g++ python3 python3-pip cmake python3-setuptools git tcpdump uml-utilities bridge-utils jq iproute2

# Install ns3
git clone https://gitlab.com/nsnam/ns-3-allinone.git && cd ns-3-allinone \
&& ./download.py -n ns-3.36 \
&& ./build.py

# Copy custom ns3 file and virtual network configuration file; Build the virtual network.
cp ns3_docker/ns3/ns3 ns-3-allinone/ns-3.36/ns3
cp ns3_docker/ns3/sim_topo.cc ns-3-allinone/ns-3.36/scratch/sim_topo.cc
./ns-3-allinone/ns-3.36/ns3 build sim_topo.cc

# Install wazuh agent
curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | apt-key add - 
echo "deb https://packages.wazuh.com/4.x/apt/ stable main" | tee -a /etc/apt/sources.list.d/wazuh.list 
apt-get update 
WAZUH_MANAGER="123.123.0.2" apt-get install -y wazuh-agent
echo "wazuh-agent hold" | dpkg --set-selections

# Install Suricata
DEBIAN_FRONTEND=noninteractive apt install -y software-properties-common 
apt-get update
add-apt-repository -y ppa:oisf/suricata-stable 
apt-get update && apt-get install -y suricata

# Copy custom config files for agent and suricata
cp network_monitoring/suricata/suricata.yaml /etc/suricata/suricata.yaml
cp network_monitoring/suricata/rules/ /etc/suricata/rules/ # FEHLER
cp network_monitoring/wazuh_agent/ossec.conf /var/ossec/etc/ossec.conf



# Start suricata and wazuh
systemctl daemon-reload
systemctl enable suricata
systemctl enable wazuh-agent
#sudo systemctl start wazuh-agent
#sudo systemctl start suricata