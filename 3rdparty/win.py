#!/usr/bin/python
#Uses nmap to scan for open netbios ports then attempts to mount.
#Usage: ./win.py <ip range>
#d3hydr8[at]gmail[dot]com

import commands, string, StringIO, getopt, sys, re, os

tmp, args = getopt.getopt(sys.argv[1:], '')

def getips():
    ip_range = args[0]
    ip_list = []
    
    nmapoutput = StringIO.StringIO(commands.getstatusoutput('nmap -P0 -p 137,138,139,445 '+ip_range)[1]).readlines()
    
    for tmp in nmapoutput:
	ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", tmp)
	if ipaddr:
	    ip_list.append(ipaddr[0])

    return ip_list

def getnames(ips):
    comp_names = []
    
    for ip in ips:
	nmblookupoutput = StringIO.StringIO(commands.getstatusoutput('nmblookup -A ' + ip)[1]).readlines()
	
	for tmp in nmblookupoutput:
	    if re.search('<00> -         ', tmp):
		point = string.find(tmp, '<00>')
		comp_names.append(tmp[1:point])
    
    return comp_names

def getshares(compname):
    
    sharelist = []
    smbclientoutput = StringIO.StringIO(commands.getstatusoutput('smbclient -n "noone" -N -L "' + compname + '"')[1]).readlines()
    
    for tmp in smbclientoutput:
	if string.find(tmp, 'PRINTER$') == -1:
	    if re.search('Disk', tmp):
		point = string.find(tmp, 'Disk')
		sharelist.append(tmp[1:point])
	    if re.search('Server               Comment', tmp):
		continue
	
    return sharelist

def mountshares(comp_name):
    comp_name = string.lower(comp_name)
    comp_name = string.strip(comp_name)
    sharecount = 0
    
    command = 'mkdir "./' + comp_name + '"'
    os.system(command)
    
    shares = getshares(comp_name)
    
    for ashare in shares:
	
	ashare = string.lower(ashare)
	ashare = string.strip(ashare)
	
	os.system('mkdir "./' + comp_name + '/' + ashare + '"')
	command = 'smbmount "//' + comp_name + '/' + ashare + '" "./' + comp_name + '/' + ashare + '" -o guest, netbiosname=bob, username=bob, uid=bob, gid=bob'
	output = commands.getstatusoutput(command)[1]
	if output:
	    print 'Error: could not mount //' + comp_name + '/' + ashare
	    os.system('rmdir  "./' + comp_name + '/' + ashare + '"')
	else:
	    print 'Mounting //' + comp_name + '/' + ashare
	    sharecount = sharecount + 1

    return sharecount
#--------------------------------------------------------------

if args == []:
    print 'Usage: win.py <ip range>'
else:    

    computer_names = getnames(getips())
    mountedcount = 0

    for name in computer_names:
    	mountedcount = mountedcount + mountshares(name)
    
    print "Mounted " + str(mountedcount) + " shares."
