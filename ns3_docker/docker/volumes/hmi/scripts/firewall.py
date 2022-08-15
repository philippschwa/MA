#!/usr/bin/python3

from scapy.all import *
import logging as log
import time


HMI_IP = "123.100.30.1"
global known_mac_adresses
known_mac_adresses = {}

# 'Dec 29 10:00:01'
log.basicConfig(filename='logs/scapy.log', format="%(asctime)s HMI scapy: %(levelname)s %(message)s",
                datefmt='%b %d %H:%M:%S', level=log.DEBUG)


def check_arp_spoof(pkt):
    print("Check ARP spoof.")

    ip_src = pkt[ARP].psrc
    ip_dest = pkt[ARP].pdst
    mac = (pkt.hwsrc)

    if not ip_src in known_mac_adresses:
        # add new entry
        known_mac_adresses[ip_src] = mac
        print(known_mac_adresses[ip_src], ip_src)
        pring("IP - MAC entry added.")
    else:
        # check if IP is already used by another mac adress
        if (known_mac_adresses[ip_src] != mac):
            print("IP already used by other MAC.")
            log.warning("%(srcip)s -> %(dstip)s ARP-SPOOF-WARNING: %(srcip)s had old_mac=%(old_mac)s new_mac=%(new_mac)s" %
                        {"srcip": ip_src, "dstip": ip_dest, "old_mac": known_mac_adresses[ip_src], "new_mac": mac})


def parse_packet(pkt):
    protocol_id = pkt.type
    
    print(pkt.summary())

    if protocol_id == 2054:  # protocol is arp
        if (pkt[ARP].op == 1):
            arp_op = "ARP-REQUEST"
        elif (pkt[ARP].op == 2):
            arp_op = "ARP-REPLY"
            check_arp_spoof(pkt)
        else:
            arp_op = "ARP-OTHER"
            check_arp_spoof(pkt)

        log_msg = "%(srcip)s -> %(dstip)s %(arp_op)s: %(summary)s" % {
            "srcip": pkt[ARP].psrc, "dstip": pkt[ARP].pdst, "arp_op": arp_op, "summary": pkt.summary()}
        
        if (pkt[ARP].pdst != HMI_IP) and (pkt[ARP].psrc != HMI_IP):
            # so that hmi's firewall isn't logged
            log.info(log_msg)

    elif protocol_id == 2048:  # protocol is icmp

        if (pkt[ICMP].type == 0):
            icmp_type = "ICMP-REPLY"
        elif (pkt[ICMP].type == 8):
            icmp_type = "ICMP-REQUEST"
        else:
            icmp_type = "ICMP-OTHER"

        log.info("%(srcip)s -> %(dstip)s %(icmp_type)s: %(summary)s" % {
            "srcip": pkt[IP].src, "dstip": pkt[IP].dst, "icmp_type": icmp_type, "summary": pkt.summary()})


#pkts = sniff(filter="icmp or arp", prn=lambda x: tcp_parse(x))
pkts = sniff(iface="eth0", prn=lambda x: parse_packet(x))
pkts.summary()