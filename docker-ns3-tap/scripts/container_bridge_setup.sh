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

# $4 = Bridge IP address
if [ -z "$3" ]
  then
    echo "No Bridge IP address supplied"
    exit 1
fi

# defining some variables we gonna need
NAME=$1
IP=$2
MAC=$3
BR_NAME=br-$NAME
BR_ADDR=$4

SIDE_A=veth-host-$NAME
SIDE_B=veth-docker-$NAME

# At another shell, learn the container process ID and create its namespace entry in /var/run/netns/ for the "ip netns" command we will be using below
PID=$(docker inspect --format '{{ .State.Pid }}' $NAME)
sudo mkdir -p /var/run/netns
sudo ln -s /proc/$PID/ns/net /var/run/netns/$PID


# Create a pair of "peer" interfaces A and B,
# bind the A end to the bridge, and bring it up
sudo ip link add $SIDE_A type veth peer name $SIDE_B
sudo brctl addif $BR_NAME $SIDE_A
sudo ip link set $SIDE_A up


# Place B inside the container's network namespace,
# rename to eth0, and activate it with the given IP & MAC
sudo ip link set $SIDE_B netns $PID
sudo ip netns exec $PID ip link set dev $SIDE_B name eth0
sudo ip netns exec $PID ip link set eth0 address $MAC
sudo ip netns exec $PID ip addr add $IP dev eth0
sudo ip netns exec $PID ip link set eth0 up

# hier hinzugefüght, damit Container Bridge findet
sudo ip netns exec $PID ip route add default via $BR_ADDR

status=$?
if [ $status -ne 0 ]; then
    echo "container_bridge_setup.sh --- 3 Failed to create bridge: $NAME!"
    exit $status
fi