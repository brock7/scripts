#!/usr/bin/python
#This script helps you scan a list of sites with nikto.
#It will create a file in your output dir for each site in
#your list with the site name. Put this script in the same 
#dir as nikto.pl and change your OUTPUT_PATH below.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com


#Change this first!!!
#------------------------------------------
OUTPUT_PATH = "/home/d3hydr8/tools/nikto/output"
#------------------------------------------

import commands, sys, getopt, StringIO, re, string, os
				   
def niktoscan(site):
	
	#Change your nikto options here.
	command = "perl nikto.pl -host "+site+" -Cgidirs all"

	nikout = StringIO.StringIO(commands.getstatusoutput(command)[1]).readlines()
	print "[+] Writing Lines:",len(nikout)
	path = os.path.join(OUTPUT_PATH, site+".txt")
	output = open(path, "a")
	for line in nikout:
		output.writelines(line+"\n")
	output.close()

#................................................
print "\nd3hydr8[at]gmail[dot]com NikListScan v1.0"
print "------------------------------------------"
	
if len(sys.argv) != 2:
	print "\nUsage: ./niklistscan.py <site_list>\n"
	sys.exit(1)

print "\n[+] Creating output folder",OUTPUT_PATH
try:
	os.mkdir(OUTPUT_PATH)
except(OSError):
	print "[-] Failure creating dir, might already exist."
	pass
sites = open(sys.argv[1], "r").readlines()
print "[+] Sites Loaded:",len(sites),"\n"
for site in sites:
	site = site.replace("\n","")
	print "-"*35
	print "\n[+] Scanning:",site
	niktoscan(site.replace("http://",""))
print "\n[+] Done\n"

				
		
