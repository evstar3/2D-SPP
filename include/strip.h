#ifndef STRIP_H
#define STRIP_H

#include "problem.h"

typedef struct Pos {
    const Box *box;
    uint x;
    uint y;
    bool isPlaced;
} Pos;

typedef struct Strip {
    Problem *problem;

    Pos *poslist;
    size_t n_placed;
    size_t n_unplaced;
} Strip;

#endif