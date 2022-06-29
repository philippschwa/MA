#!/bin/sh

sudo brctl addbr br-left
sudo brctl addbr br-right
sudo tunctl -t tap-left
sudo tunctl -t tap-right
sudo ifconfig tap-left 0.0.0.0 promisc up
sudo ifconfig tap-right 0.0.0.0 promisc up
sudo brctl addif br-left tap-left
sudo ifconfig br-left up
sudo brctl addif br-right tap-right
sudo ifconfig br-right up

sudo brctl show

# Note:  you also need to have loaded br_netfilter module
# ('modprobe br_netfilter') to enable /proc/sys/net/bridge
#sudo pushd /proc/sys/net/bridge
#sudo for f in "bridge-nf-*"; do echo 0 > $f; done
#sudo popd
# lxc-create now requires a template parameter, such as '-t ubuntu'


#sudo lxc-create -f lxc-left.conf -t download -n left -- -d ubuntu -r focal -a amd64
#sudo lxc-create -f lxc-right.conf -t download -n right -- -d ubuntu -r focal -a amd64 
sudo lxc-create -t download -n left -- -d ubuntu -r focal -a amd64
sudo lxc-create -t download -n right -- -d ubuntu -r focal -a amd64

# Start both containers
sudo lxc-start -n left -d
sudo lxc-start -n right -d
