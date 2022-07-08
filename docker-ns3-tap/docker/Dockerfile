
############################################################
# Minimal Docker Container for testing purposes
# Later here should be the attacks and stuff
############################################################

FROM ubuntu:20.04

USER root
WORKDIR /ma

# Update Ubuntu Repo 
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y apt-utils net-tools iproute2 iputils-ping nano 

# install attacker packages
RUN apt-get install -y hping3 ettercap-common

COPY init.sh ./init.sh
RUN chmod +x ./init.sh

COPY ../attacks /ma/attacks

CMD ["./init.sh"]