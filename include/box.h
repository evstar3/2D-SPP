#ifndef BOX_H
#define BOX_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

typedef struct Box {
    uint w;
    uint h;
} Box;

typedef struct BoxList {
    size_t n_boxes;
    Box *boxlist;
} BoxList;

BoxList *   BoxList_read(FILE *fp);
void        BoxList_delete(BoxList *bl);
size_t      BoxList_total_height(BoxList *bl);

#endif