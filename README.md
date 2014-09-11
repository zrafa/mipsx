mipsx
=====

Una aplicacion grafica para programar en lenguaje ensamblador (entorno
de desarrollo) de una arquitectura remota, y hacer debug de los programas.

Originalmente pensada para programar en lenguaje ensamblador de MIPS
y realizar verificacion de los programas en maquinas reales 
MIPS y MIPSEL.

Hemos testeado en qemu-mips, qemu-mipsel, Ben Nanonote (mipsel)
tplink mr3020 (mips), board SIE (mipsel)


Requisitos
----------

Se necesita tener instalado :

sshpass
python-tk
gdb-multiarch

Se necesita que en la maquina destino el usuario root tenga como clave root

Memory layout
http://www.dirac.org/linux/gdb/02a-Memory_Layout_And_The_Stack.php


Screenshot
----------

![alt tag](https://raw.github.com/zrafa/mipsx/master/mipsx.jpg)
