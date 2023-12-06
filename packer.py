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
    'TS'  : tree_search.run_tree_search,
    'MCTS': tree_search.run_MCTS,
    'GEN' : genetic.run,
}

parser = argparse.ArgumentParser(
    prog='packer.py',
    description='An interface for 2D strip-packing problems',
)

parser.add_argument('filename')
parser.add_argument(
    'method',
    help='available methods: ' + ', '.join(methods),
)
parser.add_argument('-p', '--print-strip', action='store_true', help='prints a visualization of the final packed strip')
parser.add_argument(
    '--rounds',
    required=False,
    type=int,
    help='number of rounds to perform in tree search'
)
parser.add_argument(
    '--generations',
    required=False,
    type=int,
    help='number of generations to run in the genetic algorithm'
)
parser.add_argument(
    '--generation-size',
    required=False,
    type=int,
    help='size of generations in the genetic algorithm'
)
parser.add_argument(
    '--mutation-rate',
    required=False,
    type=int,
    help='number of swaps to perform for a single mutation in the genetic algorithm'
)
parser.add_argument(
    '--timeout',
    required=False,
    type=int,
    help='timeout for each box placement in MCTS'
)

args = parser.parse_args()

if (args.filename == '--'):
    problem = Problem(sys.stdin)
else: 
    with open(args.filename) as fp:
        problem = Problem(fp)

possible_arguments = [
    'rounds',
    'generations',
    'generation_size',
    'mutation_rate',
    'timeout',
]
kwargs = {k: v for k, v in vars(args).items() if v and k in possible_arguments}

soln: Strip | None = methods[args.method](problem, **kwargs)
assert(len(soln.unplaced) == 0)

if soln is None:
    exit(1)

if (args.print_strip):
    soln.print()

print(f'Height: {soln.total_height}')
