import numpy as np
from staticData import StaticData
from factoryPlacement import generate_random_positions, FactoryIndividual
from population import Population
import random
import time


if __name__ == '__main__':
    pop = Population(20)
    for _ in range(10):
        print(pop.tournament_selection())
    # start = time.time()
    # for _ in range(10000):
    #     pop.fitting()
    # end = time.time()
    # print(end - start)



