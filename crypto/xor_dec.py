import sys

key_len = int(sys.argv[2])
def xor_str(str1, str2, length):
	#print str1, str2, length
	output = ''
	for i in range(length):
		output += chr(ord(str1[i]) ^ ord(str2[i]))
	return output

with open(sys.argv[1]) as f:
	buf = f.read()

output = ''
for i in range(0, len(buf), key_len):
	#print i
	str1 = buf[i: i + key_len]
	str2 = buf[i + key_len: i + key_len * 2]
	output += xor_str(str1, str2, min(len(str1), len(str2)))
print output

