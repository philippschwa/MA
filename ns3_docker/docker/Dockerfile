
############################################################
# Minimal Docker Container for simulation
############################################################

FROM ubuntu:20.04

USER root
WORKDIR /ma

# update packages & install dependencies
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y apt-utils python3 net-tools iproute2 iputils-ping nano 

# install packages for attacks
RUN apt-get install -y hping3 ettercap-common nmap tcpdump

COPY scripts/init.sh /ma/init.sh
RUN chmod +x /ma/init.sh

CMD ["/ma/init.sh"]
