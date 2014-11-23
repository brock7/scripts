import sys
from lxml import etree
import types

if len(sys.argv) < 2:
	print sys.argv[0] + ' <xpath>'
	sys.exit(-1)

text = ''
for line in sys.stdin:
	text += line
if len(text) <= 0:
	sys.exit(0)

tree = etree.HTML(text)
nodes = tree.xpath(sys.argv[1])
for node in nodes:
	if node == types.StringType:
		print node
	else:
		print node.text
