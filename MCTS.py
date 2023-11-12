#!/usr/bin/env python3

import sys
from strip import Strip, Problem
import itertools

import cProfile

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
            return iter(())
        

        return filter(
            lambda pos: self.strip.is_valid_placement(box_id, *pos),
            itertools.product(
                range(self.strip.problem.width),
                range(self.strip.max_height() + 1)
            )
        )
    
    def smart_prospectives(self, box_id: int):
        '''
        Makes some assumptions about prospective placements to
        reduce the tree's branching factor.
        
        Assumptions:
        - Assume boxes are best placed when touching edge of
        strip or another box (corners inclusive)

        Returns a generator of (x, y) tuples
        '''
        return filter(
            lambda pos:
                self.strip.would_touch_other_box(box_id, *pos) or self.strip.would_touch_edge(box_id, *pos),
            self.lazy_prospectives(box_id)
        )
    
    def possible_placements(self):
        for id in self.strip.unplaced:
            for x, y in self.smart_prospectives(id):
                yield (id, (x, y))


with open(sys.argv[1]) as fp:
    prob = Problem(fp)

node: TreeNode = TreeNode(prob, {0: (10,13)}, None)
#node: TreeNode = TreeNode(prob, {}, None)

# print(len(list(node.possible_placements())))

cProfile.run('for _ in range(1000000): node.strip.is_valid_placement(1, 0, 0)')




