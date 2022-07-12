#!/usr/bin/python3

import socket
import threading
import time
import random

PLC_IP = "123.100.20.1"
PLC_PORT = 5005
BUFFER_SIZE = 1024


def do_something():
    print("Starting with my process.")
    counter = 0
    while counter < 5:
        print("Processing xy")
        time.sleep(20)
        if random.randint(0, 1000) % 10 < 9:
            break
        counter += 1
        print("Process failed. Starting over")

    print("Process finished")
    return "m2 finished"


def handle_conn(con, addr):
    try:
        msg = con.recv(1024).decode()
        if not msg:
            con.close()
            return
        print(addr[0]+" sends: " + msg)

        if addr[0] == PLC_IP and msg == "Start":
            ret_msg = do_something()
            con.send(ret_msg.encode())
        # Im Moment werden nur "Start" Nachrichten gesendet - evtl noch überarbeiten
        elif addr[0] == PLC_IP and msg == "Failure":
            ret_msg = "Waiting for next order."
            con.send(ret_msg.encode())
        else:
            print("ERROR: Invalid connection.")
    finally:
        con.close


def main():
    host = ''
    port = 5005

    print("m2 -- Setting up socket...")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host, port))
    soc.listen()

    while True:
        print("m2 -- Waiting for connections...")
        con, addr = soc.accept()

        print("m2 -- starting threat with " + addr[0])
        thread = threading.Thread(target=handle_conn, args=(con, addr))
        thread.start()


main()
