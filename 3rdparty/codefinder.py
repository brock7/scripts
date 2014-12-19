#!/usr/bin/python
#Searches files for string match. You can also 
#choose to only search a certain extension (php, html, py)

#http://darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, re

def Walk( root, recurse=0, pattern='*', return_folders=0 ):
	import fnmatch, os, string

	result = []

	try:
		names = os.listdir(root)
	except os.error:
		return result

	pattern = pattern or '*'
	pat_list = string.splitfields( pattern , ';' )

	for name in names:
		fullname = os.path.normpath(os.path.join(root, name))

		for pat in pat_list:
			if fnmatch.fnmatch(name, pat):
				if os.path.isfile(fullname) or (return_folders and os.path.isdir(fullname)):
					result.append(fullname)
				continue
		if recurse:
			if os.path.isdir(fullname) and not os.path.islink(fullname):
				result = result + Walk( fullname, recurse, pattern, return_folders )
			
	return result
			
def search(files):
	print "\n[+] Searching:",len(files),"files"
	for file in files:
		num = 0
		try:
			text = open(file, "r").readlines()
			for line in text:
				num +=1
				if re.search(sys.argv[2].lower(), line.lower()):
					print "\n[!] File:",file,"\tLine:",num
					print "[!]",line
		except(IOError):
 			pass
	print "\n[-] Done\n"
				
print "\n d3hydr8[at]gmail[dot]com CodeFinder v1.1"
print "--------------------------------------------"

if len(sys.argv) not in [3,5]:
	print "\nUsage: ./codefinder.py <dir> <code> <option>"
	print "\nExample: ./codefinder.py /home/d3hydr8 \"$root_path\" -ext php"
	print "\t\n[options]"
	print "\t   -e/-ext <extension> : Will only search files with this extension.\n"
	sys.exit(1)
	
print "\n[+] Scanning:",sys.argv[1]
print "[+] Code:",sys.argv[2]

if len(sys.argv) == 3:
	files = Walk(sys.argv[1], 1, '*', 1)
	search(files)
else:
	files = Walk(sys.argv[1], 1, '*.'+sys.argv[4]+';')
	search(files)