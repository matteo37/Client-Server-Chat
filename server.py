import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
testing = "getrangeasdfadsfs"
print >>sys.stderr, testing.startswith('getrange')
# Bind the socket to the port
server_address = ('localhost', 9020)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
chat_log = []
chatname = "";
while True:
    # Wait for a connection
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = sock.accept()
	
	try:
		print >>sys.stderr, 'connection from', client_address
		
        # Receive the data in small chunks and retransmit it
		while True:
			#print >>sys.stderr, 'start', 
			data = connection.recv(16)
			processed_data = data.lower()
			print >>sys.stderr, processed_data

			return_data = ""
			if(processed_data.startswith('adios')):
				connection.close()
			elif(processed_data.startswith('help')):
				return_data = "\n help lists all of the commands and their syntax \n test: <text>test data</text> echoes your test data back to you \n name: <text>your name</text> sets your username \n get lists all of the contents of the chat \n push <text>Content</text> adds a new line to the chat \n getrange # # will return the chat lines provided. \n adios quits the chat program"				
			elif(processed_data.startswith('test:')):
				return_data = processed_data[5:].strip()
			elif(processed_data.startswith('name:')):
				chatname = processed_data[5:].strip()
				return_data = "OK"				
			elif(processed_data.startswith('push:')):
				chat_log.append(chatname + ": " + processed_data[5:].strip())
				return_data = "OK"
			elif(processed_data.startswith('getrange')):
				rangevals = processed_data[8:]
				ranges = rangevals.split()
				if (int(ranges[0]) - 1 < 0 or int(ranges[1]) > len(chat_log)):
					return_data = "Out of range"
				else:
					for i in range(int(ranges[0]) - 1, int(ranges[1])):
						return_data += chat_log[i] + " \n"
			elif(processed_data.startswith('get')):
				return_data = "Chat Log \n"
				for item in chat_log:
					return_data += item+" \n"
			else:
				return_data ="Invalid Command"
			if return_data != "":
				connection.send(return_data)
				return_data = "";
			else:
				print >>sys.stderr, 'no more data from', client_address
				break
			#print >>sys.stderr, 'finish', 

	finally:
        # Clean up the connection
		connection.close()