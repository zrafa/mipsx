#include "ppmp3.h"

int image_readSample(FILE * input)
{
    int sample = 0;
    bool cont;
    int c;
    cont = true;
    /*
     * First we ignore white spaces.
     */
    while (cont) {
        c = fgetc(input);
        if (EOF == c) {
            return 0;
        } else if (c == '#') {
            while (!(feof(input) || ('\n' == fgetc(input)))) {
                /*
                 * Ignoring a comment.
                 */
            }
        } else if (!isspace(c)) {
            cont = false;
            sample = c - 0x30;
        }
    }
    cont = true;
    c = fgetc(input);
    while (!(c == EOF || isspace(c))) {
        sample = (sample * 10) + (c - 0x30);
        c = fgetc(input);
    }
    return sample;
}

int image_read(FILE * input, struct Image *nImage)
{
    int c;
    unsigned int sample;
    unsigned int deepth;
    int width, height;
    int index, nSamples;

    c = fgetc(input);
    if (EOF == c) {
        return image_READ_ERROR;
    } else if ('P' != c) {
        return image_WRONG_FORMAT;
    }
    c = fgetc(input);
    if (EOF == c) {
        return image_READ_ERROR;
    } else if ('3' != c) {
        return image_WRONG_FORMAT;
    }

    /*
     * Reading the header
     */
    if (feof(input)) {
        return image_READ_ERROR;
    }
    width = image_readSample(input);
    if (feof(input)) {
        return image_READ_ERROR;
    }
    height = image_readSample(input);
    if (feof(input)) {
        return image_READ_ERROR;
    }
    deepth = image_readSample(input) + 1;

    /*
     * Reading the samples
     */
    nImage->width = width;
    nImage->height = height;
    nSamples = width * height * 3;
    nImage->pixel = malloc(sizeof(nImage->pixel[0]) * nSamples);
    for (index = 0; index < nSamples; index++) {
        if (feof(input)) {
            return image_READ_ERROR;
        }
        sample = image_readSample(input);
        nImage->pixel[index] = (256 * sample) / deepth;
    }

    return 0;
}

int image_write(FILE * input, struct Image *image)
{
    int width, height;
    int index, nSamples;
    int sample;
    char tw = 70, sw;

    width = image->width;
    height = image->height;
    nSamples = width * height * 3;

    fprintf(input, "P3\n%d %d 255", width, height);

    for (index = 0; index < nSamples; index++) {
        sample = image->pixel[index];
        sw = (sample < 10) ? 1 : ((sample < 100) ? 2 : 3);
        if ((tw + sw + 1) < 71) {
            fprintf(input, " %d", sample);
            tw = tw + sw + 1;
        } else {
            fprintf(input, "\n%d", sample);
            tw = sw;
        }
    }
    fprintf(input, "\n");

    return 0;
}

int image_negative(struct Image *image)
{
    int index;
    int nSamples;
    nSamples = image->width * image->height * 3;
    for (index = 0; index < nSamples; index++) {
        image->pixel[index] = 255 - image->pixel[index];
    }
    return 0;
}

int image_clone(struct Image *orig, struct Image *nImage)
{
    int nSamples;
    nSamples = orig->width * orig->height * 3;
    nImage->pixel = malloc(sizeof(nImage->pixel[0]) * nSamples);
    if (nImage->pixel == NULL) {
        nImage->width = 0;
        nImage->height = 0;
        return image_BAD_SIZE;
    }
    nImage->width = orig->width;
    nImage->height = orig->height;
    memcpy(nImage->pixel, orig->pixel, nSamples);
    return 0;
}
