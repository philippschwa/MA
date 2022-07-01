#!/bin/sh

# This file basically tears down the network bridge and TAP interface 

if [ -z "$1" ]; then
    echo "lxc_container_teardown.sh --- No container name supplied"
    exit 1
fi

NAME=$1

# Stop and remove lxc container
sudo lxc-stop -n $NAME
sudo lxc-destroy -n $NAME

# Remove bridge and TAP interface
sudo ifconfig br-$NAME down
sudo brctl delif br-$NAME tap-$NAME
sudo brctl delbr br-$NAME
sudo ifconfig tap-$NAME down
sudo tunctl -d tap-$NAME

status=$?
if [ $status -ne 0 ]; then
    echo "lxc_container_teardown.sh --- Failed to remove lxc container: $NAME!"
    exit $status
fi


