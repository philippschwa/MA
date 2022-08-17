############################################################
# Minimal Docker Container for Attacker
############################################################

FROM kalilinux/kali-rolling:latest

WORKDIR /ma

# update packages & install dependencies
RUN apt update -y 
#RUN apt -y install kali-linux-headless
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils python3 python3-pip net-tools iproute2 iputils-ping nano
# install packages for attacks
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y hping3 ettercap-common nmap tcpdump openssh-server openssh-client rsyslog tcptraceroute
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3-scapy hydra goldeneye

COPY scripts/* /ma/
COPY src/* /ma/src/
RUN chmod +x /ma/*

CMD ["./init.sh"]