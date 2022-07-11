#!/usr/bin/python3


import socket
import threading
import random

nodeIPs = ["123.100.10.1", "123.100.20.1", "123.100.30.1"] 

def inform_next_machine(ip):
    try:
        if random.randint(0,20) % 2 == 0:
            msg = "Start"
        else: 
            msg = "Failure"

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((ip, 5005))
        
        soc.send(msg.encode())
        ret_msg = soc.recv(1024).decode()
        print(ip + " responded: " + ret_msg)
    finally:
        print("Ending threat and closing connection with " + ip)
        soc.close()


def handle_conn(con, addr):
    m2_ip = "172.17.0.4"
    next_machine = ""
    ret_msg = "Recived your message!"
    
    try:
        # load message
        msg = con.recv(1024).decode()
        if not msg:
            con.close()
            return
        print(addr[0]+" sends: " + msg)
        
        # Send confirmation message back to Sender; Inform next machine to start working
        if addr[0] == "172.17.0.2":
            next_machine = m2_ip   
        elif addr[0] == nodeIPs[2]:
            next_machine = nodeIPs[3]    
        # ...

        # Send recive confirmation    
        con.send(ret_msg.encode())
        # Inform next machine to start
        thread = threading.Thread(target=inform_next_machine, args=(m2_ip,))
        thread.start()

    finally:
        print("Ending threat and closing connection with " + addr[0])
        con.close


def main():
    host = ''
    port = 5005 

    print("PLC -- Setting up socket...")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host,port))
    soc.listen()

    while True:
        print("PLC -- Waiting for connections...")
        con, addr = soc.accept()
        
        print("PLC -- Started threat with " + addr[0])
        thread = threading.Thread(target=handle_conn, args=(con, addr))
        thread.start()

    
main()