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

# create TAP interface for ns3
sudo tunctl -t $TAP_NAME
sudo ifconfig $TAP_NAME 0.0.0.0 down

# create VETH tunnel for connection to container 
sudo ip link add $VETH1 type veth peer name $VETH2
# löschen mit ip link delete <ifname>

# connect $VETH1 to bridge
# connect $VETH2 to running docker contaienr, by using PID of container
PID=$(docker inspect --format '{{ .State.Pid }}' $NAME)
sudo ip link set $VETH1 master $BR_NAME
sudo ip link set $VETH2 netns $PID

# save PIDs in temporary folder to have them later for destruction
#sudo mkdir -p /var/run/netns
#sudo ln -s /proc/$PID/ns/net /var/run/netns/$PID

# attach TAP interface to the bridge
ip link set $TAP_NAME master $BR_NAME

# start interfaces and bridge (on host side)
sudo ifconfig $VETH1 up
sudo ifconfig $TAP_NAME up
sudo ifconfig $BR_NAME up

# Setup docker container network interface 
sudo ip netns exec $PID ip link set dev $VETH2 name eth0
sudo ip netns exec $PID ip addr add $IP/16 dev eth0
sudo ip netns exec $PID ip link set eth0 up