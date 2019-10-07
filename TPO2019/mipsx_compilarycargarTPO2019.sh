#!/bin/bash

RUTA=/usr/bin/
AS=as
LD=ld
CC=gcc
OBJDUMP=mips-linux-gnu-objdump
IP_MIPS=10.0.15.50

ARCHIVO=`basename ${1}` 

exec > /tmp/archivotemp${2}.txt
exec 2>&1

# Matamos el gdbserver remoto
sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "kill `ps auxw | grep ${2} | grep gdbserver | awk '{print $2}'` 2>&1 | grep -v kill"

# Copiamos el archivo fuente
mkdir /tmp/${ARCHIVO}.dir/ &&
cd /tmp/${ARCHIVO}.dir/
cp /export/home/extras/mipsx/TPO2019/ppm/* . &&
cp ${1} tpo.s
sshpass -p "root" scp -r /tmp/${ARCHIVO}.dir/ root@${IP_MIPS}:/tmp && 

# ARCHIVO=`basename ${1}` 

# Ensamblamos y vinculamos
# El siguiente habría que hacerlo con make
# sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "cd  /tmp/${ARCHIVO}.dir/ && ${AS} -g --gstabs ${ARCHIVO} -o ${ARCHIVO}.o && ${LD} ${ARCHIVO}.o -o ${ARCHIVO}.elf " &&
sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "cd  /tmp/${ARCHIVO}.dir/ && make " &&


# Copiamos el binario nuevamente a la PC
sshpass -p "root" scp root@${IP_MIPS}:/tmp/${ARCHIVO}.dir/tpo /tmp/${ARCHIVO}.elf 

# Ejecutamos gdbserver
# (sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "gdbserver 0.0.0.0:${2} /tmp/${ARCHIVO}.elf " &  )
# sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "cd /tmp/${ARCHIVO}.dir/ ; cat orig.ppm | ./tpo > dest3.ppm" &&
# sshpass -p "root" scp root@${IP_MIPS}:/tmp/${ARCHIVO}.dir/dest3.ppm /tmp/${ARCHIVO}.ppm &&
# eom /tmp/${ARCHIVO}.ppm &&

# sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "rm -rf /tmp/${ARCHIVO}.dir/"
# rm -rf /tmp/${ARCHIVO}.dir
# rm /tmp/${ARCHIVO}.elf
# rm /tmp/${ARCHIVO}.ppm
