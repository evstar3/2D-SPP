#ifndef PROBLEM_H
#define PROBLEM_H

#include <stdbool.h>
#include <stdio.h>

#include "box.h"

typedef struct Problem {
    size_t width;
    size_t optimal_height;
    size_t max_height;

    BoxList *boxlist;
} Problem;

Problem *   Problem_create(FILE *fp);
void        Problem_delete(Problem *s);


#endif