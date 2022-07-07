#!/bin/sh
# Setup "empty" VM -- install dependencies and ns3 (ns3 has to be run as non sudo)

apt-get update -y && apt-get upgrade -y
apt install -y g++ python3 python3-pip cmake python3-setuptools git tcpdump uml-utilities bridge-utils

# vtun lxc

sudo -u caesar git clone https://gitlab.com/nsnam/ns-3-allinone.git && cd ns-3-allinone && ./download.py -n ns-3.36 && ./build.py 