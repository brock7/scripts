import sys
lines = open(sys.argv[1]).readlines()
for line in lines:
	line = line.rstrip('\n')
	if line.find('E+') != -1:
		print "%.f" % float(line)
	else:
		print line
