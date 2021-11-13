#!/usr/bin/env python3

import socket
import sys
import os

FORMAT = 'utf-8'

def recvAll(sock, numBytes):
    recvBuff = ""
    tmpBuff = ""

    while len(recvBuff) < numBytes:
        tmpBuff = sock.recv(numBytes).decode(FORMAT)
        if not tmpBuff:
            break

        recvBuff += tmpBuff

    return recvBuff

def main(argv):
    if len(argv) != 3:
        print("USAGE: {} <SERVER_MACHINE> <SERVER_PORT>".format(argv[0]))
        sys.exit()

    serverAddr = argv[1]
    serverPort = int(argv[2])

    connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connSock.connect((serverAddr, serverPort))

    while True:
        serverDataBuff = ""
        serverDataSize = 0
        serverData = ""
        clientData = ""

        message = input("ftp> ").strip()

        if message.startswith("put"):
            fileName = message.replace("put", '').strip()
            
            if os.path.exists(fileName):
                fileObj = open(fileName, "r")
                clientData = message + "\n" + fileObj.read(65536)
                fileObj.close()
            else:
                print("ERROR: {} does not exist!".format(fileName))
                clientData = "Unsuccessful cmd -> {}".format(message) 

        else:
            clientData = message

        dataSizeStr = str(len(clientData))

        while len(dataSizeStr) < 10:
            dataSizeStr = "0" + dataSizeStr

        clientData = dataSizeStr + clientData
        numSent = 0

        while len(clientData) > numSent:
            numSent += connSock.send(clientData[numSent:].encode(FORMAT))

        serverDataBuff = recvAll(connSock, 10)
        
        if serverDataBuff:
            serverDataSize = int(serverDataBuff)
            serverData = recvAll(connSock, serverDataSize)

            print(serverData)

        if message == "quit":
            break
        elif message.startswith("put"):
            print("({} bytes transferred)\n".format(int(dataSizeStr)))
        else:
            print("\n({} bytes transferred)\n".format(int(serverDataSize)))

    connSock.close()

if __name__ == "__main__":
    main(sys.argv)