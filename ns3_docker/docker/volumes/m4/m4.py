#!/usr/bin/python3

import socket
import threading
import time
import random
import logging as log

PLC_IP = "123.100.20.1"
M4_IP = "123.100.10.4"
PLC_PORT = 5005
BUFFER_SIZE = 1024
PROCESS_TIME = 20
WAIT_TIME = 5


def clean_component():
    print("[m4] -- Starting cleaning process.")
    print("[m4] -- Equipping component & reading component id.")
    time.sleep(WAIT_TIME)

    print("[m4] -- Cleaning component.")
    time.sleep(PROCESS_TIME)

    if random.randint(0, 1000) % 100 < 98:
        print("[m4] -- Finished cleaning. Informing PLC.")
        log.info("%s --> %s: [m4] -- Finished cleaning. Informing PLC.", M4_IP, PLC_IP)
        return "set_result=True"
    else:
        print("[m4] -- Cleaning failed. Informing PLC.")
        log.error("%s --> %s: [m4] -- Cleaning failed. Informing PLC.", M4_IP, PLC_IP)
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
        print("[m4] -- Received message: " + msg)
        log.info("%s --> %s: [m4] -- Received message: %s", addr[0], M4_IP, msg)

        if addr[0] == PLC_IP and msg == "can_produce=True":
            ret_msg = clean_component()
            thread = threading.Thread(target=inform_plc, args=(ret_msg,))
            thread.start()
            # con.send(ret_msg.encode())
        else:
            print("[m4] -- ERROR: Invalid connection.")
    finally:
        con.close()


def main():
    # Setup logging
    log.basicConfig(filename='./sim/logs/m4.log', format='%(levelname)s %(asctime)s -- %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=log.DEBUG)
    log.info("[m4] -- Starting up. Waiting for connections.")

    host = ''

    print("[m4] -- Setting up socket...")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host, PLC_PORT))
    soc.listen()

    try:
        while True:
            print("[m4] -- Waiting for connections...")
            con, addr = soc.accept()

            print("[m4] -- Received connection from: " + addr[0])
            thread = threading.Thread(target=handle_conn, args=(con, addr))
            thread.start()
    finally:
        soc.close


main()
