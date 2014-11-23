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

def detect_port(host, port, connect_only = False):
	s = socket.socket()
	s.settimeout(1)
	try:
		s.connect((host, port))
		if connect_only:
			print port
			return
		s.send('GET / HTTP/1.0\n\n')
		buf = s.recv(1024)
		print port, buf[:buf.find('\n')]
	except socket.timeout:
		pass
	except socket.error:
	 	pass

	s.close()

ports = (21, 22, 23, 25, 53, 69, 80, 110, 135, 137, 139, 445, 1025, 1080
	  1194, 1433, 1521, 3306, 3389, 4899, 5900, 8000, 8080)
for port in ports:
	detect_port(sys.argv[1], port)

