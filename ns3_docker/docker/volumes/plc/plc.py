#!/usr/bin/python3


import socket
import threading
import logging as log
import time

# Node Configurations
nodeNames = ["m1", "m2", "m3", "m4", "plc", "attacker"]
nodeIPs = ["123.100.10.1", "123.100.10.2", "123.100.10.3",
           "123.100.10.4", "123.100.20.1", "123.100.30.1"]


def inform_machine(ip):
    try:
        print("[PLC] -- Informing next machine.")
        log.info("%s --> %s: [PLC] -- Informing next machine.", nodeIPs[4], ip)
        msg = "can_produce=True"

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((ip, 5005))
        soc.send(msg.encode())

    finally:
        print("[PLC] -- Closing connection with " + ip)
        soc.close()


def handle_conn(con, addr):
    
    next_machine = ""

    try:
        # load message
        msg = con.recv(1024).decode()
        if not msg:
            con.close()
            return
        print("[PLC] -- Received message: " + msg)
        log.info("%s --> %s: [PLC] -- Received message: %s", addr[0], nodeIPs[4], msg)
        
        # Inform next machine to start working
        if msg == "set_result=True":
            if addr[0] == nodeIPs[0]:
                next_machine = nodeIPs[1]
            elif addr[0] == nodeIPs[1]:
                next_machine = nodeIPs[2] 
            elif addr[0] == nodeIPs[2]:
                next_machine = nodeIPs[3]
            elif addr[0] == nodeIPs[3]:
                print("[PLC] -- Process finished. Starting with next component.")
                log.info("[PLC] Process finished. Starting with next component.") #############################################
                next_machine = nodeIPs[0] 

        # If error message received, PLC informs technician and tells m1 to start with the next component
        elif msg == "set_result=False":
            print("[PLC] -- Recived Error Code. Discarding component and informing technician.")
            log.error("%s --> %s: [PLC] -- Recived error. Discarding component and informing technician", addr[0], nodeIPs[4]) #############################################
            time.sleep(5)
            print("[PLC] -- Informing machine 1.")
            next_machine = nodeIPs[0]

        if next_machine != "":
            # Inform next machine to start with their process
            thread = threading.Thread(target=inform_machine, args=(next_machine,))
            thread.start()
        
    finally:
        print("[PLC] -- Closing connection with " + addr[0])
        con.close()


def main():
    # Setup logging
    log.basicConfig(filename='./sim/logs/plc.log', format='%(levelname)s %(asctime)s -- %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=log.DEBUG)

    host = ''
    port = 5005

    print("[PLC] -- Setting up socket.")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host, port))
    soc.listen()

    try:
        # inform m1 to start
        time.sleep(15)
        print("[PLC] -- Informing machine 1")
        thread = threading.Thread(target=inform_machine, args=(nodeIPs[0],))
        thread.start()
        
        while True:
            print("[PLC] -- Waiting for connections.")
            con, addr = soc.accept()

            print("[PLC] -- Received connection from: " + addr[0])
            thread = threading.Thread(target=handle_conn, args=(con, addr))
            thread.start()
    finally:
        soc.close()



if __name__ == '__main__':
    main()
