#!/usr/bin/env python3

from strip import Strip, Problem
import sys
import random

def BL(strip: Strip):
    while (strip.unplaced()):
        box_id = random.choice(strip.unplaced())
        x = 0
        y = 0

        while (not strip.is_valid_placement(box_id, x, y)):
            x += 1
            if (x == strip.problem.width):
                x = 0
                y += 1

        strip.place(box_id, x, y)

def RF(strip: Strip):
    # stack all boxes wider than W/2 in bottom left
    wide_boxes = (box_id for box_id in strip.placements
                  if strip.problem.boxes[box_id].width > strip.problem.width / 2)

    for box_id in wide_boxes:
        y = 0
        while (not strip.is_valid_placement(box_id, 0, y)):
            y += 1
        strip.place(box_id, 0, y)

    shelves = {}
    shelves[0] = strip.max_height()

    # sort remaining boxes by decreasing height
    narrow_boxes = sorted(strip.placements, key=lambda x: strip.problem.boxes[x].height, reverse=True)
    h_max = max(strip.problem.boxes[id].height for id in narrow_boxes)
    
    # place first shelf
    x = 0
    while (strip.is_valid_placement(narrow_boxes[0], x, shelves[0])):
        id = narrow_boxes.pop(0)
        strip.place(id, x, shelves[0])
        x += strip.problem.boxes[id].width

    h1 = max(strip.problem.boxes[id].height for id in strip.unplaced())

    shelves[2] = shelves[0] + h_max + h1

    x2 = strip.problem.width
    while strip.unplaced() and x2 >= strip.problem.width / 2:
        box = strip.problem.boxes[narrow_boxes[0]]
        if (strip.is_valid_placement(narrow_boxes[0], x, shelves[0])):
            strip.place(narrow_boxes[0], x, shelves[0])
            x += box.width
        elif (strip.is_valid_placement(narrow_boxes[0], x2 - box.width, shelves[2] - box.height)):
            strip.place(narrow_boxes[0], x2 - box.width, shelves[2] - box.height)
            x2 -= box.width
        narrow_boxes.pop(0)

with open(sys.argv[1]) as fp:
    strip = Strip(Problem(fp))

RF(strip)

strip.print_strip()

print(strip.max_height())




