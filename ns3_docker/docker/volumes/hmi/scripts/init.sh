#!/bin/bash

#service ssh start

status=$?
if [ $status -ne 0 ]; then
    echo "Failed to execute deploy script!"
    exit $status
fi

# Dummy process to keep container running
tail -f /dev/null