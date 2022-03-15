import numpy as np
from staticData import StaticData
from factoryPlacement import generate_random_positions, FactoryIndividual
from population import Population
import random
import time


if __name__ == '__main__':
    pop = Population(4)
    xs = pop.fitting()
    xs.sort()
    print(xs)
    for _ in range(3):
        pop.iterate()
    xs = pop.fitting()
    xs.sort()
    print(xs)



    # for _ in range(10):
    #     print('Tournament:', pop.tournament_selection().fitting(pop.data()))
    #     print('Roulette:', pop.roulette_selection().fitting(pop.data()))
    #     print()
    # start = time.time()
    # for _ in range(10000):
    #     pop.fitting()
    # end = time.time()
    # print(end - start)



