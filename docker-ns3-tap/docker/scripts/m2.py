#!/usr/bin/python3


import socket
import threading
import time

def check_message(msg):
    if msg == "Start":
        print("Starting with my process.")
        time.sleep(20)
        print("Finished with my process.")
        return True
    elif msg == "Failure":
        print("Awaiting further messages.")
        return False
    else:
        print("Something went completly wrong.")
        return False


def handle_conn(con, addr):
    try:
        retval = False
        # load message
        msg = con.recv(1024).decode()
        if not msg:
            con.close()
            return
        print(addr[0]+" sends: " + msg)
        
        if addr[0] == "172.17.0.2":
            ret_msg = "Response to m1"
            print("Sending: " + ret_msg)
            con.send(ret_msg.encode())
        elif addr[0] == "172.17.0.3":
            retval = check_message(msg)
            
        
        if retval:
            # Eigentlich Inform next node
            ret_msg = "Process finished"
            print("Informing PLC: " + ret_msg)
            con.send(ret_msg.encode())
        else: 
            ret_msg = "Something went wrong"
            con.send(ret_msg.encode())
            
    finally:
        con.close


def main():
    host = ''
    port = 5005 

    print("m2 -- Setting up socket...")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host,port))
    soc.listen()

    while True:
        print("m2 -- Waiting for connections...")
        con, addr = soc.accept()
        
        print("m2 -- starting threat with " + addr[0])
        thread = threading.Thread(target=handle_conn, args=(con, addr))
        thread.start()

    
main()