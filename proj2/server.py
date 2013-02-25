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
		print 'connected'
		#Loop on responses
		data = connection.recv(2000)
		if(data.startswith('GET')):
			if(data.startswith('GET /CHAT')):
				return_data = data.split('?')[1].split('&')
				tuples = []
				for r in return_data:
					r.split('=')			
			connection.send('hello')			
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

