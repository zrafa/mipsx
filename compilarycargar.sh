#!/bin/bash

RUTA=/usr/bin/
AS=mips-linux-gnu-as
LD=mips-linux-gnu-ld
IP_MIPS=10.0.15.232

( ${RUTA}/${AS} -g --gstabs $1 -o ${1}.o 2>&1 ) > /tmp/archivotemp.txt  &&

( ${RUTA}/${LD} -static -o ${1}.elf ${1}.o 2>&1 ) > /tmp/archivotemp.txt  &&

( sshpass -p "root" scp ${1}.elf root@${IP_MIPS}:/tmp 2>&1 ) >> /tmp/archivotemp.txt &&

# (sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "killall gdbserver" 2>&1 & ) >> /tmp/archivotemp.txt &&
(EJECUTABLE=`basename ${1}.elf`;  echo $EJECUTABLE; sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "gdbserver 0.0.0.0:4567 /tmp/$EJECUTABLE" 2>&1 & ) >> /tmp/archivotemp.txt

