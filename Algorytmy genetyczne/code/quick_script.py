import numpy as np
from staticData import StaticData
from factoryPlacement import generate_random_positions, FactoryIndividual
from population import Population
import random
import time
import matplotlib.pyplot as pyl


if __name__ == '__main__':
    pop = Population(4)
    iterations = 10
    # xs = pop.individuals
    # for ind in xs:
    #     print(ind.grid)
    #     print(ind.fitting(pop.data()))
    #     print()
    # for _ in range(iterations):
    #     s = input("-->")
    #     if s == 'exit':
    #         break
    #     pop.iterate()
        # xs = pop.individuals
        # for ind in xs:
        #     print(ind.grid)
        #     print(ind.fitting(pop.data()))
        #     print()
    xs = pop.fitting()
    xs.sort()
    print(xs)
    best = []
    worst = []
    avg = []
    axes = [i for i in range(iterations)]
    for i in range(iterations):
        pop.iterate()
        # xs = pop.fitting()
        # xs.sort()
        # print(xs)
        best.append(pop.best)
        worst.append(pop.worst)
        avg.append(pop.average)
        pyl.plot()
    b, i = pop.best_individuals(1)[0]
    print(i.grid)
    print(f'Best: {b}')

    pyl.plot(axes, best, color='g')
    pyl.plot(axes, worst, color='r')
    pyl.plot(axes, avg, color='b')

    pyl.show()
    #
    # xs = pop.fitting()
    # xs.sort()
    # print(xs)
    # score, ind = pop.best_individuals(1)[0]
    # print(score)
    # print(ind.grid)





    # for _ in range(10):
    #     print('Tournament:', pop.tournament_selection().fitting(pop.data()))
    #     print('Roulette:', pop.roulette_selection().fitting(pop.data()))
    #     print()
    # start = time.time()
    # for _ in range(10000):
    #     pop.fitting()
    # end = time.time()
    # print(end - start)



