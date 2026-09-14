#!/bin/bash

echo $1 $2 $3 
RUTA=/usr/bin/
# AS=mips-linux-gnu-as
# LD=mips-linux-gnu-ld
AS=as
LD=ld
CC=gcc
OBJDUMP=mips-linux-gnu-objdump
IP_MIPS=$3
# 10.0.2.50


exec > /tmp/archivotemp${2}.txt
exec 2>&1

# Matamos el gdbserver remoto
##  sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "killall gdbserver "
sshpass -p "alumno" ssh  -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa -o KexAlgorithms=+diffie-hellman-group1-sha1 -o StrictHostKeyChecking=no alumno@${IP_MIPS} "kill `ps auxw | grep ${2} | grep gdbserver | awk '{print $2}'` 2>&1 | grep -v kill"

# -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa -o KexAlgorithms=+diffie-hellman-group1-sha1 
# -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa -o KexAlgorithms=+diffie-hellman-group1-sha1 

# Copiamos el archivo fuente
sshpass -p "alumno" scp -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa -o KexAlgorithms=+diffie-hellman-group1-sha1 ${1} alumno@${IP_MIPS}:/tmp &&

ARCHIVO=`basename ${1}` 

# Ensamblamos y vinculamos
# sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "cd /tmp/ && ${CC} -msoft-float -static -g ${ARCHIVO} -o ${ARCHIVO}.elf " &&

# sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "cd /tmp/ && ${AS} -g --gstabs ${ARCHIVO} -o ${ARCHIVO}.o && ${LD} ${ARCHIVO}.o -o ${ARCHIVO}.elf " &&
sshpass -p "alumno" ssh -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa -o KexAlgorithms=+diffie-hellman-group1-sha1  -o StrictHostKeyChecking=no alumno@${IP_MIPS} "cd /tmp/ && ${AS} -g --gstabs ${ARCHIVO} -o ${ARCHIVO}.o && ${LD} ${ARCHIVO}.o -o ${ARCHIVO}.elf " &&

# Obtenemos INFO de la maquina remota
# sshpass -p "alumno" ssh -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa -o KexAlgorithms=+diffie-hellman-group1-sha1 -o StrictHostKeyChecking=no alumno@${IP_MIPS} "echo \"CPU: \$(grep -m1 -E 'model name|Processor|cpu model|system type|Hardware' /proc/cpuinfo | cut -d: -f2 | sed 's/^ *//'). Linux_\$(uname -r). \$( cat /proc/meminfo  |grep Mem) \"" &&

# Copiamos el binario nuevamente a la PC
sshpass -p "alumno" scp -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa -o KexAlgorithms=+diffie-hellman-group1-sha1 alumno@${IP_MIPS}:/tmp/${ARCHIVO}.elf /tmp/ &&

# Ejecutamos gdbserver
(sshpass -p "alumno" ssh  -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa -o KexAlgorithms=+diffie-hellman-group1-sha1 -o StrictHostKeyChecking=no alumno@${IP_MIPS} "gdbserver 0.0.0.0:${2} /tmp/${ARCHIVO}.elf " &  )

