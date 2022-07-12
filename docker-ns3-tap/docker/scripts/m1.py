#!/usr/bin/python3

import socket
import random
import time
import threading


PLC_IP = "123.100.20.1"
PLC_PORT = 5005
BUFFER_SIZE = 1024
PROCESS_TIME = 20


def execute_process():
    print("m1 -- Starting process.")
    counter = 0
    while counter < 5:
        print("Testing pressure.")
        time.sleep(PROCESS_TIME)
        if random.randint(0, 1000) % 10 < 9:
            break
        counter += 1
        print("Process failed. Starting over...")

    print("m1 -- Process finished.")
    return "m1 -- finished"


def inform_plc(msg):
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((PLC_IP, 5005))
        soc.send(msg.encode())
        ret_msg = soc.recv(1024).decode()
        print(PLC_IP + " responded: " + ret_msg)
    finally:
        print("Ending threat and closing connection with " + PLC_IP)
        soc.close()


def handle_conn(con, addr):
    try:
        msg = con.recv(1024).decode()
        if not msg:
            con.close()
            return
        print(addr[0]+" sends: " + msg)

        if addr[0] == PLC_IP and msg == "Start":
            ret_msg = execute_process()
            thread = threading.Thread(target=inform_plc, args=(ret_msg,))
            thread.start()
            #con.send(ret_msg.encode())
        # Im Moment werden nur "Start" Nachrichten gesendet - evtl noch überarbeiten
        elif addr[0] == PLC_IP and msg == "Failure":
            ret_msg = "Waiting for next order."
            con.send(ret_msg.encode())
        else:
            print("ERROR: Invalid connection.")
    finally:
        con.close()


def main():
    host = ''

    print("m1 -- Setting up socket...")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host, PLC_PORT))
    soc.listen()

    try:
        while True:
            print("m2 -- Waiting for connections...")
            con, addr = soc.accept()

            print("m2 -- starting threat with " + addr[0])
            thread = threading.Thread(target=handle_conn, args=(con, addr))
            thread.start()

    finally:
        soc.close()

main()