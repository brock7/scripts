#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import urllib2
import cookielib
import re
from lxml import etree
# import ping
import time

def ping(ip):
	t1 = time.time()
	try:
		r = urllib2.urlopen('http://' + ip)
		if r == None:
			return -1
	except:
	 	return -1
	return time.time() - t1

ipdb = 'https://github.com/justjavac/Google-IPs'

urllib2.socket.setdefaulttimeout(3.5)
cookieJar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
urllib2.install_opener(opener) 
response = urllib2.urlopen(ipdb)
html = response.read()
tree = etree.HTML(html)          
nodes = tree.xpath(r"//a/@href") 


print 'links:' + str(len(nodes))

ips = []
#n = 0
for node in nodes:
	m = re.search('http://([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', node)
	if m != None:
		#n += 1
		#if n >= 5:
		#	break

		ip = m.group(1)
		t = ping(ip)
		print ip, t

		ips.append((ip, t))
		
		#ping.verbose_ping(m.group(1))
ips.sort(lambda x, y: cmp(x[1], y[1]))
print len(ips)
print ips
