#!/bin/bash

echo "########## deploy.sh - Container Started ##########"

# Start ns-3
echo "########## Installing pip packages. ##########"
#pip3 install cxxfilt pygccxml pybindgen castxml distro requests

status=$?
if [ $status -ne 0 ]; then
    echo "Failed to install python packages!"
    exit $status
fi


#echo "########## Deploying ns-3 with bake. ##########"
#cd ./bake

#bake.py check 
#bake.py configure -e ns-3.36
#bake.py show 
#bake.py deploy

status=$?
if [ $status -ne 0 ]; then
    echo "Failed to deploy ns-3!"
    exit $status
fi

# Dummy process to keep container running
echo "########## Dummy process started! ##########"
tail -f /dev/null