#!/usr/bin/env python3

import strip, tree_search
import sys

node: tree_search.TreeNode = tree_search.TreeNode(None, strip.Problem(sys.stdin), {9: (3,3)})
node.strip.print()

node.smart_prospectives(1)
