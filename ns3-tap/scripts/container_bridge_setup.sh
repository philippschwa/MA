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

SIDE_A=int-$NAME
SIDE_B=ext-$NAME


# At another shell, learn the container process ID
# and create its namespace entry in /var/run/netns/
# for the "ip netns" command we will be using below
mkdir -p /var/run/netns
ln -s /proc/$PID/ns/net /var/run/netns/$PID

# Create a pair of "peer" interfaces A and B,
# bind the A end to the bridge, and bring it up
ip link add $SIDE_A type veth peer name $SIDE_B
brctl addif $BRIDGE $SIDE_A
ip link set $SIDE_A up

# Place B inside the container's network namespace,
# rename to eth0, and activate it with the given IP & MAC
ip link set $SIDE_B netns $PID
ip netns exec $PID ip link set dev $SIDE_B name eth0
ip netns exec $PID ip link set eth0 address $MAC
ip netns exec $PID ip link set eth0 up
ip netns exec $PID ip addr add $IP dev eth0