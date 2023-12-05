#!/usr/bin/env python3

from strip import Strip, Problem
import itertools
import tqdm
import heapq
import math
import random
import datetime

class TreeNode():
    def __init__(self, parent: "TreeNode", problem: Problem, placements: dict) -> None:
        self.parent = parent
        self.strip = Strip(problem, placements)

        # used for MCTS
        self.unvisited_children = None
        self.visited_children = None
        self.playout_height = 0
        self.playouts = 0

    def lazy_prospectives(self, box_id: int):
        '''
        Return every location less than (max height + 1) in the
        strip where the box could be legally placed.

        Returns a generator of (x, y) tuples
        '''

        if (box_id in self.strip.placements):
            yield
        else:
            box = self.strip.boxes[box_id]
            yield from (
                pos for pos in
                    itertools.product(
                        range(self.strip.width - box.width + 1),
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
        return sum(self.strip.boxes[id].height for id in self.strip.unplaced)
      
    def expand(self):
        if (self.unvisited_children):
            raise RuntimeError('node already expanded')
        
        self.unvisited_children = []
        self.visited_children = []

        for id, pos in self.possible_placements():
            child_node = TreeNode(self, self.strip, self.strip.placements)
            child_node.strip.place(id, pos)
            self.unvisited_children.append(child_node)

        return self.unvisited_children

    
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
        self.root.expand()

        self.exploration_factor = problem.max_height * 0.5
        
    def search(self, timeout=datetime.timedelta(seconds=2)) -> TreeNode:
        node = self.root
        while (node.strip.unplaced):
            print(f'placing box {len(node.strip.placements)}/{self.root.strip.n_boxes}...')

            start = datetime.datetime.now()
            while (datetime.datetime.now() < start + timeout):
                self.MC_round(node)

            print(len(node.unvisited_children))
            nodes = sorted(node.visited_children, key=lambda x: x.playouts, reverse=True)
            print([n.playouts for n in nodes])
            node = nodes[0]
        
        return node.strip

    def MC_round(self, root):
        # generate children if node has not been expanded
        if (root.unvisited_children is None):
            root.expand()

        curr = root

        # selection
        while not curr.unvisited_children:
            if (not curr.visited_children):
                return

            curr_score = self.exploration_score(curr)
            child_score, child = sorted(((self.exploration_score(child), child) for child in curr.visited_children), reverse=True)[0]
            if (child_score > curr_score):
                curr = child
            else:
                break

        if (curr.unvisited_children):
            curr = random.choice(curr.unvisited_children)

        # simulation
        strip = MCTS.do_playout(curr.strip)
        playout_height = strip.total_height
        if (curr.parent and curr in curr.parent.unvisited_children):
            curr.parent.visited_children.append(curr)
            curr.parent.unvisited_children.remove(curr)

        # backpropagation
        while (curr):
            curr.playouts += 1
            curr.playout_height += playout_height
            curr = curr.parent

    def do_playout(strip: Strip):
        cop = TreeNode(None, strip, strip.placements)
        while (cop.strip.unplaced):
            id = random.choice(cop.strip.unplaced)

            x = random.randint(0, cop.strip.width - 1)
            y = random.randint(0, cop.strip.max_height - 1)
            while (not cop.strip.is_valid_placement(id, (x, y))):
                x = random.randint(0, cop.strip.width - 1)
                y = random.randint(0, cop.strip.max_height - 1)

            cop.strip.place(id, (x, y))
            break
        return cop.strip

    def exploration_score(self, node: TreeNode):
        '''
        This function gives a node a score to determine whether or not it should be explored
        during MCTS. This allows MCTS to balance deep exploration of good paths vs. new
        exploration.
        '''
        avg_playout_height = node.playout_height / node.playouts
        
        if (node.parent):
            ignored_factor = math.sqrt(math.log2(node.parent.playouts) / node.playouts)
        else:
            ignored_factor = math.inf

        return -avg_playout_height + self.exploration_factor * ignored_factor

