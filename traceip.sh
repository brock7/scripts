#!/bin/bash

if [[ -n $1 ]]; then
	#curl -s "http://www.ip138.com/ips138.asp?ip=$1&action=2" | iconv -f gbk | ./xpath.py "//h1/text()|//h1/*|//ul/li"  
	curl -s "http://www.ip138.com/ips138.asp?ip=$1&action=2" | ./xpath.py "//h1/text()|//h1/*|//ul/li"  
else
	#curl -s http://1111.ip138.com/ic.asp | iconv -f gbk | ./xpath.py '//center/text()'
	curl -s http://1111.ip138.com/ic.asp | ./xpath.py '//center/text()'
fi

