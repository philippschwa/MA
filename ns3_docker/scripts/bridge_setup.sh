#!/bin/sh

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

NAME=$1
IP=$2
BR_NAME=br-$NAME
TAP_NAME=tap-$NAME
VETH1=veth1-$NAME
VETH2=veth2-$NAME

# Create bridge 
sudo ip link add $BR_NAME type bridge
# sudo ip link set $BR_NAME promisc on
sudo ip link set $BR_NAME up

# create TAP interface for ns3
sudo tunctl -t $TAP_NAME
sudo ip link set $TAP_NAME promisc on
# set up and attach TAP interface to the bridge 
sudo ip link set $TAP_NAME master $BR_NAME
sudo ip link set $TAP_NAME up

# create VETH tunnel for connection to container 
sudo ip link add $VETH1 type veth peer name $VETH2
# sudo ip link set $VETH1 promisc on
# delete with ip link delete <ifname>

# link PID of container to netns, in order to use netns
PID=$(docker inspect --format '{{ .State.Pid }}' $NAME)
sudo mkdir -p /var/run/netns
sudo ln -s /proc/$PID/ns/net /var/run/netns/$PID

# connect $VETH1 to bridge
# connect $VETH2 to running docker container, by using PID of container
sudo ip link set $VETH1 master $BR_NAME
sudo ip link set $VETH2 netns $PID

# start interfaces and bridge (on host side)
sudo ip link set $VETH1 up

# Setup docker container network interface 
sudo ip netns exec $PID ip link set dev $VETH2 name eth0
sudo ip netns exec $PID ip addr add $IP/24 brd + dev eth0
sudo ip netns exec $PID ip link set eth0 up
