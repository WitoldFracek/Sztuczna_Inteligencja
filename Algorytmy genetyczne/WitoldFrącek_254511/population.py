from staticData import StaticData
from factoryPlacement import FactoryIndividual
from consts import *
import random


class DataCollector:
    def __init__(self):
        self.__measures = []

    def __add__(self, other):
        self.__measures += other
        return self

    @property
    def best(self):
        return min(self.__measures)

    @property
    def worst(self):
        return max(self.__measures)

    @property
    def average(self):
        return sum(self.__measures) / len(self.__measures)

    @property
    def deviation(self):
        import math
        avg = self.average
        return math.sqrt(sum([(x - avg) ** 2 for x in self.__measures]) / len(self.__measures))


class Population:
    def __init__(self, population_size: int,
                 mode: str,
                 mode_size: (int, int),
                 tournament_size: float,
                 crossover_probability: float,
                 mutation_probability: float,
                 selector: str):
        self.__data = StaticData(mode)
        self.__data.prepare_matrices()
        self.__individuals = []
        self.__best_so_far = 1e10
        self.__best = self.__best_so_far
        self.__worst_so_far = 0
        self.__worst = self.__worst_so_far
        self.__average = 0
        self.__tournament_size = tournament_size
        self.__crossover_probability = crossover_probability
        self.__mutation_possibility = mutation_probability
        self.__selector = selector
        for _ in range(population_size):
            ind = FactoryIndividual(self.__data.machine_count, mode_size)
            ind.random_start()
            #ind.ordered_start()
            self.__individuals.append(ind)
        self.__set_stats()

    def fitting(self):
        return [ind.fitting(self.__data.value_matrix) for ind in self.__individuals]

    def tournament_selection(self):
        count = max(1, int(len(self.__individuals) * self.__tournament_size))
        chosen = random.sample(self.__individuals, count)
        pairs = list(zip([ind.fitting(self.__data.value_matrix) for ind in chosen], chosen))
        pairs.sort(key=lambda x: x[0])
        return pairs[0][1]

    def roulette_selection(self):
        fittings = self.fitting()
        minimum = min(fittings) - 1
        distances = [f - minimum for f in fittings]
        distance_sum = sum(distances)
        weights = [distance_sum / d for d in distances]
        scale = sum(weights)
        spread = [w / scale for w in weights]
        roulette_table = self.__assign_spread(spread)
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

    def random_population(self):
        for ind in self.__individuals:
            ind.random_start()

    def select(self):
        if self.__selector == TOURNAMENT:
            return self.tournament_selection()
        elif self.__selector == ROULETTE:
            return self.roulette_selection()
        else:
            raise Exception(f'Wrong selection method. Available are: {TOURNAMENT} and {ROULETTE}')

    def iterate(self):
        new_ind = []
        for _ in range(self.size // 2):
            p1 = self.select()
            p2 = self.select()
            if random.random() < self.__crossover_probability:
                # alias for p1.crossover(p2, genes=1)
                o1 = p1 * p2
            else:
                o1 = p1.clone()
            if random.random() < self.__crossover_probability:
                # alias for p2.crossover(p1, genes=2)
                o2 = p2 * p1
            else:
                o2 = p2.clone()
            if random.random() < self.__mutation_possibility:
                # alias for o1.mutate()
                ~o1
            if random.random() < self.__mutation_possibility:
                # alias o2.mutate()
                ~o2
            o1.calculate_distances()
            o2.calculate_distances()
            new_ind.append(o1)
            new_ind.append(o2)
        self.__individuals = new_ind
        self.__set_stats()

    def __set_stats(self):
        adapt = self.fitting()
        self.__best = min(adapt)
        self.__worst = max(adapt)
        self.__average = sum(adapt) / len(adapt)

    def best_individuals(self, count=-1):
        adapt = self.fitting()
        sor = list(zip(adapt, self.__individuals))
        sor.sort(key=lambda pair: pair[0])
        return sor[:count]

    def __len__(self):
        return len(self.__individuals)

    def __iter__(self):
        return iter(self.__individuals)

    @property
    def size(self):
        return len(self.__individuals)

    @property
    def individuals(self):
        return tuple(self.__individuals)

    @property
    def best(self):
        return self.__best

    @property
    def worst(self):
        return self.__worst

    @property
    def average(self):
        return self.__average


