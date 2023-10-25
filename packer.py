#!/usr/bin/env python3

import sys
import numpy as np
import random

class Box:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def from_string(line: str):
        tokens = line.split(' ')
        return Box(int(tokens[1]), int(tokens[2]))
    
    def __repr__(self) -> str:
        return f'Box({self.width}, {self.height})'
    
class Problem:
    def __init__(self, fp) -> None:
        self.n_boxes = int(fp.readline().strip())
        self.width, self.optimal_height = [int(n.strip()) for n in fp.readline().split(' ')]
        
        self.boxes = [Box.from_string(line) for line in fp.readlines()]

        self.max_height = sum(box.height for box in self.boxes)

class Strip:
    def __init__(self, problem: Problem, initial_placements=None) -> None:
        self.problem = problem
        self.placements = {}

        if (initial_placements):
            self.placements.update(initial_placements)
            self.unplaced = [i for i in range(problem.n_boxes) if i not in initial_placements]
        else:
            self.unplaced = list(range(problem.n_boxes))

    def print_strip(self) -> None:
        grid = np.full((self.problem.width, self.problem.max_height), '.')
    
        for id, (x, y) in self.placements.items():
            w = self.problem.boxes[id].width
            h = self.problem.boxes[id].height

            # clear box
            grid[x : x + w - 1, y : y + h - 1] = ' '

            # set box horizontal lines
            grid[x : x + w - 1, y        ] = '─'
            grid[x : x + w - 1, y + h - 1] = '─' 

            # set box vertical lines
            grid[x,         y : y + h - 1] = '|'
            grid[x + w - 1, y : y + h - 1] = '|'

            # set box corners
            grid[x        , y        ] = '└'
            grid[x + w - 1, y        ] = '┘'
            grid[x        , y + h - 1] = '┌'
            grid[x + w - 1, y + h - 1] = '┐'

        for c in range(self.problem.max_height):
            for r in range(self.problem.width):
                char = grid[r][self.problem.max_height - c - 1]
                end = '─' if char in ['┌','└','─'] else ' '
                print(grid[r][self.problem.max_height - c - 1], end=end)
            print()

    def isCollision(b1: Box, x1: int, y1: int, b2: Box, x2: int, y2: int):
        # Is the RIGHT edge of r1 to the RIGHT of the LEFT edge of r2?
        # Is the LEFT edge of r1 to the LEFT of the RIGHT edge of r2?
        # Is the BOTTOM edge of r1 BELOW the TOP edge of r2?
        # Is the TOP edge of r1 ABOVE the BOTTOM edge of r2?

        collision = all((
            x1 + b1.width > x2,
            x1 < x2 + b2.width,
            y1 + b1.height > y2,
            y1 < y2 + b2.height,
        ))

        return collision
    
    def isValidPlacement(self, box_id: int, x: int, y: int) -> bool:
        box = self.problem.boxes[box_id]
        out_of_bounds = any((
            x < 0,
            y < 0,
            x + box.width > self.problem.width,
            y + box.height > self.problem.max_height
        ))

        if (out_of_bounds):
            return False, 'Out of bounds'
        
        for b2, (x2, y2) in self.placements.items():
            if (Strip.isCollision(box, x, y, self.problem.boxes[b2], x2, y2)):
                return False, 'Collision'

        return True, None

    def place(self, box_id: int, x: int, y: int):
        if (box_id not in self.unplaced):
            raise RuntimeError(f'Box(id={box_id}) already placed')
        
        isValid, msg = self.isValidPlacement(box_id, x, y)
        if (not isValid):
            raise RuntimeError(msg)
        
        self.unplaced.remove(box_id)
        self.placements[box_id] = (x, y)


strip = Strip(Problem(sys.stdin))
while strip.unplaced:
    box_id = strip.unplaced[0]
    x = 0
    y = 0
    while (not strip.isValidPlacement(box_id, x, y)[0]):
        x = random.randint(0, strip.problem.width)
        y = random.randint(0, strip.problem.max_height)

    strip.place(box_id, x, y)

strip.print_strip()


