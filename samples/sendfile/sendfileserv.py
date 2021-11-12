
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket

# The port on which to listen
listenPort = 5050

# The IPv4 on which to listen
listenServer = socket.gethostbyname(socket.gethostname())
print("Server is listening on: ", listenServer)

GET_MESSAGE = 'get'
DISCONNECT_MESSAGE = 'quit'

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind((listenServer, listenPort))

# Start listening on the socket
welcomeSock.listen()


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
		tmpBuff = sock.recv(numBytes).decode('utf-8')

		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff

	sock.send("File received".encode('utf-8'))

	return recvBuff
		
connected = True

# Accept connections forever
while connected:

	print("Waiting for connections...")

	# Accept connections
	clientSock, addr = welcomeSock.accept()

	print("Accepted connection from client: ", addr)

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

		if fileData == DISCONNECT_MESSAGE:
			print("Disconnecting connections...")
			connected = False

	# Close our side
	clientSock.close()
