#!/usr/bin/python
from socket import *
import sys, os
from thread import *
from mimetypes import MimeTypes
import urllib 

# import magic

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
def new_connection(conn):

	connection = conn
    # Wait for a connection
	try:
		print 'connected'
		#Loop on responses
		data = connection.recv(20000)
		#handle the GET?CHAT? command
		if(data.startswith('GET /CHAT')):
			return_data = data.split('?')[1].split('&')
			name = None
			content = None
			room = None
			# Gets the variables from the query string
			for r in return_data:
				temp = r.split('=')
				if temp[0].lower() == 'name':
					name = temp[1].replace('+',' ')
				if temp[0].lower() == 'line':
					content = str(temp[1]).split(' HTTP')[0].replace('+',' ')
				if temp[0].lower() == 'room':
					room = str(temp[1]).replace('+',' ')
			chatroom = room + '.txt'
			# writes to the chat txt file
			if name != None and content != None and room != None:
				file = open(chatroom, 'a')
				file.write(str(name)+': '+str(content)+'\n')
				file.close()
			file = open(chatroom, 'r')
			#sends the response

			connection.send(str(file.read()))	
			file.close()	
		# Just get teh updated chatlog file content
		elif(data.startswith('GET /REFRESH')):
			#import pdb; pdb.set_trace();
			return_data = data.split('?')[1].split('&')
			room = None
			# Gets the variables from the query string
			for r in return_data:
				temp = r.split('=')
				if temp[0].lower() == 'room':
					room = str(temp[1]).replace('+',' ')
			chatroom = room + '.txt'
			print >>sys.stderr, chatroom
			file = open(chatroom, 'r')
			#sends the response
			connection.send(str(file.read()))	
			file.close()	
		# Simple get servers back the content of various MIME types			
		elif(data.startswith('GET')):
			filetag = data.split('\r\n')[0].split(' ')[1]
			if filetag == '/':
				filetag = '/index.html'
			if '?' in filetag:
				filetag = filetag.split('?')[0]
			print filetag
			#gets the given file
			filename = os.path.abspath('') + filetag
			f = open(filename, 'r')
			#sends the response
			# mimeType = magic.from_file(filename, mime=True)
			mime = MimeTypes()
			url = urllib.pathname2url(filename)
			mimeType = mime.guess_type(url)
			print >>sys.stderr, mimeType[0]
			body = str(f.read())
			# Clearly state that connection will be closed after this response,
			# and specify length of response body
			response_headers = {
				'Content-Type': mimeType[0] + ' encoding=utf8',
				'Content-Length': len(body),
				'Connection': 'close',
			}

			response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())

			# Reply as HTTP/1.1 server, saying "HTTP OK" (code 200).
			response_proto = 'HTTP/1.1'
			response_status = '200'
			response_status_text = 'OK' # this can be random
			connection.send('%s %s %s' % (response_proto, response_status, response_status_text))
			connection.send(response_headers_raw)
			connection.send('\n') # to separate headers from body
			connection.send(body)		
			#connection.send(str(f.read()))	
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
		#Create a new thread when a connection is initiated
		start_new_thread(new_connection,(connection,))
except:
	sock.close()

