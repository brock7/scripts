#!/bin/bash
# Mon Mar  7 17:30:24 CET 2005 <aramosf@514.es> <aramosf@unsec.net>
#
# Reverse whois con whois.webhosting.info
# DESCRIPCION GENERAL:
#  - Partiendo de un dominio o IP realiza las busquedas
#    en la web whois.webhosting.info para encontrar posibles
#    virtualhosts asociados
# ENTRADA:
# ./script.sh <ip|web>
#
# SALIDA:
# VirtualHosts asociados a la IP o IPs
#
# HISTORIAL:
#   - v1.0: Primera version
#
# NOTAS: 
#   - Requiere: ImageMagick / gocr / wget
#   - Como se abuse == nos quedamos sin chiringo
#
# TODO: 
#   - Soporte para otros clientes web ?
#   - Random del User-Agent ?




################################ URL
URL="http://whois.webhosting.info" #
####################################

############################### PATHS
WGET="/usr/bin/wget"                #
GOCR="/usr/bin/gocr"                #
CONVERT="/usr/bin/convert"          #
#####################################

################################################### OPTIONS 
WOPTS="-q -U \"Mozilla/4.0\""                             # wget options
WOPTSPROXY="off"                                          # wget on/off PROXY
export http_proxy="http://202.56.231.117:8080"            # wget proxy url
COPTS="-monochrome -contrast -level 100 -crop 48x13+36+7" # convert
###########################################################

# Lo se, demasiados temporales, pero esto es bash~!$%@!
TMP=`mktemp -d`
PNGTMP="$TMP/$$.png"
PGMTMP="$TMP/$$.pgm"
SUM=0

# Ejecucion

parsea() {
	STRING='^<td><a href=\"http://whois.webhosting.info/'
	if [ `echo -e "$HTMLTMP" | grep -c "$STRING"` -ne 0 ]; then
		MATCH=`echo -e "$HTMLTMP" | grep "$STRING" -c`
		SUM=$(( $SUM + $MATCH )) 
		echo -e "$HTMLTMP" | grep "$STRING" | sed -e 's,.*\">\(.*\)\..*,\1,'
	elif [ `echo -e "$HTMLTMP" | grep -c 'IP Details - N/A'` -eq 1 ]; then
		echo Sin dominios registrados
	else
		echo Error. 
	fi
}
borra() {
	rm -rf $TMP
}

primera() {
 OPT=$1
 HTMLTMP=`$WGET -Y $WOPTSPROXY $WOPTS $URL/$OPT -O-`
 # comprobacion si hace falta usar OCR
 if [ `echo -e "$HTMLTMP"|grep -c sec.php` -ge 1 ]; then
   PNG=`echo -e "$HTMLTMP"|tr '<' '\n'|tr '>' '\n'| awk -F"'" '/sec.php/ {print $2}'`
   ENCK=`echo -e "$HTMLTMP"|grep sec.php|awk -F"'" '{print $26}'|awk -F= '{print $2}'`
   $WGET -Y $WOPTSPROXY $WOPTS $PNG -O $PNGTMP
   $CONVERT $COPTS $PNGTMP $PGMTMP
   # FIXME: el OCR toma como 0 los 8 y como O los 0
   COD=`$GOCR -i $PGMTMP |sed -e 's,0,8,g' -e 's,O,0,g'| awk '{print $2}'`
   if [ -z $COD ]; then 
	COD=`$GOCR -i $PGMTMP|sed -e 's,0,8,g' -e 's,O,0,g'|awk '{print $1}'`
   fi
   POST="enck=$ENCK&srch_value=$IP&code=$COD&subSecurity=Submit"
   HTMLTMP=`$WGET -Y $WOPTSPROXY $WOPTS --post-data $POST $URL/$OPT -O-`
   parsea
 else 
   parsea
 fi

}

function resto {
  STRING='ob=SLD&oo=ASC'
  OPT=`echo -e "$HTMLTMP" | grep $STRING|tr '<' '\n'|tr '>' '\n'|grep href|tail -2|head -1|awk -F'"' '{print $2}'|sed -e 's,^.,,'`
  if [ `echo -e "$URLTMP"| grep -c "$OPT"` -eq 0 ]; then
    URLTMP="$URLTMP\n$OPT"
    primera $OPT
  else
	borra
  fi
}

argv=$1

# Muere si hay algun fallo en ejecucion:
if [ -z $1 ]; then echo "$0 <ip|web>"; borra; exit 1; fi

for SOFT in $WGET $GOCR $CONVERT; do
  if [ ! -x $SOFT ]; then
	borra
	echo "Not found: $SOFT"
	exit 1
  fi
done


mkdir -p $TMP

final() {
 	primera $IP
	while [ `echo -e "$HTMLTMP"|grep -c 'ob=SLD&oo=ASC'` -ge 1 ]; do resto; done
	borra
}


if [ `echo $argv | grep -Ec "[0-9].[0-9].[0-9].[0-9]"` -eq 1 ]; then
	IP=$argv
	final 
else 
	for IP in `host -t a $argv | awk '/address/ {print $4}'`; do
		echo "Virtual Hosts in $IP"
		final 
	done
fi

echo "Total: $SUM"
exit 0
