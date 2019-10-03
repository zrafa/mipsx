#!/bin/bash

# Intentamos copiar y ejecutar en la SIE


IP_SIE=192.168.1.202
TEMPORAL=/tmp/$$$$


if [ $# -lt 1 ] ; then echo "falta el argumento" ; exit 1 ; fi

# exec > $TEMPORAL
# exec 2>&1

# Copiamos el archivo fuente

echo "copiando" 
sshpass -p "alumno" scp -o StrictHostKeyChecking=no alumno@10.0.2.31:/tmp/${1} /tmp &&


echo "copiando" 
# Copiamos el binario nuevamente a la PC
sshpass -p "root" scp ${1} root@${IP_SIE}:/tmp/ &&

echo "ejecutar.." 
# Ejecutamos gdbserver
sshpass -p "root" ssh -o StrictHostKeyChecking=no root@${IP_SIE} "/tmp/${1}"

# rm $TEMPORAL
