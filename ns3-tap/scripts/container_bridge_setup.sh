#!/bin/bash

# $1 = Container name
if [ -z "$1" ]
  then
    echo "No container name supplied"
    exit 1
fi

# $2 = IP address
if [ -z "$2" ]
  then
    echo "No IP address supplied"
    exit 1
fi

# $3 = MAC address
if [ -z "$3" ]
  then
    echo "No MAC address supplied"
    exit 1
fi

# defining some variables we gonna need
NAME=$1
IP=$2
MAC=$3
BRIDGE=br-$NAME
PID=$(docker inspect --format '{{ .State.Pid }}' $NAME)

SIDE_A=side-int-$NAME
SIDE_B=side-ext-$NAME


# At another shell, learn the container process ID
# and create its namespace entry in /var/run/netns/
# for the "ip netns" command we will be using below
sudo mkdir -p /var/run/netns
sudo ln -s /proc/$PID/ns/net /var/run/netns/$PID
status=$?
if [ $status -ne 0 ]; then
    echo "container_bridge_setup.sh --- 1 Failed to create bridge: $NAME!"
    exit $status
fi

# Create a pair of "peer" interfaces A and B,
# bind the A end to the bridge, and bring it up
sudo ip link add $SIDE_A type veth peer name $SIDE_B
sudo brctl addif $BRIDGE $SIDE_A
sudo ip link set $SIDE_A up
status=$?
if [ $status -ne 0 ]; then
    echo "container_bridge_setup.sh --- 2 Failed to create bridge: $NAME!"
    exit $status
fi

# Place B inside the container's network namespace,
# rename to eth0, and activate it with the given IP & MAC
sudo ip link set $SIDE_B netns $PID
sudo ip netns exec $PID ip link set dev $SIDE_B name eth0
sudo ip netns exec $PID ip link set eth0 address $MAC
sudo ip netns exec $PID ip link set eth0 up
sudo ip netns exec $PID ip addr add $IP dev eth0

status=$?
if [ $status -ne 0 ]; then
    echo "container_bridge_setup.sh --- 3 Failed to create bridge: $NAME!"
    exit $status
fi