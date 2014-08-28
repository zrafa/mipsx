#!/bin/bash

RUTA=/usr/bin/
# AS=mips-linux-gnu-as
# LD=mips-linux-gnu-ld
AS=as
LD=ld
CC=gcc
OBJDUMP=mips-linux-gnu-objdump
IP_MIPS=10.0.15.50

exec > /tmp/archivotemp.txt
exec 2>&1

sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "killall gdbserver "

# echo archivo origen : $1
sshpass -p "root" scp ${1} root@${IP_MIPS}:/tmp &&

ARCHIVO=`basename ${1}` 
# echo archivo nuevo : $ARCHIVO

#sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "cd /tmp/ && ${CC} -g ${ARCHIVO} -o ${ARCHIVO}.elf " &&
sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "cd /tmp/ && ${AS} -g --gstabs ${ARCHIVO} -o ${ARCHIVO}.o && ${LD} ${ARCHIVO}.o -o ${ARCHIVO}.elf " &&

sshpass -p "root" scp root@${IP_MIPS}:/tmp/${ARCHIVO}.elf /tmp/ &&

(sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "gdbserver 0.0.0.0:4567 /tmp/${ARCHIVO}.elf" &  )

