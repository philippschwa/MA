#!/bin/sh

# This file basically destroys the network bridges and TAP interfaces



if [ -z "$1" ]; then
    echo "bridge_destroy.sh --- No name supplied"
    exit 1
fi

NAME=$1

ifconfig br-$NAME down
brctl delif br-$NAME tap-$NAME
brctl delbr br-$NAME
ifconfig tap-$NAME down
tunctl -d tap-$NAME

status=$?
if [ $status -ne 0 ]; then
    echo "bridge_destroy.sh --- Failed to destroy bridge: $NAME!"
    exit $status
fi