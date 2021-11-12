# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************

import socket

# Server address
serverAddr = socket.gethostbyname(socket.gethostname())
print("Client is listening on: ", serverAddr)

# Server port
serverPort = 5050

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

# The number of bytes sent
numSent = 0

# The file data
fileData = None

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


# Keep sending until all is sent
while True:

    user_input = input('fpt> ')

    # server_input = connSock.recv(1024).decode(FORMAT)
    # print("Received server input: ", server_input)

    if user_input.find(PUT_CMD) != -1:

        # The name of the file
        fileName = user_input.replace(PUT_CMD, '').strip()
        print("--> fileName: ", fileName)

        connSock.send(user_input.encode(FORMAT))

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
                numSent += connSock.send(fileData[numSent:].encode(FORMAT))

        # The file has been read. We are done
        else:
            break

        print("Client done sending file")
        fileObj.close()
        print("Sent ", numSent, " bytes.")

    elif user_input.find(GET_CMD) != -1:

        connSock.send(user_input.encode(FORMAT))

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
        fileSizeBuff = recvAll(connSock, 10)

        if fileSizeBuff:
            # Get the file size
            fileSize = int(fileSizeBuff)

            print("The file size is: ", fileSize)

            # Get the file data
            fileData = recvAll(connSock, fileSize)

            print("The file data is:\n", '"', fileData, '"\n')

    elif user_input.find(LIST_CMD) != -1:

        connSock.send(user_input.encode(FORMAT))

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
        fileSizeBuff = recvAll(connSock, 10)

        if fileSizeBuff:
            # Get the file size
            fileSize = int(fileSizeBuff)

            print("The file size is: ", fileSize)

            # Get the file data
            fileData = recvAll(connSock, fileSize)

            print("The file data is:\n", '"', fileData, '"\n')

    elif user_input.find(QUIT_CMD) != -1:

        connSock.send(user_input.encode(FORMAT))
        break

    else:
        break

# Close the socket and the file
print("Disconnecting connections from Client")
connSock.close()
