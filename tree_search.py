#!/usr/bin/env python3

from strip import Strip, Problem
import itertools
import tqdm
import heapq
import math
import random
import datetime
import sys
import functools

class TreeNode():
    def __init__(self, parent: "TreeNode", problem: Problem, placements: dict) -> None:
        self.parent = parent
        self.strip = Strip(problem, placements)

        self.children = None

        # used for MCTS
        self.child_generator = None
        self.wins = 0
        self.playouts = 0

    def smart_prospectives(self, box_id: int):
        '''
        Makes some assumptions about prospective placements to
        reduce the tree's branching factor.
        
        Assumptions:
        - First box is placed in the bottom left corner
        - Boxes are best placed when touching another box (corners inclusive)

        Returns a generator of (x, y) tuples
        '''
        if (box_id in self.strip.placements):
            raise RuntimeError

        if (len(self.strip.placements) == 0):
            yield (0,0)
        else:
            test_box = self.strip.boxes[box_id]
            for id, (x, y) in self.strip.placements.items():
                box = self.strip.boxes[id]

                left_edge = x - test_box.width
                right_edge = x + box.width
                bottom_edge = y - test_box.height
                top_edge = y + box.height

                locs = set(itertools.chain(
                    ((right_edge, t) for t in range(bottom_edge, top_edge + 1)),
                    ((left_edge, t) for t in range(bottom_edge, top_edge + 1)),
                    ((t, bottom_edge) for t in range(left_edge, right_edge + 1)),
                    ((t, top_edge) for t in range(left_edge, right_edge + 1)),
                ))

                for loc in locs:
                    if (self.strip.is_valid_placement(box_id, loc)):
                        yield loc

    def possible_placements(self):
        for id in self.strip.unplaced:
            for pos in self.smart_prospectives(id):
                yield (id, pos)
    
    def remaining_height(self):
        return sum(self.strip.boxes[id].height for id in self.strip.unplaced)
      
    def expand(self):        
        if (self.children is None):
            self.children = []
        else:
            raise RuntimeError

        for id, pos in self.possible_placements():
            child_node = TreeNode(self, self.strip, self.strip.placements)
            child_node.strip.place(id, pos)
            self.children.append(child_node)
            yield child_node

    def __lt__(n1: 'TreeNode', n2: 'TreeNode'):
        return False
    
class Tree():
    def __init__(self, problem: Problem) -> None:
        self.root = TreeNode(None, problem, None)

        self.visited = []
        self.complete = []
        self.frontier = [((self.root.strip.total_height + self.root.remaining_height()), self.root)]

    def visit_best(self):
        score, node = heapq.heappop(self.frontier)

        heapq.heappush(self.visited, (score, node))

        if (len(node.strip.unplaced) == 0):
            heapq.heappush(self.complete, (score, node))

        for child in node.expand():
            child_score = child.strip.total_height + child.remaining_height()
            heapq.heappush(self.frontier, (child_score, child))

    def search(self, rounds) -> TreeNode | None:
        for _ in tqdm.tqdm(range(rounds)):
            self.visit_best()

        if (len(self.complete) == 0):
            print(f'No solution found with {rounds} rounds')
            return None

        return self.complete[0][1].strip

class MCTS():
    def __init__(self, problem: Problem):
        self.root = TreeNode(None, problem, None)
        self.exploration_factor = 1
        
    def search(self, timeout) -> TreeNode:
        node = self.root
        while (node.strip.unplaced):
            print(f'placing box {len(node.strip.placements) + 1}/{self.root.strip.n_boxes}...')

            sample_size = 5
            avg = sum(MCTS.do_playout(node.strip).total_height for _ in range(sample_size)) / sample_size

            start = datetime.datetime.now()
            while (datetime.datetime.now() < start + datetime.timedelta(seconds=timeout)):
                self.MC_round(node, avg)
            
            print([n.playouts for n in node.children])
            node = sorted(node.children, key=lambda x: (x.playouts, -x.strip.total_height), reverse=True)[0]
        
        return node.strip

    def MC_round(self, root, avg):
        curr = root

        # selection
        while curr.strip.unplaced:
            try:
                if (not curr.child_generator):
                    curr.child_generator = curr.expand()
                curr = next(curr.child_generator)
                break
            except StopIteration:
                curr = sorted(curr.children, key=self.exploration_score, reverse=True)[0]

        # simulation
        strip = MCTS.do_playout(curr.strip)
        isWin = 1 if strip.total_height < avg else 0

        # backpropagation
        while (curr):
            curr.playouts += 1
            curr.wins += isWin
            curr = curr.parent

    def do_playout(strip: Strip):
        cop = TreeNode(None, strip, strip.placements)
        while (cop.strip.unplaced):
            id, pos = random.choice(list(cop.possible_placements()))
            cop.strip.place(id, pos)
        return cop.strip

    def exploration_score(self, node: TreeNode):
        '''
        This function gives a node a score to determine whether or not it should be explored
        during MCTS. This allows MCTS to balance deep exploration of good paths vs. new
        exploration.
        '''
        winrate = node.wins / node.playouts

        if (node.parent):
            ignored_factor = math.sqrt(math.log2(node.parent.playouts) / node.playouts)
        else:
            ignored_factor = math.inf

        return winrate + self.exploration_factor * ignored_factor


def run_tree_search(problem, rounds=100):
    return Tree(problem).search(rounds)

def run_MCTS(problem, timeout=2):
    print(f'{timeout=}')
    return MCTS(problem).search(timeout)


