mipsx
=====

mipsx es una interfaz grafica para desarrollar programas en lenguaje ensamblador MIPS. Trabaja en conjunto con sistemas MIPS emulados y reales.

mipsx permite ensamblar y vincular los programas desarrollados. Tambien ejecutar, y al mismo tiempo analizar, los programas compilados a través del debugger gdb. A partir de estas características, es posible realizar todo el proceso de desarrollo y verificación de programas en lenguaje ensamblador con una única herramienta, mientras que los programas pueden ser ejecutados y analizados en diferentes sistemas MIPS.

```
 * Copyright (C) 2014 Rafael Ignacio Zurita <rafa@fi.uncoma.edu.ar>
 *
 *   mipsx and examples are free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version. Check COPYING file.
```

Originalmente pensada para programar en lenguaje ensamblador de MIPS
aunque la aplicación puede ser utilizada para programar en lenguaje ensamblador (entorno de desarrollo) de otras arquitecturas remotas.

mipsx fue verificado contra equipos remotos de arquitectura MIPS, reales y emulados. En particular, se ha verificado su uso contra qemu-mips y qemu-mipsel (ambos con sistema DEBIAN GNU/Linux), computadora Ben Nanonote (hw mipsel)
tplink mr3020 (hw mips big endian hw), y board SIE (hw mipsel little endian).

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
- La memoria, que incluye, los diferentes segmentos de datos, de texto y la pila.
- Mensajes de depuracion de GNU as, ld y gdb, indicando el estado de la ejecucion del programa en curso.
- Panel de edición del archivo fuente.

De esta manera, la aplicación permita la programación en lenguaje ensamblador
en un editor grafico. Además, la aplicación utiliza el ensamblador GNU as, el vinculador
GNU ld y el programa de debug gdb. Todos estos programas son el estandar
en la industria, por lo que el alumno puede observar y verificar
la ejecucion de sus programas en CPUs MIPS, utilizando la informacion
provista por programas de desarrollo estandar.

Requisitos
----------

Se necesita tener instalado :
sshpass
python-tk
gdb-multiarch

Se necesita que en la maquina destino el usuario root tenga como clave root (configurable).


Uso
---

Ejecutar con un interprete de python ```mipsx_tk_gui.py``` 

Screenshot
----------

![alt tag](https://raw.github.com/zrafa/mipsx/master/mipsx.jpg)


Extras
------

Hay una seria de programas ejemplos, en lenguaje ensamblador mips:

- Un hello.s (hello world). 
- Dos programas ejemplo para utilizar llamadas al sistema Linux, y mostrar caracteres en salida estandar.
- Entrada y Salida programada : El directorio ``` uart-mips ``` contiene un programa verificado que mapea la direccion del registro base UART de la board SIE a una palabra etiquetada del segmento de datos de un programa en lenguaje ensamblador mips. Luego, el programa ensamblador utiliza dicha direccion para acceder a los registros UART y enviar/leer caracteres asciis.


