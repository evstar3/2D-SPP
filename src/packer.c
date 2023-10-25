#include "packer.h"

int main(int argc, char *argv[])
{
    if (argc > 1)
    {
        // TODO
    }
    else
    {
        BoxList *bl = BoxList_read(stdin);
        if (bl == NULL)
            return 1;

        printf("Boxes: %lu\n", bl->n_boxes);

        for (int i = 0; i < bl->n_boxes; i++)
            printf("  %d %d\n", bl->boxlist[i].w, bl->boxlist[i].h);

        printf("Total height: %lu\n", BoxList_total_height(bl));

        BoxList_delete((BoxList *)bl);
    }

    return 0;
}