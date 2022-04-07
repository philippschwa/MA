FROM ubuntu:20.04

# update packages
RUN apt-get

# install necessary packages
RUN apt-get install -y sudo \
	&& apt-get install -y apt-utils \
	&& apt-get install -y python3 \
	&& apt-get install -y python3-pip \
	&& apt-get install -y iputils-ping \
	&& apt-get install -y net-tools \
	&& apt-get install -y git \
	&& apt-get install -y screen 

WORKDIR /app

# install & setup mininet
RUN git clone https://github.com//mininet/mininet \
	&& ./mininet/util/install.sh -a \
	&& pip install cpppo==4.3.4 \
	&& pip install minicps \
	&& apt-get install -y ettercap-common \
	&& apt-get install -y hping3 

# start mininet
USER root
COPY . .
RUN chmod u+x ./mini_start.sh 
CMD ["./mini_start.sh"]