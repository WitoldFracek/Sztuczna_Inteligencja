from staticData import StaticData
from factoryPlacement import FactoryIndividual
import numpy as np
import random

EASY = 'easy'
FLAT = 'flat'
HARD = 'hard'
TEST = 'test'
EASY_SIZE = (3, 3)
FLAT_SIZE = (1, 12)
HARD_SIZE = (5, 6)
TEST_SIZE = (1, 8)

# Set exercise mode
MODE = HARD
MODE_SIZE = HARD_SIZE
TOURNAMENT_SIZE = 0.2
CROSSOVER_PROBABILITY = 0.6
MUTATION_PROBABILITY = 0.7


class Population:
    def __init__(self, size):
        self.__data = StaticData(MODE)
        self.__data.prepare_matrices()
        self.__individuals = []
        self.best_so_far = 1e10
        self.best = self.best_so_far
        self.worst_so_far = 0
        self.worst = self.worst_so_far
        self.average = 0
        for _ in range(size):
            ind = FactoryIndividual(self.__data.machine_count, MODE_SIZE)
            ind.random_start()
            #ind.ordered_start()
            self.__individuals.append(ind)

    def fitting(self):
        return [ind.fitting(self.__data.value_matrix) for ind in self.__individuals]

    def tournament_selection(self):
        count = max(1, int(len(self.__individuals) * TOURNAMENT_SIZE))
        chosen = random.sample(self.__individuals, count)
        pairs = list(zip([ind.fitting(self.__data.value_matrix) for ind in chosen], chosen))
        pairs.sort(key=lambda x: x[0])
        return pairs[0][1]

    def roulette_selection(self):
        fittings = self.fitting()
        combined = sum(fittings)
        weights = [combined / fit for fit in fittings]
        scale = sum(weights)
        spread = [w / scale for w in weights]
        roulette_table = self.__assign_spread(spread)
        for i, elem in enumerate(roulette_table):
            print(elem[1] - elem[0], self.__individuals[i].fitting(self.__data.value_matrix))
        print('=====================')
        return self.__spin_roulette(roulette_table)

    def __assign_spread(self, spread):
        counter = 0.0
        ret = []
        for ind, s in zip(self.__individuals, spread):
            ret.append((counter, counter + s, ind))
            counter += s
        return ret

    def __spin_roulette(self, table):
        number = random.random()
        for beg, end, ind in table:
            if beg <= number < end:
                return ind
        return table[-1][2]

    def iterate(self):
        new_ind = []
        for _ in range(self.size // 2):
            p1 = self.roulette_selection()
            p2 = self.roulette_selection()
            # p1 = self.tournament_selection()
            # p2 = self.tournament_selection()
            if random.random() < CROSSOVER_PROBABILITY:
                o1 = p1.crossover(p2, genes=1)
            else:
                o1 = p1.clone()
            if random.random() < CROSSOVER_PROBABILITY:
                o2 = p2.crossover(p1, genes=2)
            else:
                o2 = p2.clone()
            if random.random() < MUTATION_PROBABILITY:
                o1.mutate()
            if random.random() < MUTATION_PROBABILITY:
                o2.mutate()
            o1.calculate_distances()
            o2.calculate_distances()
            new_ind.append(o1)
            new_ind.append(o2)
        self.__individuals = new_ind
        self.__set_stats()

    def __set_stats(self):
        adapt = self.fitting()
        adapt.sort()
        self.best = adapt[0]
        self.worst = adapt[-1]
        if adapt[0] < self.best_so_far:
            self.best_so_far = adapt[0]
        if adapt[-1] > self.worst_so_far:
            self.worst_so_far = adapt[-1]
        self.average = sum(adapt) / len(adapt)

    def best_individuals(self, count=-1):
        adapt = self.fitting()
        sor = list(zip(adapt, self.__individuals))
        sor.sort(key=lambda pair: pair[0])
        return sor[:count]

    def __len__(self):
        return len(self.__individuals)

    @property
    def size(self):
        return len(self.__individuals)

    @property
    def individuals(self):
        return tuple(self.__individuals)

    # temporary public
    def debug(self):
        f = self.__individuals[0]
        for i in range(3):
            f.mutate()
            print(f.grid)

    def data(self):
        return self.__data.value_matrix


