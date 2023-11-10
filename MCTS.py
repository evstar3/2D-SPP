#!/usr/bin/env python3

import sys
from strip import Strip, Problem
import itertools
import time

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
        if (self.strip.placements[box_id]):
            return iter(())

        x = range(self.strip.problem.width)
        y = range(self.strip.max_height() + 1)

        locations = itertools.product(x, y)

        return filter(
            lambda pos: self.strip.is_valid_placement(box_id, *pos),
            locations
        )
    
    def smart_prospectives(self, box_id: int):
        '''
        Makes some assumptions about prospective placements to
        reduce the tree's branching factor.
        
        Assumptions:
        - Assume boxes are best placed when touching edge of
        strip or another box (corners inclusive)
        '''

        locations = self.lazy_prospectives(box_id)

        return filter(
            lambda pos:
                self.strip.would_touch_other_box(box_id, *pos) or self.strip.would_touch_edge(box_id, *pos),
            locations
        )


with open(sys.argv[1]) as fp:
    prob = Problem(fp)

node: TreeNode = TreeNode(prob, {0: (10,13), 1: (0,0)}, None)

locs = list(node.smart_prospectives(2))
node.strip.print()

for loc in locs:
    node.strip.place(2, *loc)
    node.strip.print()
    time.sleep(0.1)
    node.strip.placements[2] = None

