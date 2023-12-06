# 2D-SPP
Evan Day

## Overview
One canonical problem in math and computer science is *packing.*
This repository examines a specific subset of rectangular packing called **strip packing**, where the goal is to fit a set of rectangles into a 'strip' of fixes width while minimizing height.

## Repository Structure
```
.
├── approximation_algorithms.py     # contains multiple polynomial approximation algorithms
├── data                            # contains the data for the project
│   ├── BKW
│   ├── by_size                     # all the datasets, ordered by the numbmer of boxes
│   ├── C
│   ├── N_T
│   └── ZDF
├── genetic.py                      # genetic algorithm
├── packer.py                       # CLI for running the algorithms and visualizing results
├── README.md
├── strip.py                        # data structures for storing and manipulating strip packing problems
└── tree_search.py                  # traditional and Monte Carlo tree search algorithms
```

## `packer.py` Usage
Run `packer.py --help` for more information on running from the command line.

## Algorithm Description
### BL
**BL** is an acronym for Bottom-up Left-justified.
Given a random order of boxes, the algorithm places each box as low as possible and aligns it with the box or edge to the left.
### FFDH
**FFDH** is an acrynym for First Fit Decreasing Height.
This algorithm places the boxes on shelves in order of decreasing height.
If a box is not able to fit on a shelf, a new shelf is created above the current shelf.
Boxes may only be placed at the end of the current shelf.
### NFDH
**NFDH** is an acryonym for Next Fit Decreasing Height.
This algorithm places the boxes on shelves in order of decreasing height.
If a box is not able to fit on a shelf, a new shelf is created above the current shelf.
This algorithm differs from FFDH because boxes may be placed on the current shelf or any previous shelf.
### SF
**SF** is an acronym for Split-Fit.
This algorithm splits the boxes into *wide* and *narrow* sets.
These sets are placed using FFDH, but the algorithm also sorts the shelves so as to create more space.
### TS
**TS** is an acronym for Tree Search.
This algorithm creates a search tree where an action represents placing a certain box at a certain position.
This version of tree search requires the `--rounds` flag, which determines how many tree nodes the algorithm should explore.
The algorithm is similar to A* where the current cost is the height of the strip and the hueristic function is the total height of all the yet unplaced boxes.

Notes:
- the hueristic function intentionally overestimates because an underestimating hueristic would search a majority of the tree and take a *long* time to finish
### MCTS
**MCTS** is an acronym for Monte Carlo Tree Search
This algorithm performs random playouts from the current position to determine which action to take.

Notes: 
- you may supply a timeout for each round of MCTS
### GEN

