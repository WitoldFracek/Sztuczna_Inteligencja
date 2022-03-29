from consts import *
from population import Population, DataCollector
import matplotlib.pyplot as pyl
import pandas as pd

# Mode settings
MODE = HARD
MODE_SIZE = HARD_SIZE

# Population settings
POPULATION_SIZE = 30
GENERATIONS = 500
TOURNAMENT_SIZE = 0.3
CROSSOVER_PROBABILITY = 0.7
MUTATION_PROBABILITY = 0.4
SELECTION = TOURNAMENT

# display settings
DISPLAY_INITIAL_POPULATION = False
SHOW_GRAPH = True


def only_random(dc: DataCollector, population_size, mode, mode_size, tournament_size, crossover_probability, mutation_probability, selection, generations):
    pop = Population(population_size, mode, mode_size, tournament_size, crossover_probability, mutation_probability, selection)
    for i in range(generations * 10):
        pop.random_population()
        dc += pop.fitting()


def normal(dc: DataCollector, population_size, mode, mode_size, tournament_size, crossover_probability, mutation_probability, selection, generations):
    pop = Population(population_size, mode, mode_size, tournament_size, crossover_probability, mutation_probability, selection)
    best_list = []
    worst_list = []
    average_list = []
    iterations = []

    if DISPLAY_INITIAL_POPULATION:
        xs = pop.fitting()
        xs.sort()
        print(xs)

    if SHOW_GRAPH:
        iterations = [i for i in range(generations)]

    for i in range(generations):
        pop.iterate()
        dc += pop.fitting()
        if SHOW_GRAPH:
            best_list.append(pop.best)
            worst_list.append(pop.worst)
            average_list.append(pop.average)

    if SHOW_GRAPH:
        best = pop.best
        pyl.title(f'Genetic algorithms - factory optimizing\n Best: {best}')
        pyl.xlabel('Generations')
        pyl.ylabel('Production cost')
        pyl.plot(iterations, best_list, color='#66cc00', label='Best')
        pyl.plot(iterations, worst_list, color='#ff3300', label='Worst')
        pyl.plot(iterations, average_list, color='#cccc00', label='Average')
        pyl.legend()
        pyl.show()


def parameters_comparison():
    path1 = '../excel/stats_hard.xlsx'
    path2 = '../excel/stats.xlsx'
    random_values = []
    alg_values = []
    pop_size = [50]
    generations = [300, 600]
    tour_size = [0.3]
    c_max = 2
    counter = 0
    for ps in pop_size:
        for g in generations:
            for ts in tour_size:
                dc = DataCollector()
                only_random(dc, ps, MODE, MODE_SIZE, ts, CROSSOVER_PROBABILITY, MUTATION_PROBABILITY, SELECTION, g)
                random_values.append([ps, g, ts, dc.best, dc.worst, round(dc.average, 2), round(dc.deviation, 2)])
                counter += 1
                print(counter / c_max * 100)
    df = pd.DataFrame(random_values)
    df.to_excel(path1, sheet_name='hard_random')
    for ps in pop_size:
        for g in generations:
            for ts in tour_size:
                dc = DataCollector()
                for i in range(10):
                    normal(dc, ps, MODE, MODE_SIZE, ts, CROSSOVER_PROBABILITY, MUTATION_PROBABILITY, SELECTION, g)
                alg_values.append([ps, g, ts, dc.best, dc.worst, round(dc.average, 2), round(dc.deviation, 2)])
                counter += 1
                print(counter / c_max * 100)
    df = pd.DataFrame(alg_values)
    df.to_excel(path2, sheet_name='hard_alg')


def simple():
    pop = Population(POPULATION_SIZE, MODE, MODE_SIZE, TOURNAMENT_SIZE, CROSSOVER_PROBABILITY, MUTATION_PROBABILITY, SELECTION)
    best_list = []
    worst_list = []
    average_list = []
    iterations = []

    if DISPLAY_INITIAL_POPULATION:
        xs = pop.fitting()
        xs.sort()
        print(xs)

    if SHOW_GRAPH:
        iterations = [i for i in range(GENERATIONS)]

    for i in range(GENERATIONS):
        pop.iterate()
        if SHOW_GRAPH:
            best_list.append(pop.best)
            worst_list.append(pop.worst)
            average_list.append(pop.average)

    if SHOW_GRAPH:
        best = pop.best
        pyl.title(f'Genetic algorithms - factory optimizing\n Best: {best}')
        pyl.xlabel('Generations')
        pyl.ylabel('Production cost')
        pyl.plot(iterations, best_list, color='#66cc00', label='Best')
        pyl.plot(iterations, worst_list, color='#ff3300', label='Worst')
        pyl.plot(iterations, average_list, color='#cccc00', label='Average')
        pyl.legend()
        pyl.show()


if __name__ == '__main__':
    simple()
    # parameters_comparison()
    import winsound
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)

