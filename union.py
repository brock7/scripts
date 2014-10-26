import sys, getopt

files = []

for arg in sys.argv[1:]:
	files.append(open(arg))

buffers = []

for f in files:
	buffers.append(f.readlines())

max = 0

for lines in buffers:
	l = len(lines)
	if l > max:
		max = l

mark = set()

for i in range(0, max):
	for lines in buffers:
		if i >= len(lines):
			continue;
		#print lines[i]
		line = lines[i]
		if not line in mark:
			mark.add(line);
			line = line.rstrip('\n')
			print(line)
