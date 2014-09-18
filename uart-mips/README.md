uart-mips
---------

Este programa mapea la direccion del registro base UART de la board SIE a una palabra etiquetada del segmento de datos de un programa en lenguaje ensamblador mips.  El programa ensamblador utiliza dicha direccion para acceder a los registros UART y enviar/leer caracteres ascii.
Para utilizar el programa compilar simplemente con ``` make ```, y ha sido testeado contra una terminal DEC vt320 y minicom.

El ejemplo puede ser utilizado como base para las prácticas de laboratorio del tema Entrada/Salida.

Screenshot
----------

![alt tag](https://raw.github.com/zrafa/mipsx/master/uart-mips/uartmips-dec-vt320.jpg)



Configurando el Serial
----------------------

La board SIE, como la ben nanonote, tienen configurado el uart serial a velocidad 57600 
Y lo mas IMPORTANTE: El pin RX del serial está configurado como GPIO porque se utiliza en el teclado de la Ben Nanonote!!

Para configurar el serial :

``` 
The RX serial data channel can be set in the CPU to GPIO mode or to alternative function (serial RX). By default, it's set to GPIO, as a keyboard line uses this (pin 26 of GPIO port D) HW wiki.
To enable the alternative function (RX), and disable the keyboard use, we have to write '1' to the proper position (so, the 32-bit value 2^26=0x04000000) of the PDFUNS register (0x10010344). I took this from the jz4725 PM, which in this aspect works like the jz4740 in the nanonote.
We can set the value using the poke command running it as:

echo Deshabilitando el pin RX de gpio
poke -32 0x10010344 0x04000000

echo Cambiando velocidad uart
stty -F /dev/ttyS0 9600
```

El programa poke se puede obtener de :
http://projects.qi-hardware.com/index.php/p/wernermisc/source/tree/355614bb346c58cb5e5359bac0a1411edb037c7e/poke
