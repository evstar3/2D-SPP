#!/usr/bin/env python3

import concurrent.futures
from approximation_algorithms import BL
import random
import tqdm

class Generation():
    def __init__(self, problem, size, individuals=None):
        self.problem = problem
        self.size = size

        if individuals is not None:
            self.individuals = individuals
        else:
            self.individuals = [self.random_order() for _ in range(self.size)]


    def random_order(self):
        return random.sample(range(self.problem.n_boxes), k=self.problem.n_boxes)

    def run(self, cores=16):
        with concurrent.futures.ProcessPoolExecutor(max_workers=cores) as executor:
            yield from executor.map(self.run_single, self.individuals, chunksize=max(1, len(self.individuals) // cores))

    def run_single(self, order):
        return BL(self.problem, order=order).total_height, order

def mutate(order):
    cop = [n for n in order]

    i1 = random.randint(0, len(order) - 1)
    i2 = random.randint(0, len(order) - 1)

    while i1 == i2:
        i2 = random.randint(0, len(order) - 1)

    cop[i1], cop[i2] = cop[i2], cop[i1]

    return cop

def run(problem):
    GENERATIONS = 20
    SIZE = 40

    gen_best_height = []

    gen = Generation(problem, SIZE, None)
    for g in tqdm.tqdm(range(GENERATIONS)):
        ranked = sorted(list(gen.run()))

        best = ranked[:SIZE // 2]

        gen_best_height.append(best[0][0])

        mutations = [mutate(ord) for height, ord in best]

        gen = Generation(problem, SIZE, [ord for height, ord in best] + mutations)

    print(gen_best_height)

    return BL(problem, order=best[0][1])


