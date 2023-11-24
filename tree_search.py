#!/usr/bin/env python3

from strip import Strip, Problem
import itertools
import tqdm
import heapq
import math
import random

class TreeNode():
    def __init__(self, parent: "TreeNode", problem: Problem, placements: dict) -> None:
        self.parent = parent
        self.strip = Strip(problem, placements)

        self.visited = False

        self.playout_height = 0
        self.playouts = 0

        self.children = []

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
    
    def remaining_height(self):
        return sum(self.strip.problem.boxes[id].height for id in self.strip.unplaced)
      
    def expand(self):
        if (self.visited):
            raise RuntimeError('node already expanded')
        
        self.visited = True
        for id, pos in self.possible_placements():
            child_node = TreeNode(self, self.strip.problem, self.strip.placements)
            child_node.strip.place(id, pos)
            self.children.append(child_node)

        return self.children

    
    def __lt__(n1: 'TreeNode', n2: 'TreeNode'):
        return False
    
    def do_playout(self):
        copy = TreeNode(None, self.strip.problem, self.strip.placements)
        while (copy.strip.unplaced):
            id, pos = random.choice(list(copy.possible_placements()))
            copy.strip.place(id, pos)
        return copy.strip.max_height

class Tree():
    def __init__(self, problem: Problem) -> None:
        self.root = TreeNode(None, problem, None)

        self.visited = []
        self.complete = []
        self.frontier = [((self.root.strip.max_height + self.root.remaining_height()), self.root)]

    def visit_best(self):
        cost, node = heapq.heappop(self.frontier)

        heapq.heappush(self.visited, (cost, node))

        if (len(node.strip.unplaced) == 0):
            heapq.heappush(self.complete, (cost, node))

        for child in node.expand():
            child_cost = child.strip.max_height + child.remaining_height()
            heapq.heappush(self.frontier, (child_cost, child))

    def search(self, max_iters) -> TreeNode | None:
        for _ in tqdm.tqdm(range(max_iters)):
            self.visit_best()

        if (len(self.complete) == 0):
            print(f'No solution found with {max_iters} iterations')
            return None

        return self.complete[0][1]

def run_tree_search(problem, iters):
    tree: Tree = Tree(problem)
    if (tree is None):
        return None
    return tree.search(iters).strip

class MCTS_Tree():
    def __init__(self) -> "MCTS_Tree":
        self.root = TreeNode(None, problem, None)

        self.frontier = [(self.root.strip.max_height + self.cost_func(self.root), self.root)]

    def search(self, rounds) -> TreeNode:
        pass

    def visit_best(self):
        curr = self.root

        while (curr.children):
            curr = sorted(curr.children, key=lambda x: x.playout_height / x.playouts)[0]

        playout_height = curr.do_playout()

        while (curr):
            curr.playouts += 1
            curr.playout_height += playout_height
            curr = curr.parent
