#!/bin/sh


if [ -z "$1" ]; then
    echo "lxc_container_setup.sh --- No container name supplied"
    exit 1
fi

NAME=$1

sudo brctl addbr br-$NAME
sudo tunctl -t tap-$NAME
sudo ifconfig tap-$NAME 0.0.0.0 promisc up
sudo brctl addif br-$NAME tap-$NAME
sudo ifconfig br-$NAME up

status=$?
if [ $status -ne 0 ]; then
    echo "lxc_container_setup.sh --- Failed to create bridge: $NAME!"
    exit $status
fi

sudo brctl show

# Note:  you also need to have loaded br_netfilter module
# ('modprobe br_netfilter') to enable /proc/sys/net/bridge

# failure -> don't know why...
#sudo pushd /proc/sys/net/bridge
#sudo for f in "bridge-nf-*"; do echo 0 > $f; done
#sudo popd

# create lxc container from image ubuntu 20.04 (focal) amd64
# config files won't work as expected
#sudo lxc-create -f lxc-left.conf -t download -n left -- -d ubuntu -r focal -a amd64
#sudo lxc-create -f lxc-right.conf -t download -n right -- -d ubuntu -r focal -a amd64 
sudo lxc-create  -t download -n $NAME -- -d ubuntu -r focal -a amd64
#sudo lxc-create --rcfile=../config/lxc-left.conf -t download -n left -- -d ubuntu -r focal -a amd64

# Start lxc container
sudo lxc-start -n $NAME -d

status=$?
if [ $status -ne 0 ]; then
    echo "lxc_container_setup.sh --- Failed to create lxc container: $NAME!"
    exit $status
fi

sudo lxc-ls -f