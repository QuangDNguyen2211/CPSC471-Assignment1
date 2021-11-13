Daniel Nazeri <dnazeri@csu.fullerton.edu>
Kristofer Calma <calmakris@csu.fullerton.edu>
Quang Nguyen <quangdnguyen2211@csu.fullerton.edu>
Juan Ramirez Lopez <juanr2000@csu.fullerton.edu>
Nathan Vu <mr.nathanvu@csu.fullerton.edu>

* Programming language used: Python

* How to run the program:
  1. Open terminal in the program directory to run the server
  2. Run the server by type in this command line: python3 server.py <PORTNUMBER>
  3. Open a second terminal for the client side
  4. Run the client by type in this command line: python3 client.py <SERVER-MACHINE> <SERVER-PORT>
  5. After this the client side will print out ftp> to ask the user for commands
    - get <file-name>: let the user download that file from the server
    - put <file-name>: let the user upload that file to the server
    - ls: list all files on the server
    - quit: disconnect from the server and exit

* Anything special about our submission: No

* Protocol Design
The protocol that our group designed is similar to the File Transfer Protocol, which uses two TCP connections: a control and a data channel.

• What kinds of messages will be exchanged across the control channel?
->	After the TCP connection is established(control), the client can then send commands to the controls channel.
All the commands that the user can send are get, put, ls and quit

• How should the other side respond to the messages
->	For each command from the client to the server. The server will print out if the command success in what it tries to do, or did it fail.

• What sizes/formats will the messages have?
->	Because the Internet is a packet switched network, data will be split into multiple packets.

• What message exchanges have to take place in order to setup a file transfer channel?
->	The client needs to provide the server’s name and its port in order to establish a TCP connection with the FTP server.
An ephemeral connection will be established through which data for the command will be sent

• How will the receiving side know when to start/stop receiving the file?
->	The client will tell the server when to start/ stop receiving files

• How to avoid overflowing TCP buffers?
->	The buffer sizes define the amount of data that can be sent and not received before it is interrupted.
If too much data is sent, it will overrun the buffer and interrupts the transfer. Therefore, we use flow control to prevent this.
The flow control will stop the data transfer if the buffer is being overrun until it is empty
