#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#
# filename: xpath.py
# written by 老妖@wooyun
# date: 2014-06-06
#
###############################################################################

import sys
from lxml import etree
import types
import getopt
import locale

reload(sys)
sys.setdefaultencoding(locale.getpreferredencoding())

docType = 'HTML'

opts, args = getopt.getopt(sys.argv[1:], "x")
for op, vaule in opts:
	if op == '-x':
		docType = 'xml'

if len(args) < 1:
	print sys.argv[0] + ' <xpath>'
	sys.exit(-1)

text = ''
for line in sys.stdin:
	text += line
if len(text) <= 0:
	sys.exit(0)

if docType == 'HTML':
	tree = etree.HTML(text)
else:
	tree = etree.XML(text)

nodes = tree.xpath(args[0])
for node in nodes:
	if node == types.StringType:
		print node
	else:
		if hasattr(node, 'text'):
			print node.text
		else:
		 	print node

