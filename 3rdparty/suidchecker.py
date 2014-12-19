#!/usr/bin/python
#Uses the linux find cmd to locate all suid/sgid files
#and monitors checksums for changes on these files.
#d3hydr8[at]gmail[dot]com

import os, sys, pwd, getopt, StringIO, commands, md5, time

def sumfile(fobj):
	m= md5.new()
	while True:
		d= fobj.read(8096)
		if not d:
			break
		m.update(d)
	return m.hexdigest()

def md5sum(fname):
	if fname == '-':
		ret = sumfile(sys.stdin)
	else:
		try:
			f = open(fname, 'rb')
		except:
			return 'Failed to open file'
		ret = sumfile(f)
		f.close()
	return ret
	
def title():
	print "\n   d3hydr8[at]gmail[dot]com SuidChecker v1.0"
	print "----------------------------------------------"

def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

suids = []
suidsdic = {}

if len(sys.argv) != 2:
	title()
	print "\n[-] Need a time\n"
	sys.exit(1) 

title()
cmdsuids = StringIO.StringIO(commands.getstatusoutput('find / \( -perm -02000 -o -perm -04000 \) -ls')[1]).readlines()
for suid in cmdsuids:
	file = "/"+suid.split("/",1)[1][:-1]
	if os.path.isfile(file) == True:
		suids.append(file)

print "[+] Found:",len(suids),"suids\n"
print "[+] Monitoring...\n"

for fname in suids:
	hash =  md5sum(fname)
	suidsdic[fname] = hash

while 1:
	time.sleep(int(sys.argv[1]))
	for k,v in suidsdic.items():
		hash =  md5sum(k)
		if hash != v:
			print "\n[-] Found a change:",k
			print "[-] From:",v
			print "[-] To:",hash
			print "[-] Time:",timer(),"\n"
			suidsdic[k] = hash



