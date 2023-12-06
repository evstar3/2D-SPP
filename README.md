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
- the algorithm suffers from poor performance because expanded each node takes a long time. There are thousands of possible placements for each box, even after making assumptions about optimal locations. I recommend running with <30 boxes for usable results
### MCTS
**MCTS** is an acronym for Monte Carlo Tree Search
This algorithm performs random playouts from the current position to determine which action to take.

Notes: 
- you may supply a timeout for each round of MCTS
- the algorithm suffers from poor performance because each random playout takes a long time. I recommend running with <30 boxes for usable results
### GEN
This is a genetic algorithm that relies on the Bottom-up Left-justified algorithm.
In this genetic algorithm, the population is a list of *orders*, and we create *mutations* by swapping boxes in the order.
For each generation, the top 50% are kept for the next generation. The rest of the generation is made up of mutations of those same top 50%.

Notes:
- you may specify the number of gnerations, the generation size, and the number of swaps to do per mutation
- this algorithm is capable of producing the best results out of all the algorithms I've implemented, sometimes even finding perfect solutions (i.e. solutions with no wasted space)

