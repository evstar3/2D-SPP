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
        self.width = [int(n.strip()) for n in fp.readline().split(' ')][0]
        
        self.boxes = [Box.from_string(line) for line in fp.readlines()]

        self.max_height = sum(box.height for box in self.boxes)

class Strip:
    def __init__(self, problem: Problem) -> None:
        self.problem = problem
        
        self.clear_placements()

        self.BL_soln  = list(range(problem.n_boxes))

    def clear_placements(self):
        ids = list(range(self.problem.n_boxes))
        random.shuffle(ids)
        self.placements = {id: None for id in ids}

    def unplaced(self):
        return [id for id, pos in self.placements.items() if pos is None]

    def _merge_border_chars(c1: str, c2: str) -> str: # WORK IN PROGRESS
        if (len(c1) != 1 or len(c2) != 1):
            raise RuntimeError(f'_merge_border expects two box drawing characters')
        
        map = {
        #              ┘        ┌        ┐        ─        │
            '└': {'┘':'┴', '┌':'├', '┐':'┼', '─':'┴', '│':'├'},
            '┘':          {'┌':'┼', '┐':'┤', '─':'┴', '│':'┤'},
            '┌':                   {'┐':'┬', '─':'┬', '│':'├'},
            '┐':                            {'─':'┬', '│':'┤'},
            '─':                                     {'│':'┼'},
            '│':                                            {},
        }

        for x, arr in map.items():
            for y, z in arr.items():
                map[y][x] = z

        if (c1 == c2):
            return c1
        
        if (c1 == '┼' or c2 == '┼'):
            return '┼'
        
        if (c1 in ('·', ' ')):
            return c2
        
        if (c2 in ('·', ' ')):
            return c1
        
        return map[c1][c2]

    def print_strip(self) -> None:
        grid = np.full((self.problem.width + 1, self.problem.max_height + 1), '·')
    
        for id, pos in self.placements.items():
            if not pos:
                continue

            x, y = pos

            w = self.problem.boxes[id].width
            h = self.problem.boxes[id].height

            # clear box
            grid[x : x + w, y : y + h] = ' '

            # set box horizontal lines
            grid[x : x + w, y    ] = '─'
            grid[x : x + w, y + h] = '─' 

            # set box vertical lines
            grid[x,     y : y + h] = '│'
            grid[x + w, y : y + h] = '│'

            # set box corners
            grid[x    , y    ] = '└'
            grid[x + w, y    ] = '┘'
            grid[x    , y + h] = '┌'
            grid[x + w, y + h] = '┐'

        for c in range(grid.shape[1]):
            for r in range(grid.shape[0]):
                char = grid[r][grid.shape[1] - c - 1]

                if (char in ['┌','└','─']):
                    end = '─'
                else:
                    end = ' '

                print(char, end=end)
            print()

    def is_collision(b1: Box, x1: int, y1: int, b2: Box, x2: int, y2: int):
        return all((
            x1 + b1.width > x2,
            x1 < x2 + b2.width,
            y1 + b1.height > y2,
            y1 < y2 + b2.height,
        ))
    
    def is_valid_placement(self, box_id: int, x: int, y: int) -> bool:
        if box_id not in self.unplaced():
            return False
        
        box = self.problem.boxes[box_id]
        out_of_bounds = any((
            x < 0,
            y < 0,
            x + box.width > self.problem.width,
            y + box.height > self.problem.max_height
        ))

        if (out_of_bounds):
            return False
        
        for b2, pos in self.placements.items():
            if pos is None:
                continue

            if (Strip.is_collision(box, x, y, self.problem.boxes[b2], *pos)):
                return False

        return True

    def place(self, box_id: int, x: int, y: int):
        if (self.placements[box_id]):
            raise RuntimeError(f'Box(id={box_id}) already placed')
        
        is_valid = self.is_valid_placement(box_id, x, y)
        if (not is_valid):
            raise RuntimeError('invalid placement')
        
        self.placements[box_id] = (x, y)

    def is_valid_move(self, box_id: int, x: int, y: int) -> bool:
        if box_id in self.unplaced():
            return False
        
        old_x, old_y = self.placements[box_id]
        self.placements[box_id] = None

        if (self.is_valid_placement(box_id, x, y)):
            self.place(box_id, old_x, old_y)
            return True
        
        self.place(box_id, old_x, old_y)
        return False

    def move_box(self, box_id: int, x: int, y: int):       
        if (not self.is_valid_move(box_id, x, y)):
            raise RuntimeError('invalid move')

        self.placements[box_id] = None
        self.place(box_id, x, y)

    def max_height(self):
        if (len(self.unplaced()) == self.problem.n_boxes):
            return 0
        
        return max(self.problem.boxes[box_id].height + pos[1] for box_id, pos in self.placements.items() if pos)


