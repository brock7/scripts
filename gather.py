import sys, os
import urllib2
import cookielib
from lxml import etree
import sys,socket
import json

opener = None

def getTitle(domain):
	try:
		if domain[:7] != 'http://':
			domain = 'http://' + domain
		response = urllib2.urlopen(domain)
		tree = etree.HTML(response.read())
		nodes = tree.xpath("/html/head/title")
		if len(nodes) >= 1:
			return nodes[0].text
		else:
			return 'No Title'
	except Exception, e:
		if hasattr(e, 'msg'):
			return 'Error: ' + e.msg
		return 'Error: ' + repr(e)

def querySubdomain(domain):
	# TODO: process page
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

def queryWhois(domain):
	# fetch cookie
	urllib2.urlopen('http://whois.www.net.cn/whois/domain/cankaoxiaoxi.com')
	response = urllib2.urlopen('http://whois.www.net.cn/whois/api_whois?host=cankaoxiaoxi.com')
	jbase = json.loads(response.read())
	for (k, v) in jbase['module'].items():
		print k, v
	response = urllib2.urlopen('http://whois.www.net.cn/whois/api_whois_full?host=cankaoxiaoxi.com')
	jdetail = json.loads(response.read())
	for (k, v) in jdetail['module'].items():
		print k + ':', v

def nmap(domain):
	pass # TODO: 

if __name__ == '__main__':
	cookieJar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
	urllib2.install_opener(opener)
	print '============================== subdomain =============================='
	querySubdomain(sys.argv[1])
	print '============================== reverse dns =============================='
	queryRDNS(sys.argv[1])
	print '============================== whois =============================='
	queryWhois(sys.argv[1])
	print '============================== nmap =============================='
	nmap(sys.argv[1])

	#urllib2.urlopen('http://whois.www.net.cn/whois/domain/cankaoxiaoxi.com')
	#response = urllib2.urlopen('http://whois.www.net.cn/whois/api_whois?host=cankaoxiaoxi.com')
	#print response.read()
	#response = urllib2.urlopen('http://whois.www.net.cn/whois/api_whois_full?host=cankaoxiaoxi.com')
	#print response.read()
	sys.exit(0)
################################################################

#from formatter import AbstractFormatter, NullWriter
#from htmllib import HTMLParser
# 
#def _(str, in_encoder="gbk", out_encoder="utf8"):
#    #return unicode(str, in_encoder).encode(out_encoder)
#    return str
#
#
#class myWriter(NullWriter):
#    def __init__(self):
#        NullWriter.__init__(self)
#        self._bodyText = []
#
#    def send_flowing_data(self, str):
#        self._bodyText.append(str)
#
#    def _get_bodyText(self):
#        return '/n'.join(self._bodyText)
#
#    bodyText = property(_get_bodyText, None, None, 'plain text from body')
#
#class myHTMLParser(HTMLParser):
#    def do_meta(self, attrs):
#        self.metas = attrs
#
#def convertFile(filename):
#    mywriter = myWriter()
#    absformatter = AbstractFormatter(mywriter)
#    parser = myHTMLParser(absformatter)
#    parser.feed(open(filename).read())
#    return ( _(parser.title), parser.formatter.writer.bodyText )
#
#import os
#import os.path
#
#OUTPUTDIR = "./txt"
#INPUTDIR = "."
#if __name__ == "__main__":
#    if not os.path.exists(OUTPUTDIR):
#        os.mkdir(OUTPUTDIR)
#
#    for file in os.listdir(INPUTDIR):
#        if file[-4:] == '.htm':
#            print "Coverting", file,
#            outfilename, text = convertFile(file)
#            outfilename = outfilename + '.txt'
#            outfullname = os.path.join(OUTPUTDIR, outfilename)
#            open(outfullname, "wt").write(text)
#            print "Done!"
#
################################################################################
"""

#!/usr/bin/env python
# encoding:utf8
# author:zhouhh
# date:2012.11.20
from bs4 import BeautifulSoup
import os
import codecs
f="shedia.txt"
t=codecs.open(f,"wb",encoding="gb18030")
#t.write("\nzhh made for my dear yff \n2012.11.18\n")
ts=[]
 
t.write("\nzhh made for my dear yff \n2012.11.18\n\n")
for i in sorted(os.listdir(".")):
    if(i[-3:]=="htm"):
        print "convert %s title "%i
        htm=codecs.open(i,"rb",encoding="gb18030")
    soup=BeautifulSoup(htm)
        htm.close()
    #f="%stxt"%i[:-3]
    #print "write to %s"%f
        #t.write(soup.select("p")[0].text)
    title=soup.title.text[7:]
    ts.append(title)
t.write("\n".join(ts))
 
for i in sorted(os.listdir(".")):
    if(i[-3:]=="htm"):
        print "convert %s"%i
        htm=codecs.open(i,"rb",encoding="gb18030")
    soup=BeautifulSoup(htm)
        htm.close()
    #f="%stxt"%i[:-3]
    #print "write to %s"%f
        #t.write(soup.select("p")[0].text)
    t.write("\nzhh made for my dear yff \n2012.11.18\n\n")
    title=soup.title.text[7:]
 
        t.write(title)
    t.write(soup.select("pre")[0].text)
    #t.write(soup.body.text)
t.close()
"""

