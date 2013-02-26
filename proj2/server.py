#!/usr/bin/python
from socket import *
import sys
from thread import *

# Create a TCP/IP socket
sock = socket(AF_INET,SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 9020)
print >> sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(20)
#print >> sys.stderr, f.read()		

#initialize vars
chat_log = []
def new_connection(conn):
	connection = conn
    # Wait for a connection
	try:
		print 'connected'
		#Loop on responses
		data = connection.recv(2000)
		if(data.startswith('GET /CHAT')):
			return_data = data.split('?')[1].split('&')
			name = None
			content = None
			for r in return_data:
			 	temp = r.split('=')
				if temp[0].lower() == 'name':
					name = temp[1]
				if temp[0].lower() == 'line':
					content = str(temp[1]).split(' HTTP')[0]		
			# Just ake it put the contents into the chatlog.txt file and then they will be displayed nicely
			file = open('chatlog.txt', 'w')
			file.write(str(name)+': '+str(content)+'\n')
			file.close()
			file = open('chatlog.txt', 'r')
			connection.send(str(file.read()))	
			file.close()	
		elif(data.startswith('GET')):
			f = open('chat.html', 'r')
			connection.send(str(f.read()))	
			f.close()	
		
		connection.close()
		#sock.close()
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

