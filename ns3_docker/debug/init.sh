#!/bin/bash

echo "########## Executing deploy script! ##########"
status=$?
if [ $status -ne 0 ]; then
    echo "Failed to execute deploy script!"
    exit $status
fi

# Dummy process to keep container running
echo "########## Dummy process started! ##########"
tail -f /dev/null