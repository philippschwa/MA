#!/usr/bin/python3


import socket
import threading
import random

# Node Configurations
nodeNames = ["m1", "m2", "m3", "m4", "plc", "attacker"]
nodeIPs = ["123.100.10.1", "123.100.10.2", "123.100.10.3",
           "123.100.10.4", "123.100.20.1", "123.100.30.1"]


def inform_machine(ip):
    
    try:
        msg = "Start"

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((ip, 5005))
        soc.send(msg.encode())
        ret_msg = soc.recv(1024).decode()
        print(ip + " responded: " + ret_msg)
    finally:
        print("Ending threat and closing connection with " + ip)
        soc.close()


def handle_conn(con, addr):
    
    next_machine = ""
    ret_msg = "Received your message!"

    try:
        # load message
        msg = con.recv(1024).decode()
        if not msg:
            con.close()
            return
        print(addr[0]+" sends: " + msg)
        # Send receive confirmation
        con.send(ret_msg.encode())
        
        # Send confirmation message back to Sender; Inform next machine to start working
        if addr[0] == nodeIPs[0] and msg == "m1 -- finished":
            next_machine = nodeIPs[1]
        elif addr[0] == nodeIPs[1] and msg == "m2 -- finished":
            next_machine = nodeIPs[2] 
        elif addr[0] == nodeIPs[2] and msg == "m3 -- finished":
            next_machine = nodeIPs[3]
        elif addr[0] == nodeIPs[3] and msg == "m4 -- finished":
            next_machine = nodeIPs[0]

        if next_machine != "":
            # Inform next machine to start their process
            thread = threading.Thread(target=inform_machine, args=(next_machine,))
            thread.start()
            asdf = "Informing next machine."
            con.send(asdf.encode())

    finally:
        print("Ending threat and closing connection with " + addr[0])
        con.close()


def main():
    host = ''
    port = 5005

    print("PLC -- Setting up socket...")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host, port))
    soc.listen()

    try:
        # inform m1 to start
        thread = threading.Thread(target=inform_machine, args=(nodeIPs[0],))
        thread.start()
        
        while True:
            print("PLC -- Waiting for connections...")
            con, addr = soc.accept()

            print("PLC -- Started threat with " + addr[0])
            thread = threading.Thread(target=handle_conn, args=(con, addr))
            thread.start()
    finally:
        soc.close()

main()
