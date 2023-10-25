#include "problem.h"

Problem * Problem_create(FILE *fp)
{
    Problem *p = malloc(sizeof(Problem));
    if (p == NULL)
        return NULL;

    while (fgetc(fp) != '\n'); // skip first line

    fscanf(fp, "%lu %lu", &p->width, &p->optimal_height);

    p->boxlist = BoxList_read(fp);

    fclose(fp);

    p->max_height = BoxList_total_height(p->boxlist);

    return p;
}

void Problem_delete(Problem *p)
{
    BoxList_delete(p->boxlist);
    free(p);
}