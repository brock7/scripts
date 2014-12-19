#!/usr/bin/env python
#Trys to crack md5 with alpha lowercase char set.
#Length 5 characters.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, md5, time

def crack(word):
	time.sleep(0.2) #Edit according to your system.
	print ''.join(word), md5.new(''.join(word)).hexdigest()
	value = md5.new(''.join(word)).hexdigest()
	if sys.argv[1] == value:
		print "\n[!] Cracked:",''.join(word),"\n"
		sys.exit(1)

def main(first, start, second=[]):
	if not start: return crack(second)
    	for i in range(len(first)):
        	second.append(first.pop(i))
        	main(first, start-1, second)
        	first.insert(i, second.pop())

if len(sys.argv) != 2:
	print "\nUsage: ./alphalowcrack.py <md5>\n"
	sys.exit(1)
	
print "\nWorking...\n"
main(list("abcdefghijklmnopqrstuvwxyz"), 5)