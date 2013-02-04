from socket import *
import sys
import shlex
# reaver 
# Create a TCP/IP socket
sock = socket(AF_INET,SOCK_STREAM)

# user_input = raw_input()
user_input = sys.argv
ip_address = user_input[1]
port = int(float(user_input[2]))

# ip_address = 'localhost'
# port = 9020

print ip_address
print port
# Connect the socket to the port where the server is listening
server_address = (ip_address, port)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)


try:
    
    while(1):
    	# Send data
		message = raw_input()
		#print >>sys.stderr, 'sending "%s"' % message
		sock.sendall(message)

		# Look for the response
		amount_received = 0
		amount_expected = len(message)
	    
		data = sock.recv(2000)
		print >>sys.stderr, data

finally:
	print >>sys.stderr, 'closing socket'
	sock.close()