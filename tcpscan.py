#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#
# author: Brock | 老妖(laoyaogg@qq.com)
# date: 2014-11-15
# ver: 0.5
#

import sys, os
import socket
import getopt

def detect_port(host, port):
	s = socket.socket()
	s.settimeout(1)
	try:
		s.connect((host, port))
		s.send('GET / HTTP/1.0\n\n')
		buf = s.recv(1024)
		print port, buf[:buf.find('\n')]
	except socket.timeout:
		pass
	except socket.error:
	 	pass

	s.close()

for port in open('data/nmap_tcp_port.txt'):
	port = int(port)
	detect_port(sys.argv[1], port)

