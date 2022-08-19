#!/bin/sh

# Allow Container to communicate with each other
sysctl net.bridge.bridge-nf-call-iptables=0
sysctl net.bridge.bridge-nf-call-arptables=0
sysctl net.bridge.bridge-nf-call-ip6tables=0

status=$?
if [ $status -ne 0 ]; then
    echo "bridge_end_setup.sh --- Failed to do stuff!"
    exit $status
fi