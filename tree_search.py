#!/usr/bin/env python3

import sys
from strip import Strip, Problem
import itertools
import tqdm
import heapq

class TreeNode():
    def __init__(self, problem: Problem, placements: dict) -> None:
        self.strip = Strip(problem, placements)

        self.visited = False
        self.children = set()

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
                        range(self.strip.max_height + 1)
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
    
    def height_plus_remaining_height(self):
        return self.strip.max_height + sum(self.strip.problem.boxes[id].height for id in self.strip.unplaced)
    
    def expand(self):
        if (self.visited):
            raise RuntimeError('node already expanded')
        
        self.visited = True
        for id, pos in self.possible_placements():
            child_node = TreeNode(self.strip.problem, self.strip.placements)
            child_node.strip.place(id, pos)
            self.children.add(child_node)

        return self.children
    
    def __lt__(n1: 'TreeNode', n2: 'TreeNode'):
        return False
    
class Tree():
    def __init__(self, problem: Problem, cost_func) -> None:
        self.root = TreeNode(problem, None)

        self.cost_func = cost_func

        self.visited = []
        self.complete = []
        self.frontier = [(0, self.root)]

    def visit_best(self) -> TreeNode | None:
        cost, node = heapq.heappop(self.frontier)

        heapq.heappush(self.visited, (cost, node))

        for child in node.expand():
            cost = self.cost_func(child)

            if (len(child.strip.unplaced) == 0):
                heapq.heappush(self.complete, (cost, child))
            else:
                heapq.heappush(self.frontier, (cost, child))

        return None

    def search(self, max_iters) -> TreeNode | None:
        for _ in tqdm.tqdm(range(max_iters)):
            self.visit_best()

        if (len(self.complete) == 0):
            return None
        
        return tree.complete[0][1]

with open(sys.argv[1]) as fp:
    prob = Problem(fp)

tree: Tree = Tree(prob, TreeNode.height_plus_remaining_height)
max_iters = 1000
soln = tree.search(max_iters=max_iters)

if soln:
    for cost, node in tree.complete[:20]:
        print(cost)
    soln.strip.print()
    print(soln.strip.max_height)
else:
    print(f'No solution found with {max_iters} iterations')



