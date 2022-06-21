#!/bin/bash

echo "########## Executing shell script ##########"
status=$?
if [ $status -ne 0 ]; then
    echo "Failed to start container!"
    exit $status
fi