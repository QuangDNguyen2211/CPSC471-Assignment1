#!/usr/bin/env python3

import socket
import sys

def recvAll(sock, numBytes):
    recvBuff = ""
    tmpBuff = ""

    while len(recvBuff) < numBytes:
        tmpBuff = sock.recv(numBytes)

        if not tmpBuff:
            break

        recvBuff += tmpBuff

    return recvBuff

def main(argv):
    if len(argv) != 2:
        print("USAGE: {} <PORT_NUMBER>".format(argv[0]))
        sys.exit()

    listenPort = int(argv[1])

    welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    welcomeSock.bind(('', listenPort))
    welcomeSock.listen(1)
    
    while True:
        print("Waiting for connections...")

        clientSock, addr = welcomeSock.accept()
        print("Client {} connected!\n".format(addr))

        serverMessage = ""

        while True:
            data = clientSock.recv(1024).decode()
            if not data:
                break

            print("Client says: {}".format(data))

            if str(data) == "quit":
                serverMessage = "SUCCESS"
                clientSock.send(serverMessage.encode())

        print("\nClient {} disconnected!\n".format(addr))
        clientSock.close()


if __name__ == "__main__":
    main(sys.argv)