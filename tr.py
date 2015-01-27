#!/usr/bin/env python
# _*_ encoding: utf-8 _*_

import sys, os
import re

lineNum = 0
pos = 0
startLine = 0;
startPos = 0;
prev = ''
flag = 0
str = ''

for line in open(sys.argv[1]).readlines():
	lineNum += 1
	pos = 0
	for c in line:
		if c == '\"' and prev != '\\':
			if flag == 0:
				flag += 1
				startLine = lineNum
				startPos = pos
			elif flag == 1:
				str += c
				if re.search('[+s]*#', line) == None:
					print "%d:%d - %d:%d %s" % (startLine, startPos, lineNum, pos, str)
				str = ''
				flag = 0
		if flag == 1:
			str += c;
		prev = c
		pos += 1

