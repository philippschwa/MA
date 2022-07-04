#!/bin/sh
# Install packages needed for ns3 and other simulation stuff

apt-get update -y && apt-get upgrade -y


apt install -y g++ python3 cmake python3-setuptools git tcpdump vtun lxc uml-utilities bridge-utils

git clone https://gitlab.com/nsnam/ns-3-allinone.git && cd ns-3-allinone && ./download.py -n ns-3.36 \
    && ./build.py 