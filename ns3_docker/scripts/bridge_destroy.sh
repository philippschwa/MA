#!/bin/sh

if [ -z "$1" ]; then
    echo "bridge_destroy.sh --- No name supplied"
    exit 1
fi

NAME=$1
BR_NAME=br-$NAME
TAP_NAME=tap-$NAME

# Remove tap intefaces and bridges
sudo ip link set $BR_NAME down
sudo ip link set $TAP_NAME down
sudo ip link del $TAP_NAME
sudo ip link del $BR_NAME

status=$?
if [ $status -ne 0 ]; then
    echo "bridge_destroy.sh --- Failed to destroy bridge: $NAME!"
    exit $status
fi