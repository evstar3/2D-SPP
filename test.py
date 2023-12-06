#!/usr/bin/env python3

import strip, tree_search
import sys
from time import sleep

node: tree_search.TreeNode = tree_search.TreeNode(None, strip.Problem(sys.stdin), {9: (8,13)})
print(node.strip.unplaced)

for pos in sorted(list(node.smart_prospectives(1))):
    node.strip.place(1, pos)
    node.strip.print()
    del node.strip.placements[1]
    node.strip.unplaced.append(1)
    sleep(0.5)
