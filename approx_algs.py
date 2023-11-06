#!/usr/bin/env python3

from strip import Strip, Problem
import sys
import random

def BL(strip: Strip):
    while (strip.unplaced):
        box_id = strip.unplaced[0]
        x = 0
        y = 0

        while (not strip.isValidPlacement(box_id, x, y)[0]):
            x += 1
            if (x == strip.problem.width):
                x = 0
                y += 1

        strip.place(box_id, x, y)

with open(sys.argv[1]) as fp:
    strip = Strip(Problem(fp))

BL(strip)

strip.print_strip()

print(strip.max_height())




