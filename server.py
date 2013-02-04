from socket import *
import sys
from thread import *

# Create a TCP/IP socket
sock = socket(AF_INET,SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 9020)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(5)
#initialize vars
chat_log = []
def new_connection(conn):
	connection = conn
    # Wait for a connection
	try:
		#Welcome
		connection.send("Welcome to Matt's Chat \r\n")
		#Loop on responses
		data = connection.recv(2000)
		while (data.startswith('adios') == False):
			print data
			processed_data = data.lower().strip()
			return_data = ""
			chatname = "";
			if(processed_data.startswith('help')):
				return_data = "help lists all of the commands and their syntax \n test: <text>test data</text> echoes your test data back to you \n name: <text>your name</text> sets your username \n get lists all of the contents of the chat \n push: <text>Content</text> adds a new line to the chat \n getrange # # will return the chat lines provided. \n adios quits the chat program\r\n"	
				connection.send(return_data)			
			elif(processed_data.startswith('test:')):
				return_data = data[5:].strip() + " \r\n"
				connection.send(return_data)
			elif(processed_data.startswith('name:')):
				chatname = data[5:].strip()
				return_data = "OK\r\n"				
				connection.send(return_data)
			elif(processed_data.startswith('push:')):
				if(chatname != ""):
					chat_log.append(chatname + ": " + data[5:])
					return_data = "OK\r\n"
					connection.send(return_data)
				else:
					connection.send("You need to give me your name first")
			elif(processed_data.startswith('getrange')):
				rangevals = data[8:]
				ranges = rangevals.split()
				if (int(ranges[0]) - 1 < 0 or int(ranges[1]) > len(chat_log)):
					return_data = "Out of range \r\n"
				else:
					for i in range(int(ranges[0]) - 1, int(ranges[1])):
						return_data += chat_log[i] + " \r\n"
				connection.send(return_data)
			elif(processed_data.startswith('get')):
				return_data = "Chat Log \r\n"
				for item in chat_log:
					return_data += item+" \r\n"
				connection.send(return_data)
			else:
				return_data ="Invalid Command"
				connection.send(return_data)
			data = connection.recv(2000)

		if(data.startswith('adios')):
			connection.send("OK\r\n")
			connection.shutdown()
			connection.close()
	except:
        # Clean up the connection
		connection.close()
		#sock.close()
try:
	while(True):
		print >>sys.stderr, 'waiting for a connection'
		connection, client_address = sock.accept()
		start_new_thread(new_connection,(connection,))
except:
	sock.close()		

