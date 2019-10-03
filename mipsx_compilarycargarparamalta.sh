#!/bin/bash

RUTA=/usr/bin/

exec > /tmp/archivotemp${2}.txt
exec 2>&1


ARCHIVO=`basename ${1}` 

# Ensamblamos y vinculamos
mkdir /tmp/${ARCHIVO}.dir/ &&
cd /tmp/${ARCHIVO}.dir/
cp /export/home/extras/mipsx/barebone/* . &&
cp /tmp/$ARCHIVO start.S
make clean
make || (echo "Error de compilacion" ; exit 1)
# make run

# Copiamos el archivo fuente
sshpass -p "alumno" scp barebone.elf alumno@10.0.15.49:/tmp/${ARCHIVO}

# ARCHIVO=`basename ${1}` 

# Ensamblamos y vinculamos
sshpass -p "alumno" ssh -C -X -o StrictHostKeyChecking=no alumno@10.0.15.49 "cd /tmp/ && qemu-system-mips -M malta -m 16M -kernel $ARCHIVO -serial null -serial null -serial vc ; rm $ARCHIVO"

rm -rf /tmp/${ARCHIVO}.dir
rm /tmp/${ARCHIVO}
