#!/usr/bin/python
#GoogEmail v1.0 strictly uses google to retrieve email
#addresses. Flow: rand_ip > hostname > google

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com


import socket, random, time, sys, urllib2, re, sets

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com GoogEmail v1.0"
	print "\t---------------------------------------------"

def usage():
	title()
	print "\n\tUsage: python googemail.py <how many addresses> <file to save>"
	print "\tExample: ./googemail.py 10000 emails.txt\n"

def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

def StripTags(text):
    finished = 0
    while not finished:
        finished = 1
        start = text.find("<")
        if start >= 0:
            stop = text[start:].find(">")
            if stop >= 0:
                text = text[:start] + text[start+stop+1:]
                finished = 0
    return text

def getgoog(domain):
	counter = 0

	try:
		while counter < 50:
			results = 'http://groups.google.com/groups?q='+str(domain)+'&hl=en&lr=&ie=UTF-8&start='+repr(counter)+ '&sa=N'
			request = urllib2.Request(results)
			request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
			opener = urllib2.build_opener()  
			text = opener.open(request).read()
			emails = (re.findall('([\w\.\-]+@'+domain+')',StripTags(text)))
			for email in emails:
				addrs.append(email)
			counter += 10
		page_counter = 0
		while page_counter < 50 :
			results_web = 'http://www.google.com/search?q=%40'+str(domain)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter) + '&sa=N'
			request_web = urllib2.Request(results_web)
			request_web.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
			opener_web = urllib2.build_opener()  
			text = opener_web.open(request_web).read()
			emails_web = (re.findall('([\w\.\-]+@'+domain+')',StripTags(text)))
			for email_web in emails_web:
				addrs.append(email_web)
			page_counter += 10
	except(IndexError, urllib2.HTTPError):
		pass

def randip():
	
	A = random.randrange(255) + 1
	B = random.randrange(255) + 1
	C = random.randrange(255) + 1
	D = random.randrange(255) + 1
	randip = "%d.%d.%d.%d" % (A,B,C,D)
	return randip

def gethost(): 
	try:
		hostname = socket.gethostbyaddr(randip())[0]
		return hostname
	except(socket.herror):
		pass

if len(sys.argv) != 3:
	usage()
	sys.exit(1)

title()
print "\n[+] Length:",sys.argv[1]
print "[+] File:",sys.argv[2]
print "[+] Starting Scan -",timer(),"\n"
addrs = []
file = open(sys.argv[2], "a")
while int(len(addrs)) < int(sys.argv[1]):
	domain = gethost()
	if domain:
		domain = domain.split(".",domain.count(".")-1)[-1]
		print "[+] Found:",domain
		getgoog(domain)
		addrs = list(sets.Set(addrs))
		print "[+] Total:",len(addrs)
print "\n[!] Found:",len(addrs),"addresses\n"
print "[+] Writing Data:",sys.argv[2],"\n"
time.sleep(3)
for addr in addrs:
	print "[",addr.replace("...",""),"]"
	file.writelines(addr.replace("...","")+"\n")
file.close()
print "\n[+] Done",timer(),"\n"
