
############################################################
# Minimal Docker Container for HMI simulation
############################################################

FROM ubuntu:20.04

USER root
WORKDIR /ma

# update packages & install dependencies
RUN apt-get update -y && apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils python3 net-tools iproute2 iputils-ping nano 

# install packages for attacks
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y hping3 ettercap-common nmap tcpdump openssh-server openssh-client

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 admin 
RUN echo 'admin:nimda' | chpasswd

COPY scripts/dos.sh /ma/dos.sh
COPY scripts/mitm.sh /ma/mitm.sh
COPY scripts/init.sh /ma/init.sh

CMD ["/ma/init.sh"]
