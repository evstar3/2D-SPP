#!/usr/bin/env python3


import argparse
import sys

from strip import Strip, Problem
import approximation_algorithms
import tree_search

methods = {
    'BL'  : approximation_algorithms.BL,
    'NFDH': approximation_algorithms.NFDH,
    'FFDH': approximation_algorithms.FFDH,
    'SF'  : approximation_algorithms.SF,
    'TS'  : tree_search.run_tree_search,
#    'MCTS': tree_search.run_MCTS,
}

parser = argparse.ArgumentParser(
    prog='packer.py',
    description='An interface for 2D-SPP problems',
)

parser.add_argument('filename')
parser.add_argument(
    'method',
    help='available methods: ' + ', '.join(methods),
)
parser.add_argument('-p', '--print-strip', action='store_true')
parser.add_argument(
    '-i',
    '--max-iters',
    required=False,
    type=int,
    help='required for tree search'
)

args = parser.parse_args()

if (args.filename == '--'):
    problem = (Problem(sys.stdin))
else: 
    with open(args.filename) as fp:
        problem = (Problem(fp))

params = [problem]

if (args.method == 'TS'):
    if args.max_iters is None:
        print('Tree search requires the --max-iters flag')
        exit(1)
    params.append(args.max_iters)
    
soln: Strip | None = methods[args.method](*params)

if soln is None:
    exit(1)

if (args.print_strip):
    soln.print()

print(f'Height: {soln.max_height}')
