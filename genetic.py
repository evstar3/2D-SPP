#!/usr/bin/env python3

import concurrent.futures
from approximation_algorithms import BL
import random
import copy
import time

class Individual():
    def __init__(self, order, score):
        self.order = order
        self.score = score

    def mutate(self, N):
        '''
        Makes a copy of the order and swaps two boxes N times
        '''
        cop = copy.deepcopy(self.order)
        for _ in range(N):
            i1 = random.randint(0, len(cop) - 1)
            i2 = random.randint(0, len(cop) - 1)

            while i1 == i2:
                i2 = random.randint(0, len(cop) - 1)

            cop[i1], cop[i2] = cop[i2], cop[i1]

        return cop

    def __lt__(i1, i2):
        return i1.score < i2.score

class Generation():
    def __init__(self, problem, size, ran=None, to_run=None):
        self.problem = problem
        self.size = size

        if ran is None:
            self.ran = []
        else:
            self.ran = ran

        if to_run is None:
            self.to_run = [self.random_order() for _ in range(size - len(self.ran))]
        else:
            self.to_run = to_run

    def random_order(self):
        return random.sample(list(range(self.problem.n_boxes)), k=self.problem.n_boxes)

    def _run(self, cores):
        with concurrent.futures.ProcessPoolExecutor(max_workers=cores) as executor:
            yield from executor.map(self.run_single, self.to_run, chunksize=max(1, len(self.to_run) // cores))

    def run_and_update(self, cores):
        for order, score in self._run(cores):
            self.ran.append(Individual(order, score))

    def run_single(self, order):
        return order, BL(self.problem, order=order).total_height

def run(problem, generations=15, generation_size=40, mutation_rate=2, cores=4):
    gen_best_height = []

    print(f'{generations=}')
    print(f'{generation_size=}')
    print(f'{mutation_rate=}')
    print(f'{cores=}')

    gen = Generation(problem, generation_size, None)
    for g in range(generations):
        print(f'Generation {g}:')

        start = time.time()
        gen.run_and_update(cores)
        runtime = time.time() - start

        best = sorted(gen.ran)[:generation_size // 2]

        print(f'\tRuntime: {runtime:.2f} seconds')
        print(f'\tBest:    {best[0].score}')
        print(f'\tCutoff:  {best[-1].score}')

        gen = Generation(problem, generation_size, ran=best, to_run=[b.mutate(mutation_rate) for b in best])

    return BL(problem, order=best[0].order)


