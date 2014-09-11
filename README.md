mipsx
=====

Una aplicacion grafica para programar en lenguaje ensamblador (entorno
de desarrollo) de una arquitectura remota, y hacer debug de los programas.

Originalmente pensada para programar en lenguaje ensamblador de MIPS
y realizar verificacion de los programas en maquinas reales 
MIPS y MIPSEL.

Hemos testeado en qemu-mips, qemu-mipsel, Ben Nanonote (mipsel)
tplink mr3020 (mips), board SIE (mipsel)

Cada vez que el alumno realiza un click en "compilar y cargar" el
archivo fuente es ensamblado y vinculado en la maquina MIPS remota.
Luego, se inicia automaticamente gdbserver en el sistema mips,
con el programa binario generado. La interfaz grafica mipsx
utiliza entonces gdb-multiarch para controlar el gdbserver remoto,
y mostrar en los distintos paneles de informacion, el estado
de la maquina mips remota y la ejecución paso a paso del programa.

La información que el usuario (alumno) puede analizar mientras
ejecuta su programa es :

- Listado del programa con lineas numeradas.
- Archivo binario decodificado (disassemble), util para verificar como se implementan las pseudoinstrucciones en instrucciones reales.
- Los registros de la CPU MIPS y su contenido.
- La memoria, que incluye, el segmento de datos, de texto y la pila.
- Mensajes de depuracion de gdb, indicando el estado de ejecucion del programa en curso.
- Panel de edicio del archivo fuente.

Requisitos
----------

Se necesita tener instalado :

sshpass
python-tk
gdb-multiarch

Se necesita que en la maquina destino el usuario root tenga como clave root (configurable).

Memory layout
http://www.dirac.org/linux/gdb/02a-Memory_Layout_And_The_Stack.php


Screenshot
----------

![alt tag](https://raw.github.com/zrafa/mipsx/master/mipsx.jpg)


Extras
------

Hay una seria de programas reales ejemplos, en lenguaje ensamblador mips.
En particular, un hello.s (hello world). Un programa ejemplo para utilizar una llamada al sistema, y mostrar un caracter por la salida estandar.
El directorio ``` uart-mips ``` con un programa verificado que mapea la direccion del registro base UART de la board SIE a una palabra etiquetada del segmento de datos de un programa en lenguaje ensamblador mips. Luego, el programa ensamblador utiliza dicha direccion para acceder a los registros UART y enviar/leer caracteres asciis.


