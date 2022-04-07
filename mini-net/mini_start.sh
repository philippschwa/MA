#!/bin/bash
#Kommentar
echo "Inside mini_start!"

service openvswitch-switch start
#mn -c
mn --custom ./mininet/custom/topo-2sw-2host.py --topo mytopo --test pingall
#python3 test.py