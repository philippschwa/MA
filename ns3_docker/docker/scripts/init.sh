#!/bin/bash

echo "########## Executing deploy script! ##########"
status=$?
if [ $status -ne 0 ]; then
    echo "Failed to execute deploy script!"
    exit $status
fi

sleep 5
while 1:
do 
python3 ./sim/*.py
done

echo "hallo warum wird hier nichts erkannt.s"



# Dummy process to keep container running
echo "########## Dummy process started! ##########"
tail -f /dev/null