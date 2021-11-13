#!/usr/bin/env python3

import socket
import subprocess
import sys
import os

FORMAT = 'utf-8'
GOOD_MSG = "COMMAND SUCCESS"
BAD_MSG = "COMMAND FAILURE"

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

        while True:
            clientDataBuff = ""
            clientDataSize = 0
            clientMessage = ""
            serverData = ""
            cmdResult = GOOD_MSG

            clientDataBuff = recvAll(clientSock, 10)
            clientDataSize = int(clientDataBuff)

            clientMessage = str(recvAll(clientSock, clientDataSize))

            # Change value of server data to send based on client msg
            if clientMessage == "quit":
                serverData = "Goodbye!"
                pass

            elif clientMessage == "ls":
                data = subprocess.getstatusoutput("ls -l")

                if int(data[0]) == 0:
                    serverData = str(data[1])
                else:
                    cmdResult = BAD_MSG
                    serverData = BAD_MSG

            elif clientMessage.startswith("get"):
                fileName = clientMessage.replace("get", '').strip()

                if os.path.exists(fileName):
                    fileObj = open(fileName, "r")
                    serverData = fileObj.read(65536)
                    fileObj.close()
                else:
                    cmdResult = BAD_MSG
                    serverData = BAD_MSG
                
            elif clientMessage.startswith("put"):
                pass

            else:
                cmdResult = BAD_MSG
                serverData = BAD_MSG

            print("{}: {}".format(cmdResult, clientMessage))

            dataSizeStr = str(len(serverData))

            while len(dataSizeStr) < 10:
                dataSizeStr = "0" + dataSizeStr

            sendData = dataSizeStr + serverData
            numSent = 0

            while len(sendData) > numSent:
                numSent += clientSock.send(sendData[numSent:].encode(FORMAT))

            if clientMessage == "quit":
                break

        print("\nClient {} disconnected!\n".format(addr))
        clientSock.close()

if __name__ == "__main__":
    main(sys.argv)