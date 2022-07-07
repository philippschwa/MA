# Detection of simulated Cyber Attacks against an IIoT Network using a SIEM System

## Description

SIEM systems are already in use as part of the Security Operations Center (SOC) within
the organizations overall security strategy. They offer comprehensive security analyses
and enable SIEM analysts to secure the network more efficiently. In the context of the
IIoT , cyber-attacks are becoming more complex and using more points of attack, which
is why a holistic view of enterprise security is crucial [VGD+21](https://link.springer.com/chapter/10.1007/978-3-030-81242-3_17).

This project simulates an IIoT network. The network is simulated using the open source 
[ns3](https://www.nsnam.org/) sofware. Within the project various attacks on different 
nodes are implemented. With the help of Wazuh and Suricata the attack detection is performed.

## Installation (on Ubuntu 20.04 LTS)


#### 1. Install [Docker](https://docs.docker.com/engine/install/ubuntu/) (version 20.10.17, build 100c701) and [Docker-Compose](https://docs.docker.com/compose/install/) (version v2.6.0) as described in the respective docs

#### 2. Clone the repository:
```bash
git clone https://github.com/philippschwa/MA.git
```

#### 3. Install ns3 in your /home/<user> directory (see READ.ME in xy)

#### 4. Run the setup script (from the MA folder):
It installs the necessary packages and the sets up the project.
```bash
sudo ./setup.sh
```
#### 5. Setup and start the simulation. (TODO: write one setup script, e.g. start.sh/py)
First you have to start up the Wazuh Manager, Indexer and Dashboard. The docker compose file starts all necessary containers. Therfore run from the wazuh folder:
```bash
docker compose up
```

Second you have to setup the basics for the simulation (docker-ns3 folder):
```bash
sudo pyhton3 main.py setup
```

Third you have to start the simulated network with ns3 (from the /ns-3-allinone/ns-3.36):
```bash
./ns3 run --enable-sudo scratch/my-tap-csma.cc
```


