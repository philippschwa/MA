
############################################################
# Minimal Docker Container for HMI simulation
############################################################

FROM ubuntu:20.04

USER root
WORKDIR /ma

# update packages & install dependencies
RUN apt-get update -y && apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils python3 python3-pip net-tools iproute2 iputils-ping nano python3-scapy


# install packages for attacks
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y hping3 ettercap-common nmap tcpdump openssh-server openssh-client rsyslog tcptraceroute


RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 admin 
RUN echo 'admin:nimda' | chpasswd

COPY scripts/* /ma/
#COPY scripts/hmi.py /ma/hmi.py

COPY config/log.conf /etc/ssh/sshd_config.d
COPY config/sshd.conf /etc/rsyslog.d/sshd.conf

RUN chmod +x /ma/*.sh

CMD ["/ma/init.sh"]
