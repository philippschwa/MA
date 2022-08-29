#!/usr/bin/python3

import socket
import random
import time
import threading
import logging as log


NAME="M1"
IP = "123.100.10.1"
PLC_IP = "123.100.20.1"
PLC_PORT = 5005
BUFFER_SIZE = 1024
PROCESS_TIME = 20
WAIT_TIME = 5


def perform_leakage_test():
    print("[m1] -- Starting leakage test.")
    print("[m1] -- Equiping component & reading component id.")
    
    time.sleep(WAIT_TIME)
    ret_msg = ""

    print("[m1] -- Testing for leakage.")
    time.sleep(PROCESS_TIME)

    if random.randint(0, 1000) % 100 < 98:
        print("[m1] -- Finished leakage test. Informing PLC.")
        log.info("%s %s -> %s: Finished leakage test. Informing PLC.", 
        NAME, IP, PLC_IP)
        return "set_result=True"
    else:
        print("[m1] -- Leakeage test failed. Informing PLC.")
        log.error("%s %s -> %s: Leakeage test failed. Informing PLC.", 
        NAME, IP, PLC_IP)
        return "set_result=False"


def inform_plc(msg):
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((PLC_IP, PLC_PORT))
        soc.send(msg.encode())
    
    except ConnectionError:
        log.error("%s %s -> %s: PLC not reachable.", NAME, IP, PLC_IP)
        time.sleep(5)
        inform_plc(msg)

    finally:
        soc.close()


def handle_conn(con, addr):
    try:
        msg = con.recv(1024).decode()
        if not msg:
            con.close()
            return
        print("[m1] -- Received message: " + msg)
        log.info("%s %s -> %s: Received message: %s"%(NAME, addr[0], IP, msg))

        if addr[0] == PLC_IP and msg == "can_produce=True":
            ret_msg = perform_leakage_test()
            thread = threading.Thread(target=inform_plc, args=(ret_msg,))
            thread.start()
            # con.send(ret_msg.encode())
        else:
            print("[m1] -- ERROR: Invalid connection.")
    finally:
        con.close()


def main():
    # Setup logging
    log.basicConfig(filename='./src/logs/m1.log', format='machinelog %(levelname)s %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=log.DEBUG)
    log.info("%s %s -> %s: Starting up. Waiting for connections."%(NAME, IP, IP))
    host = ''

    print("[m1] -- Setting up socket.")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host, PLC_PORT))
    soc.listen()

    try:
        while True:
            print("[m1] -- Waiting for connections.")
            con, addr = soc.accept()

            print("[m1] -- Received connection from: " + addr[0])
            thread = threading.Thread(target=handle_conn, args=(con, addr))
            thread.start()

    finally:
        soc.close()


main()
