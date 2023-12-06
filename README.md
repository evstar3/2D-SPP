# [2D-SPP](https://github.com/evstar3/2D-SPP)
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
- the hueristic function intentionally overestimates because an underestimating hueristic would search a majority of the tree and take a *very long* time to finish
- the algorithm suffers from poor performance because expanding each node takes a long time. The branching factor can easily surpass 10,000, even after making assumptions about optimal locations for box placement. I recommend running with <30 boxes for usable results
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

## Project Evolution
The project I have completed differs from my original proposal. Here is an excerpt from my project proposal:

> My solutions to this problem would look into tree search, possibly with Monte Carlo Tree Search since the branching factor is huge when the number of objects is non-trivial. I have also considered deep-learning techniques for this problem, and it would be interesting to see how neural networks compare to traditional search algorithms. To add complexity to the project, I may explore the effect of rotations or non-rectangular objects on the packing efficiency.

I decided not to pursue any machine learning techniques because of a few complications, most notably a lack of training data and computing power. After seeing the sheer size of the search trees produced for these problems, I also decided not to consider rotations as this would effectively double that. I also ruled-out non-rectangular objects since the collision detection would because considerably more complicated, leading to even further increased runtimes.

One aspect of my final project that is not in my initial proposal is the genetic algorithm. I am glad that I pursued this approach rather than neural networks because it is efficient and produces excellent results.

## TODO
### Algorithm Performance Overview
I would like to create a summary of multiple algorithms running on the same data sets to more easily compare performance.

### Runtime
I am unhappy with the runtime of many of these algorithms. At 50 boxes, certain algorithms are already gasping for more computing power. Using cProfile, I determined that the majority of runtime is devoted to collision detection, which has to check against every other placed block. This could be improved by running collision detection in parallel, by optimizing the data structures used to represent the strip, or by moving to a compiled language.

### Genetic Algorithms
I would like to implement different mutation / crossover methods, and also do parameter search to determine the best values for generations and generation size.

## Self-Evaluation
I am happy with my work on this project. Although my codebase is relatively small, the implementation was made from scratch, and I have refactored each section numerous times to achieve the highest-quality final product. I think that I covered a good mix of AI methods, including various polynomial approximation algorithms, various forms of tree search, and a genetic algorithm. I have enjoyed seeing the results that each algorithm produces, and it's fun to identify patterns across the algorithms (for example, FFDH's 'shelves' are quite easy to spot). I was especially glad that I got to learn about Monte Carlo tree search, since I know that it is a powerful technique used in a variety of real-world applications, but we only touched on it briefly during class.

