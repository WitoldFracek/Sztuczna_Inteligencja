import numpy as np
from staticData import StaticData
from factoryPlacement import generate_random_positions, FactoryIndividual
from population import Population
import random


if __name__ == '__main__':
    pop = Population(20)
    xs = pop.get_adaptations()
    best = pop.best_individuals(5)
    print(xs)
    print(best)



