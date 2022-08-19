#!/bin/sh

# This file basically destroys the network bridges and TAP interfaces
if [ -z "$1" ]; then
    echo "bridge_destroy.sh --- No name supplied"
    exit 1
fi

NAME=$1
BR_NAME=br-$NAME
TAP_NAME=tap-$NAME
VETH1=veth1-$NAME


sudo ip link set $BR_NAME down
sudo ip link set $TAP_NAME down
sudo ip link del $TAP_NAME
sudo ip link del $VETH1
sudo ip link del $BR_NAME

# Old commands. Using newer iproute2 is better
#sudo ifconfig $BR_NAME down
#sudo brctl delif $BR_NAME $TAP_NAME
#sudo brctl delbr $BR_NAME
#sudo ifconfig $TAP_NAME down
#sudo tunctl -d $TAP_NAME

status=$?
if [ $status -ne 0 ]; then
    echo "bridge_destroy.sh --- Failed to destroy bridge: $NAME!"
    exit $status
fi