import urllib2
import re
import urlparse
from utils import webutils
from lxml import etree
import codecs

#####################################################################
# vulnerability testers

"""
http://bbs.drvsky.com/read.php?tid[]=2679
Fatal error: Unsupported operand types in /home/wwwroot/drvsky/require/guestfunc.php on line 23
"""
def scan(url, scanner):
	urlP = urlparse.urlparse(url)
	if re.search(r'\.php$', urlP.path, re.IGNORECASE):
		if url.find('=') != -1:
			url = url.replace('=', '[]=')
			#print url

			req = urllib2.Request(url)
			response = scanner.sendReq(req)
			if response == None:
				return False
			try:
				respText = response.read()
			except:
				return False
			try:
				respText = webutils.decodeHtml(respText)
				if respText[:3] == codecs.BOM_UTF8:
					respText = respText[3:]
				# respText = respText.decode('utf8')
			except Exception, e:
				print e
				pass
			
			if scanner.isCheckAll():
				scanner.report(url, respText[:512])
				return True

			if re.search('Fatal error', respText):
				scanner.report(url, respText[:512])
				return True
	return False

