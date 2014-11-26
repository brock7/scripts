#!/bin/sh
curl -s http://1111.ip138.com/ic.asp | iconv -f gbk | ./xpath.py "//center/text()"
if [[ -n $1 ]]; then
	curl -s "http://www.ip138.com/ips138.asp?ip=$1&action=2" | iconv -f gbk | ./xpath.py "//h1|//h1/*|//ul/li"  
fi
