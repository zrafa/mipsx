#!/bin/bash

RUTA=/usr/bin/
# AS=mips-linux-gnu-as
# LD=mips-linux-gnu-ld
AS=as
LD=ld
CC=gcc
OBJDUMP=mips-linux-gnu-objdump
IP_MIPS=10.0.15.50


exec > /tmp/archivotemp${2}.txt
exec 2>&1

# Matamos el gdbserver remoto
##  sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "killall gdbserver "
sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "kill `ps auxw | grep ${2} | grep gdbserver | awk '{print $2}'` "

# Copiamos el archivo fuente
sshpass -p "root" scp ${1} root@${IP_MIPS}:/tmp &&

ARCHIVO=`basename ${1}` 

# Ensamblamos y vinculamos
#sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "cd /tmp/ && ${CC} -g ${ARCHIVO} -o ${ARCHIVO}.elf " &&
sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "cd /tmp/ && ${AS} -g --gstabs ${ARCHIVO} -o ${ARCHIVO}.o && ${LD} ${ARCHIVO}.o -o ${ARCHIVO}.elf " &&

# Copiamos el binario nuevamente a la PC
sshpass -p "root" scp root@${IP_MIPS}:/tmp/${ARCHIVO}.elf /tmp/ &&

# Ejecutamos gdbserver
(sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "gdbserver 0.0.0.0:${2} /tmp/${ARCHIVO}.elf" &  )

