
############################################################
# Minimal Docker Container for simulation
############################################################

FROM python:3.7.13-alpine3.16

USER root
WORKDIR /ma

# update packages & install dependencies
RUN apk update && apk upgrade
RUN DEBIAN_FRONTEND=noninteractive apk add net-tools iproute2 iputils nano bash

# install packages for attacks
RUN DEBIAN_FRONTEND=noninteractive apk add nmap tcpdump openssh-server openssh-client

COPY scripts/init.sh /ma/init.sh
RUN chmod +x /ma/init.sh

CMD ["/ma/init.sh"]
