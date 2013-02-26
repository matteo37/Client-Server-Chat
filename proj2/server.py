from socket import socket, AF_INET, SOCK_STREAM
from thread import start_new_thread
# Create a TCP/IP socket

sock = socket(AF_INET,SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 9020)
print 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(20)
f = open('chat.html', 'r')
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
			tuples = []
			for r in return_data:
				r.split('=')		
			connection.send("working")	
		elif(data.startswith('GET')):
			connection.send(str(f.read()))		
	except:
        # Clean up the connection
		connection.close()
		#sock.close()
try:
	while(True):
		print 'waiting for a connection'
		connection, client_address = sock.accept()
		start_new_thread(new_connection,(connection,))
except:
	sock.close()		

