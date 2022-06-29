#!/bin/sh

# This file basically destroys the network bridges and TAP interfaces



if [ -z "$1" ]; then
    echo "bridge_destroy.sh --- No name supplied"
    exit 1
fi

NAME=$1

sudo ifconfig br-$NAME down
sudo brctl delif br-$NAME tap-$NAME
sudo brctl delbr br-$NAME
sudo ifconfig tap-$NAME down
sudo tunctl -d tap-$NAME

status=$?
if [ $status -ne 0 ]; then
    echo "bridge_destroy.sh --- Failed to destroy bridge: $NAME!"
    exit $status
fi