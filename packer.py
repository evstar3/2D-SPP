#!/usr/bin/env python3


import argparse
import sys

from strip import Strip, Problem
import approximation_algorithms

methods = {
    'BL'  : approximation_algorithms.BL,
    'NFDH': approximation_algorithms.NFDH,
    'FFDH': approximation_algorithms.FFDH,
    'SF'  : approximation_algorithms.SF,
}

parser = argparse.ArgumentParser(
    prog='packer.py',
    description='An interface for 2D-SPP problems',
)

parser.add_argument('filename')
parser.add_argument(
    'method',
    help='Available methods: ' + ', '.join(methods),
)
parser.add_argument('-p', '--print-strip', action='store_true')

args = parser.parse_args()

if (args.filename == '--'):
    problem = (Problem(sys.stdin))
else: 
    with open(args.filename) as fp:
        problem = (Problem(fp))

strip = Strip(problem, None)

methods[args.method](strip)

if (args.print_strip):
    strip.print()

print(f'Height: {strip.max_height}')
