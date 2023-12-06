# 2D-SPP
Evan Day

## Overview
One canonical problem in math and computer science is *packing.*
This repository examines a specific subset of rectangular packing called strip packing, where the goal is to fit a set of rectangles into a 'strip' of fixes width while minimizing height.

## Repository Structure
```
.
├── approximation_algorithms.py # contains multiple polynomial approximation algorithms
├── data                        # contains the data for the project
│   ├── BKW
│   ├── by_size                 # all the datasets, ordered by the numbmer of boxes
│   ├── C
│   ├── N_T
│   └── ZDF
├── genetic.py                  # genetic algorithm
├── packer.py                   # CLI for running the algorithms and visualizing results
├── README.md
├── strip.py                    # data structures for storing and manipulating strip packing problems
└── tree_search.py              # traditional and Monte Carlo tree search algorithms
```

7 directories, 11 files

## Usage
This repository contains datasets and algorithm implementations for solving 2D strip packing problems.
The easiest way to interact with the problems is through `packer.py`. Run `packer.py --help` for more information.
