#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import re
import locale

reload(sys)
sys.setdefaultencoding(locale.getpreferredencoding())

text = ''
for line in sys.stdin:
	text += line
if len(text) <= 0:
	sys.exit(0)

nodes = re.findall(sys.argv[1], text)
for node in nodes:
	print node

