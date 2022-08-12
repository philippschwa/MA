#!/usr/bin/python3

#!/usr/bin/python3

import socket
import random
import time
import threading
import logging as log


PLC_IP = "123.100.20.1"
HMI_IP = "123.100.10.1"
PLC_PORT = 22
BUFFER_SIZE = 1024

def perform_leakage_test():
    print("[hmi] -- Starting leakage test.")
    print("[hmi] -- Equiping component & reading component id.")
    time.sleep(WAIT_TIME)

    ret_msg = ""

    print("[hmi] -- Testing for leakage.")
    
    time.sleep(PROCESS_TIME)

    if random.randint(0, 1000) % 100 < 98:
        print("[hmi] -- Finished leakage test. Informing PLC.")
        log.info("HMI %s -> %s: Finished leakage test. Informing PLC.", HMI_IP, PLC_IP)
        return "set_result=True"
    else:
        print("[hmi] -- Leakeage test failed. Informing PLC.")
        log.error("HMI %s -> %s: Leakeage test failed. Informing PLC.", HMI_IP, PLC_IP)
        return "set_result=False"


def inform_plc(msg):
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((PLC_IP, 5005))
        soc.send(msg.encode())
    
    except ConnectionError:
        #time.sleep(5)
        #inform_machine(ip)
        log.error("HMI %s -> %s: PLC not reachable.", HMI_IP, PLC_IP)
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
        print("[hmi] -- Received message: " + msg)
        log.info("HMI %s -> %s: Received message: %s", addr[0], HMI_IP, msg)

        if addr[0] == PLC_IP and msg == "can_produce=True":
            ret_msg = perform_leakage_test()
            thread = threading.Thread(target=inform_plc, args=(ret_msg,))
            thread.start()
            # con.send(ret_msg.encode())
        else:
            print("[hmi] -- ERROR: Invalid connection.")
    finally:
        con.close()


def main():
    # Setup logging
    log.basicConfig(filename='./sim/logs/hmi.log', format='machinelog %(levelname)s %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=log.DEBUG)
    log.info("HMI %s -> %s: Starting up. Waiting for connections."%(HMI_IP, HMI_IP))
    host = ''

    print("[hmi] -- Setting up socket.")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host, PLC_PORT))
    soc.listen()

    try:
        while True:
            print("[hmi] -- Waiting for connections.")
            con, addr = soc.accept()

            print("[hmi] -- Received connection from: " + addr[0])
            thread = threading.Thread(target=handle_conn, args=(con, addr))
            thread.start()

    finally:
        soc.close()


main()
