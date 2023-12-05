#!/usr/bin/env python3

from strip import Strip, Problem
import random
import copy

def BL(problem: Problem, order=None) -> Strip:
    '''Bottom-up left-justified'''
    strip = Strip(problem, None)

    if order is not None:
        order = copy.deepcopy(order)
    else:
        order = random.sample(strip.unplaced, k = len(strip.unplaced))

    
    while (order):
        id = order.pop()
        x = 0
        y = 0

        while (not strip.is_valid_placement(id, (x, y))):
            x += 1
            if (x == strip.width):
                x = 0
                y += 1

        strip.place(id, (x, y))

    return strip

def NFDH(problem: Problem) -> Strip:
    '''Next-fit decreasing-height'''
    strip = Strip(problem, None)
    sorted_ids = sorted(strip.unplaced, key = lambda x: strip.boxes[x].height)

    x = 0
    y = 0
    shelf_height = 0
    while (sorted_ids):
        id = sorted_ids.pop()
        
        while True:
            while (not strip.is_valid_placement(id, (x, y))) and x < strip.width:
                x += 1

            if (strip.is_valid_placement(id, (x, y))):
                break
            
            y += shelf_height
            shelf_height = 0
            x = 0

        strip.place(id, (x, y))

        if (shelf_height == 0):
            shelf_height = strip.boxes[id].height
        
        x += strip.boxes[id].width

    return strip


def FFDH(problem: Problem) -> Strip:
    '''First-fit decreasing-height'''
    strip = Strip(problem, None)
    sorted_ids = sorted(strip.unplaced, key = lambda x: strip.boxes[x].height)

    shelves = {0: 0}
    while (sorted_ids):
        id = sorted_ids.pop()

        placed = False

        for y in shelves:
            x = 0
            while (not strip.is_valid_placement(id, (x, y))) and x < strip.width:
                x += 1

            if (strip.is_valid_placement(id, (x, y))):
                placed = True
                strip.place(id, (x, y))
                if (shelves[y] == 0):
                    shelves[y] = strip.boxes[id].height
            
        if (placed):
            continue
            
        new_shelf_height = y + shelves[y]
        strip.place(id, (0, new_shelf_height))
        shelves[new_shelf_height] = strip.boxes[id].height

    return strip

def SF(problem: Problem) -> Strip:
    '''Split fit'''
    strip = Strip(problem, None)
    m = 1
    while (all(box.width < (strip.width / (m + 1)) for box in strip.boxes)):
        m += 1

    wide = sorted(
        [id for id in strip.unplaced
            if strip.boxes[id].width > strip.width / (m + 1)],
        key = lambda x: strip.boxes[x].height
    )

    narrow = sorted(
        [id for id in strip.unplaced if id not in wide],
        key = lambda x: strip.boxes[x].height
    )

    # FFDH on wide
    # TODO: get better data structures
    shelves = {0: [0, 0]} # shelves[shelf] = [next open x pos, height of tallest box on shelf]
    while (wide):
        id = wide.pop()

        placed = False

        Y = -1
        for y in shelves:
            x = 0
            Y = y
            while (not strip.is_valid_placement(id, (x, y))) and x < strip.width:
                x += 1

            if (strip.is_valid_placement(id, (x, y))):
                placed = True
                strip.place(id, (x, y))
                shelves[y][0] += strip.boxes[id].width
                if (shelves[y][1] == 0):
                    shelves[y][1] = strip.boxes[id].height
            
        if (placed):
            continue
            
        new_shelf_height = Y + shelves[Y][1] if Y != -1 else 0
        strip.place(id, (0, new_shelf_height))
        shelves[new_shelf_height] = [0, 0]
        shelves[new_shelf_height][0] = strip.boxes[id].width
        shelves[new_shelf_height][1] = strip.boxes[id].height

    boxes_by_shelf = {}
    for id, pos in strip.placements.items():
        x, y = pos
        if (y not in boxes_by_shelf):
            boxes_by_shelf[y] = []

        boxes_by_shelf[y].append((id, (x, y)))

    strip.clear_placements()

    # sort the widest shelves to the bottom
    widest_shelves = [shelf for shelf, info in shelves.items()
                      if info[0] > (strip.width * (m + 1)) / (m + 2)]
    
    new_shelves = {}
    new_shelf_height = 0
    while (widest_shelves):
        shelf = widest_shelves.pop()

        new_shelves[new_shelf_height] = [0, 0]

        for id, (x, _) in boxes_by_shelf[shelf]:
            strip.place(id, (x, new_shelf_height))
            new_shelves[new_shelf_height][0] += strip.boxes[id].width
            
            if (strip.boxes[id].height > new_shelves[new_shelf_height][1]):
                new_shelves[new_shelf_height][1] = strip.boxes[id].height

        del boxes_by_shelf[shelf]

        new_shelf_height += new_shelves[new_shelf_height][1]

    for old_shelf in boxes_by_shelf.values():
        new_shelves[new_shelf_height] = [0, 0]
        for id, (x, y) in old_shelf:
            strip.place(id, (x, new_shelf_height))
            new_shelves[new_shelf_height][0] += strip.boxes[id].width

            if (strip.boxes[id].height > new_shelves[new_shelf_height][1]):
                new_shelves[new_shelf_height][1] = strip.boxes[id].height

        new_shelf_height += new_shelves[new_shelf_height][1]

    # FFDH on narrow
    while (narrow):
        id = narrow.pop()

        placed = False

        Y = -1
        for y in new_shelves:
            x = 0
            Y = y
            while (not strip.is_valid_placement(id, (x, y))) and x < strip.width:
                x += 1

            if (strip.is_valid_placement(id, (x, y))):
                placed = True
                strip.place(id, (x, y))
                new_shelves[y][0] += strip.boxes[id].width
                if (new_shelves[y][1] == 0):
                    new_shelves[y][1] = strip.boxes[id].height
            
        if (placed):
            continue
        
        
        new_shelf_height = Y + new_shelves[Y][1] if Y != -1 else 0
        strip.place(id, (0, new_shelf_height))
        new_shelves[new_shelf_height] = [0, 0]
        new_shelves[new_shelf_height][0] = strip.boxes[id].width
        new_shelves[new_shelf_height][1] = strip.boxes[id].height

    return strip

