#!/usr/bin/python3


import socket
import time
import random

nodeNames = ["node1", "node2", "attacker"]
nodeIPs = ["123.100.10.1", "123.100.20.1", "123.100.30.1"]

TCP_PORT = 5005
BUFFER_SIZE = 1024

# create a socket
soc = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

counter = random.randint(0,20)
try:
    soc.connect(('172.17.0.3', TCP_PORT))

    if counter % 2 == 0:
        data = "Finished."
    else:
        data = "Error."

    # Send message
    print("Sending: " + data)
    soc.send(data.encode())

    # Print recived message
    msg = soc.recv(BUFFER_SIZE).decode()
    print("Recived: " + msg)

finally:
    soc.close()
