# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket
import subprocess
import os

# The IPv4 on which to listen
listenServer = socket.gethostbyname(socket.gethostname())
print("Server is listening on: ", listenServer)

# The port on which to listen
listenPort = 5050

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind((listenServer, listenPort))

# Start listening on the socket
welcomeSock.listen(1)

# Accept connections
clientSock, addr = welcomeSock.accept()
print("Accepted connection from client: ", addr)

PUT_CMD = 'put'
GET_CMD = 'get'
QUIT_CMD = 'quit'
LIST_CMD = 'ls'
FORMAT = 'utf-8'


# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************

def recvAll(sock, numBytes):
    # The buffer
    recvBuff = ""

    # The temporary buffer
    tmpBuff = ""

    # Keep receiving till all is received
    while len(recvBuff) < numBytes:

        # Attempt to receive bytes
        tmpBuff = sock.recv(numBytes).decode(FORMAT)

        # The other side has closed the socket
        if not tmpBuff:
            break

        # Add the received bytes to the buffer
        recvBuff += tmpBuff

    return recvBuff


# Accept connections forever
while True:

    print("Waiting for connections...")

    client_input = clientSock.recv(1024).decode(FORMAT)
    print("Received client input: ", client_input)

    if client_input.find(PUT_CMD) != -1:

        # The buffer to all data received from the
        # the client.
        fileData = ""

        # The temporary buffer to store the received
        # data.
        recvBuff = ""

        # The size of the incoming file
        fileSize = 0

        # The buffer containing the file size
        fileSizeBuff = ""

        # Receive the first 10 bytes indicating the
        # size of the file
        fileSizeBuff = recvAll(clientSock, 10)

        if fileSizeBuff:
            # Get the file size
            fileSize = int(fileSizeBuff)

            print("The file size is: ", fileSize)

            # Get the file data
            fileData = recvAll(clientSock, fileSize)

            print("The file data is:\n", '"', fileData, '"\n')

    elif client_input.find(GET_CMD) != -1:

        # The name of the file
        fileName = client_input.replace(GET_CMD, '').strip()
        print("--> fileName: ", fileName)

        # clientSock.send(PUT_CMD.encode(FORMAT))

        # Open the file
        fileObj = open(fileName, "r")

        # Read 65536 bytes of data
        fileData = fileObj.read(65536)

        # Make sure we did not hit EOF
        if fileData:

            # Get the size of the data read
            # and convert it to string
            dataSizeStr = str(len(fileData))

            # Prepend 0's to the size string
            # until the size is 10 bytes
            while len(dataSizeStr) < 10:
                dataSizeStr = "0" + dataSizeStr

            # Prepend the size of the data to the
            # file data.
            fileData = dataSizeStr + fileData

            # The number of bytes sent
            numSent = 0

            # Send the data!
            while len(fileData) > numSent:
                numSent += clientSock.send(fileData[numSent:].encode(FORMAT))

        # The file has been read. We are done
        else:
            break

        print("Server done sending file")
        fileObj.close()
        print("Sent ", numSent, " bytes.")

    elif client_input.find(LIST_CMD) != -1:

        for line in subprocess.getstatusoutput('ls'):
            print("lists files on the server", line)

        # Get the size of the data read
        # and convert it to string
        dataSizeStr = str(len(str(line)))

        # Prepend 0's to the size string
        # until the size is 10 bytes
        while len(dataSizeStr) < 10:
            dataSizeStr = "0" + dataSizeStr

        # Prepend the size of the data to the
        # file data.
        fileData = dataSizeStr + line

        # The number of bytes sent
        numSent = 0

        # Send the data!
        while len(fileData) > numSent:
            numSent += clientSock.send(fileData[numSent:].encode(FORMAT))

    elif client_input.find(QUIT_CMD) != -1:

        break

    else:

        break

# Close our side
print("Disconnecting connections from Server")
clientSock.close()
