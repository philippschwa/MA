#!/bin/sh
#

modprobe br_netfilter

pushd /proc/sys/net/bridge
for f in bridge-nf-*; do echo 0 > $f; done
popd

status=$?
if [ $status -ne 0 ]; then
    echo "bridge_end_setup.sh --- Failed to do stuff!"
    exit $status
fi