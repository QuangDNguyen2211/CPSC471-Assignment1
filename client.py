#!/usr/bin/env python3

import socket
import sys

def main(argv):
    if len(argv) != 3:
        print("USAGE: {} <SERVER_MACHINE> <SERVER_PORT>".format(argv[0]))
        sys.exit()

    serverAddr = argv[1]
    serverPort = int(argv[2])

    connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connSock.connect((serverAddr, serverPort))

    while True:
        message = input("ftp> ")

        connSock.send(message.encode())

        if message.strip() == "quit":
            data = connSock.recv(1024).decode()
            break

    connSock.close()

if __name__ == "__main__":
    main(sys.argv)