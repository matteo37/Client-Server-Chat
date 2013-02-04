from socket import *
import sys
import shlex

# Create a TCP/IP socket
sock = socket(AF_INET,SOCK_STREAM)

# put args into variables
user_input = sys.argv
ip_address = user_input[1]
port = int(float(user_input[2]))

# Connect the socket to the port where the server is listening
server_address = (ip_address, port)
sock.connect(server_address)
data = sock.recv(2000)
print >>sys.stderr, data

try:
	message = ''
	while(message.startswith('adios') == False):
		# Send data
		message = raw_input()
		if (message != ''):
			sock.sendall(message)
			# Look for the response
			data = sock.recv(2000)
			print >>sys.stderr, data
	sock.sendall('adios')
	quit()
	#print >>sys.stderr, 'close'
except:
	sock.close()