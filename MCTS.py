#!/usr/bin/env python3

import sys
from strip import Strip, Problem
import itertools

import random

class TreeNode():
    def __init__(self, problem: Problem, placements: dict, parent: "TreeNode") -> None:
        self.strip = Strip(problem, placements)
        self.parent = parent

    def lazy_prospectives(self, box_id: int):
        '''
        Return every location less than (max height + 1) in the
        strip where the box could be legally placed.

        Returns a generator of (x, y) tuples
        '''

        if (box_id in self.strip.placements):
            yield
        else:
            box = self.strip.problem.boxes[box_id]
            yield from (
                pos for pos in
                    itertools.product(
                        range(self.strip.problem.width - box.width + 1),
                        range(self.strip.max_height() + 1)
                    )
                if self.strip.is_valid_placement(box_id, pos)
            )
    
    def smart_prospectives(self, box_id: int):
        '''
        Makes some assumptions about prospective placements to
        reduce the tree's branching factor.
        
        Assumptions:
        - First box is placed in the bottom left corner
        - Boxes are best placed when touching another box (corners inclusive)

        Returns a generator of (x, y) tuples
        '''
        if (len(self.strip.placements) == 0):
            yield (0,0)
        else:
            yield from (pos for pos in self.lazy_prospectives(box_id)
                        if self.strip.would_touch_other_box(box_id, pos))
    
    def possible_placements(self):
        for id in self.strip.unplaced:
            for pos in self.smart_prospectives(id):
                yield (id, pos)

    def greedy_score(self, box_id: int, pos: tuple[int, int]):
        return max(self.strip.max_height(), pos[1] + self.strip.problem.boxes[box_id].height)

with open(sys.argv[1]) as fp:
    prob = Problem(fp)

node: TreeNode = TreeNode(prob, {0: (0,0), 1: (2,0)}, None)

id, pos = min(node.possible_placements(), key=lambda tup: node.greedy_score(tup[0], tup[1]))
node.strip.place(id, pos)

node.strip.print()
print(node.strip.max_height())




