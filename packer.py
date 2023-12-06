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
    description='An interface for 2D-SPP problems',
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
    help='number of rounds to perform'
)
parser.add_argument(
    '--generations',
    required=False,
    type=int,
    help='number of generations to run'
)
parser.add_argument(
    '--generation-size',
    required=False,
    type=int,
    help='size of generations'
)
parser.add_argument(
    '--mutation-rate',
    required=False,
    type=int,
    help='number of swaps to perform for a single mutation'
)

args = parser.parse_args()

if (args.filename == '--'):
    problem = Problem(sys.stdin)
else: 
    with open(args.filename) as fp:
        problem = Problem(fp)

kwargs = {}

if (args.method == 'TS'):
    if args.rounds:
        kwargs['rounds'] = args.rounds
elif (args.method == 'GEN'):
    if (args.generations):
        kwargs['generations'] = args.generations
    if (args.generation_size):
        kwargs['generation_size'] = args.generation_size
    if (args.mutation_rate):
        kwargs['mutation_rate'] = args.mutation_rate
    
soln: Strip | None = methods[args.method](problem, **kwargs)
assert(len(soln.unplaced) == 0)

if soln is None:
    exit(1)

if (args.print_strip):
    soln.print()

print(f'Height: {soln.total_height}')
