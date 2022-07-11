#!/usr/bin/python3

#####
#
# PLC Script. Recives messages from all 4 machines and handels the messages.
#
#####

import socket
import time
import threading
from _thread import *


def check_m1_msg(msg):
    print("check_m1_msg()")
    if msg == "Finished":
        return "Informing m2"
    else: 
        return "What did go wrong?"

def send_message(msg, dest_ip):
    tmp_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tmp_soc.connect((dest_ip, PORT))
    tmp_soc.send(msg.encode())
    time.sleep(10)
    tmp_soc.close()

def handle_connection(con, src_ip):
    
    try:
        print("handle_connection()")
        ret_msg = "Fail."
        # msg eher erst im funktionsteil holen
        msg = con.recv(BUFFER_SIZE).decode()
        if not msg:
            con.close()
            return
        if src_ip == "172.17.0.2":
            print("Recived: " + msg)
            #ret_msg = check_m1_msg(msg)
            ret_msg = "Response m1"
            print("Sending: " + ret_msg)
            con.send(ret_msg.encode())
            con.close()
            # test
            data = "You can start now."
            start_new_thread(send_message, (data, "172.17.0.4"))
        
        elif src_ip == "172.17.0.4":
            print("Recived: " + msg)
            ret_msg = "Response m2"
            print("Sending: " + ret_msg)
            con.send(ret_msg.encode())
            con.close()
    finally:
        con.close()
    


def main():
    print("main()")
    #nodeNames = ["node1", "node2", "attacker"]
    #nodeIPs = ["123.100.10.1", "123.100.20.1", "123.100.30.1"]

    global PORT 
    global BUFFER_SIZE
    global soc
    PORT = 5005
    BUFFER_SIZE = 1024

    print("Creating Socket listening on Port 5005.")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind(('', PORT))
    soc.listen()

    try:
        print("main() --- Entering loop.") 
        while True:
            # wait for connections 
            con, addr = soc.accept()
            print("Incoming connection from: " + addr[0])
            # handle connection in new thread
            start_new_thread(handle_connection, (con, addr[0]))
            
    finally:
        soc.close()


if __name__ == '__main__':
    main()