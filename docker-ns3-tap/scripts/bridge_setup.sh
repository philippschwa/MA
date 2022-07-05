#!/bin/sh

# This file creates a bridge with the tool brctl (ethernet bridge administration)
# and a TAP interface with the tool tunctl (create and manage persistent TUN/TAP interfaces)
# then the tap interface is configured in promisc mode, added to the bridge
# and started.
# References:
# brctl -> http://linuxcommand.org/man_pages/brctl8.html
# tunctl -> http://linux.die.net/man/8/tunctl

# The whole purpose of this script is to create the end of the NS3 node.
# So the NS3 nodes will try to connect to the tap-$NAME device,
# since this is connected to the bridge, and a docker container will be connected
# to the same bridge via another mechanism ... that will make the docker container
# to be able to communicate via the NS3 simulation.

# $1 Node's name
if [ -z "$1" ]; then
    echo "bridge_setup.sh --- No name supplied"
    exit 1
fi
# $2 = Bridge IP address
if [ -z "$2" ]
  then
    echo "No IP address supplied"
    exit 1
fi


NAME=$1
BR_ADDR=$2
BR_NAME=br-$NAME
TAP_NAME=tap-$NAME

# Create bridge
sudo ip link add $BR_NAME type bridge
sudo ip addr add ${BR_ADDR}/16 dev $BR_NAME

# Create TAP device for ns3
sudo tunctl -t tap-$NAME
sudo ifconfig $TAP_NAME hw ether 00:00:00:00:00:01
sudo ifconfig $TAP_NAME 0.0.0.0 up

# link bridge and TAP device
sudo brctl addif $BR_NAME $TAP_NAME

# set up bridge
sudo ifconfig $BR_NAME up

#sudo brctl addbr $BR_NAME
#sudo tunctl -t tap-$NAME
#sudo ifconfig tap-$NAME 0.0.0.0 promisc up
#sudo brctl addif $BR_NAME tap-$NAME
#sudo ifconfig $BR_NAME up

#sudo ip addr add ${BR_ADDR}/16 dev $BR_NAME


status=$?
if [ $status -ne 0 ]; then
    echo "bridge_setup.sh --- Failed to create bridge: $NAME!"
    exit $status
fi