#!/usr/bin/python3

import socket
import random
import time


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
    return "m1 finished"


def main():
    # create a socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        soc.connect((PLC_IP, PLC_PORT))

        # Send message
        msg = execute_process()
        print("Sending '%s' to %s" % (msg, PLC_IP))
        soc.send(msg.encode())

        # Print response
        msg = soc.recv(BUFFER_SIZE).decode()
        print("Recived: " + msg)

    finally:
        soc.close()
