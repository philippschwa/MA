
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
if [ -z "$4" ]
  then
    echo "No Bridge IP address supplied"
    exit 1
fi

# $5 = Bridge MAC address
if [ -z "$4" ]
  then
    echo "No Bridge MAC address supplied"
    exit 1
fi

# set variables
NAME=$1
IP=$2
MAC=$3
BR_NAME=br-$NAME
BR_ADDR=$4
BR_MAC=$5
TAP_NAME=tap-$NAME

SIDE_A=veth-ho-$NAME
SIDE_B=veth-$NAME

# Create bridge
sudo ip link add $BR_NAME type bridge
sudo ip addr add ${BR_ADDR}/16 dev $BR_NAME

# Create TAP device for ns3
sudo tunctl -t tap-$NAME
#sudo ifconfig $TAP_NAME hw ether 00:00:00:00:00:01
sudo ifconfig $TAP_NAME 0.0.0.0 promisc up

# link bridge and TAP device
sudo brctl addif $BR_NAME $TAP_NAME

# set up bridge
sudo ifconfig $BR_NAME up

echo "Finished setting up bridge and TAP device"
echo "Setting up Bridge to docker container"

# At another shell, learn the container process ID and create its namespace entry in /var/run/netns/ for the "ip netns" command we will be using below
PID=$(docker inspect --format '{{ .State.Pid }}' $NAME)
sudo mkdir -p /var/run/netns
sudo ln -s /proc/$PID/ns/net /var/run/netns/$PID

# Create a pair of "peer" interfaces A and B,
# bind the A end to the bridge, and bring it up
sudo ip link add $SIDE_A type veth peer name $SIDE_B
sudo brctl addif $BR_NAME $SIDE_A
sudo ip link set $SIDE_A up
sudo ip link set $SIDE_B netns $PID
sudo ip netns exec $PID ip link set dev $SIDE_B name eth123lol
sudo ip netns exec $PID ip link set eth123lol address $MAC
sudo ip netns exec $PID ip addr add $IP dev eth123lol
sudo ip netns exec $PID ip link set eth123lol up

# hier hinzugefüght, damit Container Bridge findet
sudo ip netns exec $PID ip route add $BR_ADDR dev eth123lol
sudo ip netns exec $PID ip route add default via $BR_ADDR