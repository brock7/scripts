#!/usr/bin/env python
#Very Simple Wordlist Generator

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, time

def write(w):
	time.sleep(0.2) #Edit according to your system.
	ofile.writelines(''.join(w)+"\n")
	
def main(first, start, second=[]):
	if not start: return write(second)
    	for i in range(len(first)):
        	second.append(first.pop(i))
        	main(first, start-1, second)
        	first.insert(i, second.pop())

if len(sys.argv) != 4:
	print "\nUsage: ./rtgen.py <char_set> <length> <output file>\n"
	sys.exit(1)
print "\nCharSet:",sys.argv[1]
print "Length:",sys.argv[2]
print "Writing Output:",sys.argv[3]
print "\nWorking..."
ofile = open(sys.argv[3], "a")
main(list(sys.argv[1]), int(sys.argv[2]))
ofile.close()
print "\nDone\n"
