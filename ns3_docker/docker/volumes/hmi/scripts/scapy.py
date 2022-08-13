#!/usr/bin/python3

from scapy.all import *
import logging
import time


HMI_IP = "123.100.30.1"
global known_mac_adresses
known_mac_adresses={}
#sniff(offline="tcpdump.pcap", prn=check_mitm(), filter='tcp or udp')
#pkts = sniff(offline="tcpdump.pcap",prn = check_mitm())

# 'Dec 29 10:00:01'
logging.basicConfig(filename='logs/scapy.log',format="%(asctime)s HMI scapy: %(levelname)s %(message)s", datefmt='%b %d %H:%M:%S', level=logging.DEBUG)
#logging.basicConfig(filename='logs/scapy.log',format='scapy %(levelname)s %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

def check_arp_spoof(pkt):
    ip_src = pkt[ARP].psrc
    mac = (pkt.hwsrc)
    print("check_arp_spoof")
    if not ip_src in known_mac_adresses:
        print("new entry")
        #add new entry
        known_mac_adresses[ip_src] = mac
        print(known_mac_adresses[ip_src], ip_src)
    else:
        #check if IP is already used by another mac adress
        print("warning log")
        if (known_mac_adresses[ip_src] != mac):
            log="%(srcip)s -> %(dstip)s "%{"srcip": pkt[ARP].psrc, "dstip": pkt[ARP].psrc}+"ARP-SPOOF-WARNING: "+mac+" and "+ known_mac_adresses[ip_src] 
            print(log)
            logging.warning(log)
    

def tcp_parse(pkt):
    #pkt.show()
    
    protocol_id=pkt.type
    if protocol_id==2054: #protocol is arp
        if (pkt[ARP].op == 1):
            arp_op="ARP-REQUEST"
        elif (pkt[ARP].op == 2):
            
            arp_op="ARP-REPLY"
            check_arp_spoof(pkt)
        else:
            arp_op="ARP-OTHER"
            check_arp_spoof(pkt)
          
        log="%(srcip)s -> %(dstip)s %(arp_op)s - %(summary)s" %{"srcip": pkt[ARP].psrc, "dstip": pkt[ARP].pdst, "arp_op": arp_op, "summary": pkt.summary()}
     
        if (pkt[ARP].pdst != HMI_IP) and (pkt[ARP].psrc != HMI_IP): 
            #so that hmi's firewall isn't logged
            print(log)
            logging.info(log)
 
    

pkts = sniff(filter="icmp or arp",prn=lambda x: tcp_parse(x))