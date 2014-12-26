#!/bin/bash
# username|ipaddr
# brock|10.8.1.1

find /var/log -exec sed -i -r "/$1/d" {} \;
find /var -name '*.log' -exec sed -i -r "/$1/d" {} \;

