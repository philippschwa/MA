#!/usr/bin/python3

import socket
import random
import time
import threading


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
        return "set_result=True"
    else:
        print("[m1] -- Leakeage test failed. Informing PLC.")
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
        print("[m1] -- Received message: " + msg)

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
    host = ''

    # wait for all containers to be set up
    time.sleep(10)

    print("[m1] -- Setting up socket.")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host, PLC_PORT))
    soc.listen()

    try:
        while True:
            print("[m1] -- Waiting for connections.")
            con, addr = soc.accept()

            print("[m1] -- Recieved connection from: " + addr[0])
            thread = threading.Thread(target=handle_conn, args=(con, addr))
            thread.start()

    finally:
        soc.close()


main()
