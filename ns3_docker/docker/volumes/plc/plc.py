#!/usr/bin/python3

import socket
import threading
import logging as log
import time


IP = "123.100.20.1"
NAME = "PLC"

# Node Configurations
nodeNames = ["M1", "M2", "M3", "M4"]
nodeIPs = ["123.100.10.1", "123.100.10.2", "123.100.10.3", "123.100.10.4"]


def inform_machine(next_ip):
    try:
        print("[PLC] -- Informing next machine.")
        log.info("%s %s -> %s: Informing next machine.", NAME, IP, next_ip)
        msg = "can_produce=True"

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((next_ip, 5005))
        soc.send(msg.encode())
    
    except ConnectionError:
        log.error("%s %s -> %s: Machine not reachable. Retrying in 5 seconds.", NAME, IP, next_ip)
        time.sleep(5)
        inform_machine(msg)

    finally:
        print("[PLC] -- Closing connection with " + next_ip)
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
        log.info("%s %s -> %s: Received message: %s", NAME, addr[0], IP, msg)
        
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
                log.info("%s %s -> %s: Process finished. Starting with next component.", NAME, IP, nodeIPs[0]) 
                next_machine = nodeIPs[0] 

        # If error message received, PLC informs technician and tells m1 to start with the next component
        elif msg == "set_result=False":
            print("[PLC] -- Received Error Code. Discarding component and informing technician.")
            log.error("%s %s -> %s: Received error. Discarding component and informing technician.", NAME, addr[0], IP)
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
    log.basicConfig(filename='./src/logs/plc.log', format='machinelog %(levelname)s %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=log.DEBUG)
    log.info("%s %s -> %s: Starting up."%(NAME, IP, IP))
    
    # Sleep, to give other containers the chance to start up
    time.sleep(30)
    log.info("%s %s -> %s: Waited 30 seconds.", NAME, IP, IP)
    host = ''
    port = 5005

    

    print("[PLC] -- Setting up socket.")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host, port))
    soc.listen()

    try:
        # inform m1 to start
        
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
