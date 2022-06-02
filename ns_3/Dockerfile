FROM ubuntu:20.04

USER root
WORKDIR /app

# Update Ubuntu Repo 
RUN apt-get update -y && apt-get upgrade -y

# install core dependencies for build and compilation
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential libsqlite3-dev libboost-all-dev \
    libssl-dev git python3-setuptools castxml
# python-dev missing - not an essential dependency

# install dependencies for ns-3 python bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    gir1.2-goocanvas-2.0 gir1.2-gtk-3.0 \
    libgirepository1.0-dev python3-dev python3-gi python3-gi-cairo \
    python3-pip python3-pygraphviz python3-pygccxml

# install dependecies for ns-3
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    g++ pkg-config sqlite3 qt5-default mercurial \
    ipython3 openmpi-bin openmpi-common openmpi-doc libopenmpi-dev \
    autoconf cvs bzr unrar gdb valgrind uncrustify doxygen graphviz \
    imagemagick python3-sphinx dia tcpdump libxml2 libxml2-dev cmake \
    libc6-dev libc6-dev-i386 libclang-6.0-dev llvm-6.0-dev automake 

# install ns3 & set environment variables
# Manuelle Installation 
RUN git clone https://gitlab.com/nsnam/ns-3-allinone.git \
    && cd ns-3-allinone \
    && ./download.py -n ns-3.36 \
    && ./build.py


# Befehle für Installation mit bake --> Fehler im build Prozess...
#RUN git clone https://gitlab.com/nsnam/bake 
#RUN chmod +x ./bake/bake.py

#ENV BAKE_HOME="/app/bake"
#ENV PATH="${PATH}:${BAKE_HOME}"   
#ENV PYTHONPATH="${PYTHONPATH}:${BAKE_HOME}"

# copy deploy script into container an make it executable
COPY ./deploy.sh ./ 
RUN chmod u+x ./deploy.sh

CMD ["./deploy.sh"]