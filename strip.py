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
    def __init__(self, problem: Problem, init_placements: None) -> None:
        self.problem = problem

        self.placements = {}
        self.unplaced = [id for id in range(self.problem.n_boxes)]

        if (init_placements):
            for id, (x, y) in init_placements.items():
                self.place(id, (x, y))

    def clear_placements(self):
        self.placements = {}
        self.unplaced = [id for id in range(self.problem.n_boxes)]

    def would_touch_edge(self, box_id: int, pos: tuple[int, int]) -> bool:
        x, y = pos
        if (x == 0 or y == 0):
            return True
        
        return x + self.problem.boxes[box_id].width == self.problem.width
    
    def are_touching(self, placed_id: int, test_id: int, test_pos: tuple[int, int]) -> bool:
        if (not self.placements[placed_id]):
            raise RuntimeError(f'Box placed_id={placed_id} is not placed')
                        
        placed_x, placed_y = self.placements[placed_id]
        placed_w = self.problem.boxes[placed_id].width
        placed_h = self.problem.boxes[placed_id].height

        test_x, test_y = test_pos
        test_w = self.problem.boxes[test_id].width
        test_h = self.problem.boxes[test_id].height

        # right edge
        if (test_x == placed_x + placed_w):
            if (test_y + test_h >= placed_y and test_y <= placed_y + placed_h):
                return True
            
        # top edge
        if (test_y == placed_y + placed_h):
            if (test_x + test_w >= placed_x and test_x <= placed_x + placed_w):
                return True
        
        # left edge
        if (test_x + test_w == placed_x):
            if (test_y + test_h >= placed_y and test_y <= placed_y + placed_h):
                return True

        # bottom edge
        if (test_y + test_h == placed_y):
            if (test_x + test_w >= placed_x and test_x <= placed_x + placed_w):
                return True

        return False
    
    def would_touch_other_box(self, box_id: int, pos: tuple[int, int]) -> bool:
        for placed_id in self.placements:
            if self.are_touching(placed_id, box_id, pos):
                return True
            
        return False

    def _merge_border_chars(c1: str, c2: str) -> str:
        if (len(c1) != 1 or len(c2) != 1):
            raise RuntimeError(f'_merge_border expects two box drawing characters')
        
        # TODO: get add remaining characters to map
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

    def print(self) -> None:
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

    def is_collision(b1: Box, pos1: tuple[int, int], b2: Box, pos2: tuple[int, int]):
        x1, y1 = pos1
        x2, y2 = pos2
        return x1 + b1.width > x2 and y1 + b1.height > y2 \
                                  and x1 < x2 + b2.width  \
                                  and y1 < y2 + b2.height
            
    def is_valid_placement(self, box_id: int, pos: tuple[int, int]) -> bool:
        if box_id in self.placements:
            return False
        
        box = self.problem.boxes[box_id]
        x, y = pos

        if x < 0 or y < 0:
            return False
        
        if x + box.width > self.problem.width:
            return False

        if y + box.height > self.problem.max_height:
            return False
        
        for b2, pos2 in self.placements.items():
            if (Strip.is_collision(box, pos, self.problem.boxes[b2], pos2)):
                return False
        
        return True

    def place(self, box_id: int, pos: tuple[int, int]):
        if (box_id in self.placements):
            raise RuntimeError(f'Box(id={box_id}) already placed')
        
        is_valid = self.is_valid_placement(box_id, pos)
        if (not is_valid):
            raise RuntimeError('invalid placement')
        
        self.unplaced.remove(box_id)        
        self.placements[box_id] = pos

    def max_height(self):
        if (len(self.placements) == 0):
            return 0
        
        return max(self.problem.boxes[box_id].height + pos[1] for box_id, pos in self.placements.items())


