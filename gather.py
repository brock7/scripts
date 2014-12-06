#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#
# filename: gather.py
# written by 老妖@wooyun
# date: 2014-06-06
#
###############################################################################

import sys, os, getopt, types
import urllib2
import cookielib
from lxml import etree
import sys,socket
import json

noTitle = False
def encoding(data):
	if len(data) <= 0:
		return data
	encodings = ['utf-8', 'gbk', 'gb2312']   #可以添加其他字符编码
	for encoding in encodings:
		try:
			return data.decode(encoding)
		except:
			pass
	return data

def getTitle(domain):
	global noTitle
	if noTitle:
		return ''

	try:
		if domain[:7] != 'http://':
			domain = 'http://' + domain
		response = urllib2.urlopen(domain, timeout = 15)
		tree = etree.HTML(encoding(response.read()))
		nodes = tree.xpath("/html/head/title/text()")
		# nodes = tree.xpath("/html/head/title") # 没有 text() 时，返回节点对象，用 nodes[0].text 访问
		if len(nodes) >= 1:
			return nodes[0]
		else:
			return 'No Title'
	except Exception, e:
		if hasattr(e, 'msg'):
			return 'Error: ' + e.msg
		return 'Error: ' + repr(e)

def querySubdomain(domain):
	# all in on page
	response = urllib2.urlopen('http://i.links.cn/subdomain/', data = 'domain=%s&b2=1&b3=1&b4=1' % domain)
	tree = etree.HTML(response.read())
	nodes = tree.xpath("//a[@rel='nofollow']/@href")
	for node in nodes:
		print node, getTitle(node)

def queryRDNS(domain):
	hostInfos = socket.gethostbyname_ex(domain) #r = (hostname, aliaslist, ipaddrlist)
	for ipaddr in hostInfos[2]:
		maxpage = 1
		page = 1
		print '[IP Address: ' + ipaddr + ']'
		try:
			while page <= maxpage:
				response = urllib2.urlopen('http://dns.aizhan.com/index.php?r=index/domains&ip=%s&page=%d' % 
						(ipaddr, page))
				jtext = response.read()
				if len(jtext) <= 0:
					break
				j = json.loads(jtext)
				if j == None:
					break
				#print j.keys()
				if j['maxpage'] != None:
					maxpage = int(j['maxpage'])
				for name in j['domains']:
					print name, getTitle(name)
				page += 1
		except Exception, e:
			print e
			#pass

def toStr(l):
	#print type(l)
	if type(l) != types.ListType:
		return l
	result = ''
	for item in l:
		if type(item) == types.ListType:
			for v in itme:
				result += '%s, ' % v
		elif type(item) == types.DictType:
			for (k, v) in item.items():
				result += '%s: %s ' % (k, v)
		else:
			result += str(item) + ', '
	return result


def queryWhois(domain):
	# fetch cookie
	if domain.count('.') > 1:
		domain = domain[domain.find('.') + 1:]
	urllib2.urlopen('http://whois.www.net.cn/whois/domain/%s' % domain)
	response = urllib2.urlopen('http://whois.www.net.cn/whois/api_whois?host=%s' % domain)
	jbase = json.loads(response.read())
	if jbase['success']:
		for (k, v) in jbase['module'].items():
			print k if k[-1:] == ':' else k + ': ', toStr(v) 

	response = urllib2.urlopen('http://whois.www.net.cn/whois/api_whois_full?host=%s' % domain)
	jdetail = json.loads(response.read())
	if jdetail['success']:
		for (k, v) in jdetail['module'].items():
			print k if k[-1:] == ':' else k + ': ', toStr(v)

def nmap(domain):
	os.system('nmap -sV %s' % domain)

def baseInfo(domain):
	req = urllib2.Request('http://' + domain)
	req.add_header('Proxy-Connection', 'Keep-Alive')
	req.add_header('Accept', '*/*')
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0')
	try:
		response = urllib2.urlopen(req, timeout = 15)
		#html = response.read()
		#for k, v in response.info().items():
		#	print k,v 
		if response.info().getheader('Server'):
			print 'Server: ' + response.info().getheader('Server')

		if response.info().getheader('X-Powered-By'):
			print 'Powered By: ' + response.info().getheader('X-Powered-By')
	except:
		pass

if __name__ == '__main__':
	import locale	
	reload(sys)
	sys.setdefaultencoding(locale.getpreferredencoding())

	cookieJar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
	urllib2.install_opener(opener)
	
	options = 0
	opts, args = getopt.getopt(sys.argv[1:], "Nrsw")
	for op, vaule in opts:
		if op == '-N':
			noTitle = True
		elif op == '-r':
			options |= 1
		elif op == '-s':
			options |= 2
		elif op == '-w':
			options |= 4

	if options == 0:
		options = 1 | 2 | 4 | 8
	
	baseInfo(args[0])

	if options & 1:
		print '\n============================== reverse dns ==============================\n'
		queryRDNS(args[0])
	if options & 2:
		print '\n============================== subdomain ==============================\n'
		querySubdomain(args[0])
	if options & 4:
		print '\n============================== whois ==============================\n'
		queryWhois(args[0])
	if options & 8:
		print '\n============================== nmap ==============================\n'
		sys.stdout.flush()
		nmap(args[0])
	sys.exit(0)

