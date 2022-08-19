#!/usr/bin/python3

from scapy.all import *
import logging as log
import time

global known_mac_adresses
known_mac_adresses = {}

# 'Dec 29 10:00:01'
log.basicConfig(filename='arp.log', format="%(asctime)s NetworkMonitoring arp-sniffer: %(levelname)s %(message)s",
                datefmt='%b %d %H:%M:%S', level=log.DEBUG)


def check_arp_spoof(pkt, arp_op):
    print("Check ARP spoof.")

    ip_src = pkt[ARP].psrc
    ip_dest = pkt[ARP].pdst
    mac = (pkt.hwsrc)

    if not ip_src in known_mac_adresses:
        # add new entry to known adresses
        known_mac_adresses[ip_src] = mac
        log.info("%(srcip)s -> %(dstip)s %(arp_op)s: %(summary)s" % {"srcip": ip_src, "dstip": ip_dest, "arp_op": arp_op, "summary": pkt.summary()})
        print("Unknown IP. New entry added: " + ip_src, mac )
    else:
        # check if IP is already used by another mac adress
        if (known_mac_adresses[ip_src] != mac):
            print("IP already used by other MAC. Potential ARP Spoof detected.")
            log.warning("%(srcip)s -> %(dstip)s ARP-SPOOF-WARNING: %(srcip)s had old_mac=%(old_mac)s new_mac=%(new_mac)s" %
                        {"srcip": ip_src, "dstip": ip_dest, "old_mac": known_mac_adresses[ip_src], "new_mac": mac})


def parse_packet(pkt):
    protocol_id = pkt.type

    # check if protocol is arp
    if protocol_id == 2054:
        # If ARP Reques -> log request
        if (pkt[ARP].op == 1):
            arp_op = "ARP-REQUEST"
            print(str(pkt[ARP].op) + " --- "+pkt.summary())
            log.info("%(srcip)s -> %(dstip)s %(arp_op)s: %(summary)s" % {"srcip": pkt[ARP].psrc, "dstip": pkt[ARP].pdst, "arp_op": arp_op, "summary": pkt.summary()})
        
        # If ARP Reply -> check for ARP Spoofing
        elif (pkt[ARP].op == 2):
            arp_op = "ARP-REPLY"
            print(str(pkt[ARP].op) + " --- "+pkt.summary())
            check_arp_spoof(pkt, arp_op)
        else:
            arp_op = "ARP-OTHER"
            check_arp_spoof(pkt, arp_op)    


print("ARP sniffer started.")
pkts = sniff(iface="br-hmi", filter="arp", prn=lambda x: parse_packet(x))
#pkts = sniff(iface="eth0", filter="icmp and arp", prn=lambda x: parse_packet(x))
#pkts = sniff(prn=lambda x: parse_packet(x))
#pkts.summary()
