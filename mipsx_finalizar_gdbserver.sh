#!/bin/bash

IP_MIPS=$1

# exec > /tmp/archivotemp.txt
# exec 2>&1

# Matamos el gdbserver remoto
sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "kill -9 `ps auxw | grep ${2} | grep gdbserver | grep -v grep | awk '{print $2}'` "

sleep 2
# $3, $4, $5 y $6 son los archivos temporales a borrar
sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_MIPS} "rm $3 $4 $5 $6"

