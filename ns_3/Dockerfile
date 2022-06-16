FROM ubuntu:20.04

USER root
WORKDIR /ma

# Update Ubuntu Repo 
RUN apt-get update -y && apt-get upgrade -y

# install core dependencies for build and compilation
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential libsqlite3-dev libboost-all-dev \
    libssl-dev git python3-setuptools castxml apt-utils \
    iputils-ping net-tools curl systemctl screen

# install dependencies for ns-3 python bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    gir1.2-goocanvas-2.0 gir1.2-gtk-3.0 \
    libgirepository1.0-dev python3-dev python3-gi python3-gi-cairo \
    python3-pip python3-pygraphviz python3-pygccxml

# install dependecies for ns-3
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    g++ pkg-config sqlite3 qt5-default mercurial \
    ipython3 openmpi-bin openmpi-common openmpi-doc libopenmpi-dev \
    autoconf cvs bzr unrar-free gdb valgrind uncrustify doxygen graphviz \
    imagemagick python3-sphinx dia tcpdump libxml2 libxml2-dev cmake \
    libc6-dev libc6-dev-i386 libclang-6.0-dev llvm-6.0-dev automake 

# install ns3 & set environment variables
# Manuelle Installation (Optional: Hier noch hinter build.py '--enable-examples --enable-tests' einsetzen, damit tests etc. gemacht werden können; ca 3h kompilierungs Zeit)
RUN git clone https://gitlab.com/nsnam/ns-3-allinone.git \
    && cd ns-3-allinone \
    && ./download.py -n ns-3.36 \
    && ./build.py 
    # --enable-tests --enable-examples 


# Hier jetzt noch Wazuh Agent Installieren (Packages sind schon oben mit eingtragen.)
# Add the Wazuh repository to download the official packages & Install Wazuh Agent
RUN curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | apt-key add - \
    && echo "deb https://packages.wazuh.com/4.x/apt/ stable main" | tee -a /etc/apt/sources.list.d/wazuh.list \
    && apt-get update \
    && WAZUH_MANAGER="wazuh.manager" apt-get install -y wazuh-agent

# install Suricata
RUN apt install -y software-properties-common && apt-get update
RUN add-apt-repository ppa:oisf/suricata-stable 
RUN apt-get update && apt-get install -y suricata iproute2
# suricata-update
# RUN suricata-update -o /etc/suricata/rules

# copy custom config files for suricata wazuh agent
COPY config/suricata.yaml /etc/suricata/suricata.yaml
COPY config/ossec.conf /var/ossec/etc/ossec.conf

# copy deploy script into container an make it executable
COPY scripts/deploy.sh ./deploy.sh
RUN chmod u+x ./deploy.sh

CMD ["./deploy.sh"]