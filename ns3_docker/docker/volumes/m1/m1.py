#!/usr/bin/python3

import socket
import random
import time
import threading
import logging as log


PLC_IP = "123.100.20.1"
M1_IP = "123.100.10.1"
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
        log.info("M1 %s -> %s: Finished leakage test. Informing PLC.", M1_IP, PLC_IP)
        return "set_result=True"
    else:
        print("[m1] -- Leakeage test failed. Informing PLC.")
        log.error("M1 %s -> %s: Leakeage test failed. Informing PLC.", M1_IP, PLC_IP)
        return "set_result=False"


def inform_plc(msg):
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((PLC_IP, 5005))
        soc.send(msg.encode())
    
    except ConnectionError:
        #time.sleep(5)
        #inform_machine(ip)
        log.error("M1 %s -> %s: PLC not reachable.", M1_IP, PLC_IP)
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
        log.info("M1 %s -> %s: Received message: %s", addr[0], M1_IP, msg)

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
    log.basicConfig(filename='./sim/logs/m1.log', format='machinelog %(levelname)s %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=log.DEBUG)
    log.info("M1 123.100.10.1 -> 123.100.10.1: Starting up. Waiting for connections.")
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
