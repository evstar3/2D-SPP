#include "box.h"

BoxList *BoxList_read(FILE *fp)
{
    fseek(fp, 0, SEEK_SET);

    BoxList *bl = malloc(sizeof(BoxList));
    if (bl == NULL)
        return NULL;

    fscanf(fp, "%lu", &bl->n_boxes);

    char c = '\0';
    for (c = fgetc(fp); c != EOF && c != '\n'; c = fgetc(fp)); // skip strip dimension line
    if (c == EOF)
        goto bad_boxfile;

    bl->boxlist = malloc(bl->n_boxes * sizeof(Box));
    if (bl->boxlist == NULL)
    {
        free(bl);
        return NULL;
    }

    for (size_t i = 0; i < bl->n_boxes; i++)
    {
        if (fscanf(fp, "%*u %u %u", &bl->boxlist[i].w, &bl->boxlist[i].h) != 2)
            goto bad_boxfile;

        for (char c = fgetc(fp); c != EOF && c != '\n'; c = fgetc(fp));
        if (c == EOF)
            goto bad_boxfile;
    }

    return bl;

bad_boxfile:

    free(bl->boxlist);
    free(bl);

    return NULL;
}

void BoxList_delete(BoxList *bl)
{
    free(bl->boxlist);
    free(bl);
}

size_t BoxList_total_height(BoxList *bl)
{
    size_t total = 0;
    for (size_t i = 0; i < bl->n_boxes; i++)
        total += bl->boxlist[i].h;
    return total;
}