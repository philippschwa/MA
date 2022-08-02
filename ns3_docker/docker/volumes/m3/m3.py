#!/usr/bin/python3

import socket
import threading
import time
import random
import logging as log

PLC_IP = "123.100.20.1"
M3_IP = "123.100.10.3"
PLC_PORT = 5005
BUFFER_SIZE = 1024
PROCESS_TIME = 20
WAIT_TIME = 5


def label_component():
    print("[m3] -- Starting labeling process.")
    print("[m3] -- Equiping component & reading component id.")
    time.sleep(WAIT_TIME)

    print("[m3] -- Labeling component.")
    time.sleep(PROCESS_TIME)

    if random.randint(0, 1000) % 100 < 98:
        print("[m3] -- Finished labeling. Informing PLC.")
        log.info("%s --> %s: [m3] -- Finished labeling. Informing PLC.", M3_IP, PLC_IP)
        return "set_result=True"
    else:
        print("[m3] -- Labeling failed. Informing PLC.")
        log.error("%s --> %s: [m3] -- Leakeage test failed. Informing PLC.", M3_IP, PLC_IP)
        return "set_result=False"


def inform_plc(msg):
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((PLC_IP, 5005))
        soc.send(msg.encode())
    finally:
        soc.close()


def handle_conn(con, addr):
    try:
        msg = con.recv(1024).decode()
        if not msg:
            con.close()
            return
        print("[m3] -- Received message: " + msg)
        log.info("%s --> %s: [m3] -- Received message: %s", addr[0], M3_IP, msg)

        if addr[0] == PLC_IP and msg == "can_produce=True":
            ret_msg = label_component()
            thread = threading.Thread(target=inform_plc, args=(ret_msg,))
            thread.start()
            # con.send(ret_msg.encode())
        else:
            print("[m3] -- ERROR: Invalid connection.")
    finally:
        con.close()


def main():
    # Setup logging
    log.basicConfig(filename='logs/plc.log', format='%(levelname)s %(asctime)s -- %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=log.DEBUG)

    host = ''

    # wait for all containers to be set up
    time.sleep(10)

    print("[m3] -- Setting up socket.")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host, PLC_PORT))
    soc.listen()

    try:
        while True:
            print("[m3] -- Waiting for connections.")
            con, addr = soc.accept()

            print("[m3] -- Received connection from: " + addr[0])
            thread = threading.Thread(target=handle_conn, args=(con, addr))
            thread.start()
    finally:
        soc.close


main()
