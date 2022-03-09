from staticData import StaticData
from factoryPlacement import FactoryIndividual
import numpy as np

EASY = 'easy'
FLAT = 'flat'
HARD = 'hard'
EASY_SIZE = (3, 3)
FLAT_SIZE = (1, 12)
HARD_SIZE = (5, 6)

# Set exercise mode
MODE = HARD
MODE_SIZE = HARD_SIZE


class Population:
    def __init__(self, size):
        self.__data = StaticData(MODE)
        self.__data.prepare_matrices()
        self.__individuals = []
        for _ in range(size):
            ind = FactoryIndividual(self.__data.machine_count, MODE_SIZE)
            ind.random_start()
            #ind.ordered_start()
            self.__individuals.append(ind)

    def fitting(self):
        return [ind.fitting(self.__data.value_matrix) for ind in self.__individuals]

    def best_individuals(self, count=-1):
        adapt = self.fitting()
        sor = list(zip(adapt, self.__individuals))
        sor.sort(key=lambda pair: pair[0])
        ret = [a for a, _ in sor]
        return ret[:count]

    def __len__(self):
        return len(self.__individuals)

    @property
    def size(self):
        return len(self.__individuals)

    @property
    def individuals(self):
        return tuple(self.__individuals)

    # temporaty public
    def debug(self):
        for elem in self.__individuals:
            print(elem.grid)


