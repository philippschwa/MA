#!/bin/sh
#

#??modprobe br_netfilter

# alter Befehl von source github repo
#pushd /proc/sys/net/bridge
#for f in bridge-nf-*; do echo 0 > $f; done
#popd

# meine lösung:
sysctl net.bridge.bridge-nf-call-iptables=0
sysctl net.bridge.bridge-nf-call-arptables=0
sysctl net.bridge.bridge-nf-call-ip6tables=0
sysctl net.bridge.bridge-nf-call-ip6tables=0



status=$?
if [ $status -ne 0 ]; then
    echo "bridge_end_setup.sh --- Failed to do stuff!"
    exit $status
fi