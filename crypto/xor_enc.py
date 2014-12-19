import sys

crypto = sys.argv[2]
with open(sys.argv[1]) as f:
	buf = f.read()

output = ''
i = 0
for c in buf:
	output += chr(ord(c) ^ ord(crypto[i % len(crypto)]))
	i += 1

sys.stdout.write(output)

