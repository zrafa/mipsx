uart-mips
---------

Este programa mapea la direccion del registro base UART de la board SIE a una palabra etiquetada del segmento de datos de un programa en lenguaje ensamblador mips. 

El programa ensamblador utiliza dicha direccion para acceder a los registros UART y enviar/leer caracteres ascii.

El programa se compila con make, y ha sido testeado contra una terminal DEC vt320 y minicom.

El ejemplo puede ser utilizado como base para las prácticas de laboratorio del tema Entrada/Salida.



