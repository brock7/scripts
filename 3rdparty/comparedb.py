#!/usr/bin/python
#This will compare 2 lists created from my md5
#database collector's and remove duplicates 
#saving to a new database.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com 

import sys, sets

if len(sys.argv) != 4:
	print "Usage: ./comparedb.py <1st list> <2nd list> <new list>"
	sys.exit(1)
	
print "\n   d3hydr8[at]gmail[dot]com compareDB v1.0"
print "----------------------------------------------"

try:
  	list1 = open(sys.argv[1], "r").readlines()
except(IOError): 
	print "[-] Error: Check your 1st database file.\n"
  	sys.exit(1)

try:
  	list2 = open(sys.argv[2], "r").readlines()
except(IOError): 
  	print "[-] Error: Check your 2nd database file.\n"
  	sys.exit(1)
  
new_list = []
print "\n[+] Loaded:",len(list1)+len(list2),"lines"
list1.extend(list2)
for line in list1:
	new_list.append(line.strip("\n"))
new_list = list(sets.Set(new_list))
print "[+] Writing Data:",len(new_list)
file = open(sys.argv[3], "a")
for line in new_list:
	file.writelines(line.strip("\n")+"\n")
file.close()
print "\n[+] Done\n"