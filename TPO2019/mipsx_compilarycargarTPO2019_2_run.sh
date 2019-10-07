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


# Copiamos el archivo fuente
cd /tmp/${ARCHIVO}.dir/


# Ejecutamos gdbserver
sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "cd /tmp/${ARCHIVO}.dir/ ; cat orig.ppm | ./tpo > dest3.ppm" &&
sshpass -p "root" scp root@${IP_MIPS}:/tmp/${ARCHIVO}.dir/dest3.ppm /tmp/${ARCHIVO}.ppm &&
eom /tmp/${ARCHIVO}.ppm &&

sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "rm -rf /tmp/${ARCHIVO}.dir/"
rm -rf /tmp/${ARCHIVO}.dir
rm /tmp/${ARCHIVO}.elf
rm /tmp/${ARCHIVO}.ppm
