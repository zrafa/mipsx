#!/bin/bash

RUTA=/usr/bin/
AS=mips-linux-gnu-as
LD=mips-linux-gnu-ld
OBJDUMP=mips-linux-gnu-objdump
# IP_MIPS=10.0.15.50
IP_MIPS=192.168.0.71

exec > /tmp/archivotemp.txt
exec 2>&1

cp "${1}" /tmp

ARCHIVO=`basename ${1}` 

${RUTA}/${AS} -g --gstabs /tmp/${ARCHIVO} -o /tmp/${ARCHIVO}.o  &&

${RUTA}/${LD} -static -o /tmp/${ARCHIVO}.elf /tmp/${ARCHIVO}.o &&

#echo "---------------------------------------------"
#echo " ** DIRECCIONES EN MEMORIA ** "
#${RUTA}/${OBJDUMP} -s ${1}.elf | grep -A 1 section
#echo "---------------------------------------------"

sshpass -p "root" scp /tmp/${ARCHIVO}.elf root@${IP_MIPS}:/tmp &&

# (sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "killall gdbserver" 2>&1 & ) >> /tmp/archivotemp.txt &&
#(EJECUTABLE=`basename ${1}.elf` ; echo $EJECUTABLE ; sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "gdbserver 0.0.0.0:4567 /tmp/$EJECUTABLE" & )
(sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "gdbserver --multi 0.0.0.0:4567 " & )

