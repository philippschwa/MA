FROM ubuntu:20.04

USER root
WORKDIR /app

# install dependencies
RUN apt-get update 
RUN apt-get install -y \
    sudo \
    net-tools \
    apt-utils \
	python3 \
	python3-pip \
	iputils-ping \
    net-tools \
    curl \
    systemctl \
    screen \
    git

# install & setup mininet
RUN git clone https://github.com//mininet/mininet \
	&& ./mininet/util/install.sh -a \
	&& pip install cpppo==4.3.4 \
	&& pip install minicps 

# Add the Wazuh repository to download the official packages & Install Wazuh Agent
RUN curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | apt-key add - \
    && echo "deb https://packages.wazuh.com/4.x/apt/ stable main" | tee -a /etc/apt/sources.list.d/wazuh.list \
    && apt-get update \
    && WAZUH_MANAGER="wazuh.manager" apt-get install -y wazuh-agent

COPY ./deploy.sh ./
RUN chmod u+x ./deploy.sh

CMD ["./deploy.sh"]