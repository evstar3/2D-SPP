#!/usr/bin/env python3

import argparse
import sys

from strip import Strip, Problem
import approximation_algorithms
import genetic
import tree_search

methods = {
    'BL'  : approximation_algorithms.BL,
    'NFDH': approximation_algorithms.NFDH,
    'FFDH': approximation_algorithms.FFDH,
    'SF'  : approximation_algorithms.SF,
    'TS'  : lambda problem, rounds: tree_search.Tree(problem).search(rounds),
    'MCTS': lambda problem: tree_search.MCTS(problem).search(), # sunken cost fallacy
    'GEN' : genetic.run
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
    '-r',
    '--rounds',
    required=False,
    type=int,
    help='number of rounds to perform. required for tree search and MCTS'
)

args = parser.parse_args()

if (args.filename == '--'):
    problem = Problem(sys.stdin)
else: 
    with open(args.filename) as fp:
        problem = Problem(fp)

params = [problem]

if (args.method in ['TS']):
    if args.rounds is None:
        print('Tree search requires the --rounds flag')
        exit(1)
    params.append(args.rounds)
    
soln: Strip | None = methods[args.method](*params)

if soln is None:
    exit(1)

if (args.print_strip):
    soln.print()

print(f'Height: {soln.total_height}')
