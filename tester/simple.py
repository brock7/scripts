import urllib2
import re
import types
import codecs
from utils import webutils

results = [
	"<b>Fatal error</b>:", 
	"^Access Denied$",
	"Microsoft OLE DB Provider", 
	"You have an error in your SQL syntax", 
	r'ERROR [0-9]+?:', 
	"Forbidden", 
];

def scan(url, scanner):
	#print 'SimpleTester.scan:', url
	#pdb.set_trace()
	req = urllib2.Request(url)
	response = scanner.sendReq(req)
	if response == None:
		return False
	#print response
	try:
		if type(response) == types.StringType:
			respText = response
		else:
			if response.geturl() != url and response.geturl() != url + '/':
				# print "REDIRECTED: ", response.geturl(), url
				return False
			respText = response.read()
		respText = webutils.decodeHtml(respText)
		#print respText
		if respText[:3] == codecs.BOM_UTF8:
			respText = respText[3:]

		if scanner.isCheckAll():
			#pdb.set_trace()
			if not scanner.isNotFoundPage(respText):
				scanner.report(url, respText[:512])
				return True
			else:
				#pdb.set_trace()
				return False

		for p in results:
			if re.search(p , respText, re.IGNORECASE):
				scanner.report(url, respText[:512])
				return True
	except:
		#raise
		pass
	return False

