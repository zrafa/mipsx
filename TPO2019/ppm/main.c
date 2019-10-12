#include "ppmp3.h"

#include <stdio.h>
#include <stdlib.h>

extern int func_num;
extern void image_algonegra(unsigned char *pixel);

int main(int carg, char **varg)
{
    FILE *entrada, *salida;
    struct Image img;
    struct Image nimg;

    entrada = (carg > 1) ? fopen(varg[1], "r") : stdin;
    if (entrada == NULL) {
        fprintf(stderr, "No se pudo abrir el archivo de entrada T_T\n");
        return -1;
    }

    salida = (carg > 2) ? fopen(varg[2], "w") : stdout;
    if (salida == NULL) {
        fprintf(stderr, "No se pudo abrir el archivo de salida T_T\n");
        if (entrada != stdin)
            fclose(entrada);
        return -1;
    }

    if (image_read(entrada, &img)) {
        fprintf(stderr, "Error en la entrada\n");
    }

    switch (func_num) {
    case 1:
        image_fun_1(nimg.pixel);
        break;
    case 2:
        image_fun_2(nimg.pixel);
        break;
    case 1:
        image_fun_3(nimg.pixel);
        break;
    default:
        image_negative(&img, &nimg);
    }

    image_write(salida, &nimg);

    if (entrada != stdin)
        fclose(entrada);
    if (salida != stdout)
        fclose(salida);

    return 0;
}
