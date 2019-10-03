#!/bin/bash

RUTA=/usr/bin/
# AS=mips-linux-gnu-as
# LD=mips-linux-gnu-ld
AS=as
LD=ld
CC=gcc
OBJDUMP=mips-linux-gnu-objdump
IP_MIPS=10.0.15.50

PATH=/usr/local/jlime-2010.1/mipsel/bin/:$PATH


exec > /tmp/archivotemp${2}.txt
exec 2>&1


# Copiamos el archivo fuente
# cp ${1} /tmp &&

ARCHIVO=`basename ${1}` 

# Ensamblamos y vinculamos
cd /tmp &&
mipsel-linux-gnu-as  -g --gstabs -o ${ARCHIVO}.o ${ARCHIVO}  &&
mipsel-linux-gnu-gcc  -o ${ARCHIVO}.elf ${ARCHIVO}.o /export/home/extras/mipsx/uartmips_init.o  && echo "Compilacion OK. Ejecutar en SIE el programa ${ARCHIVO}.elf

"


