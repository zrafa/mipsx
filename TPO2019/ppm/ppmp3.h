#ifndef __ppmp3_h
#define __ppp3m_h

#ifndef _STDLIB_H
#include <stdlib.h>
#endif

#ifndef _STDIO_H
#include <stdio.h>
#endif

#ifndef CTYPE_H
#include <ctype.h>
#endif

#ifndef _STDBOOL_H
#include <stdbool.h>
#endif

#ifndef _STRING_H
#include <string.h>
#endif

struct Image {
    int height;
    int width;
    unsigned char *pixel;
};

enum image_err {
    image_OK = 0,
    image_READ_ERROR,
    image_WRONG_FORMAT,
    image_BAD_SIZE,
    image_UNKOW_ERROR = 0xFFFF
};

int image_read(FILE * input, struct Image * nImage);
int image_write(FILE * input, struct Image * image);
int image_clone(struct Image *orig, struct Image *nImage);
int image_negative(struct Image *image);

#endif
