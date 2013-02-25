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
#initialize vars
chat_log = []
def new_connection(conn):
	connection = conn
    # Wait for a connection
	try:
		#Loop on responses
		data = connection.recv(2000)
		if(processed_data.startswith('help')):
			connection.send(return_data)			
		elif(processed_data.startswith('test:')):
			return_data = data[5:].strip() + " \r\n"
			connection.send(return_data)
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

