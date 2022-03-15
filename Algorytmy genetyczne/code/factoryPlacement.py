import numpy as np
import itertools
import random


def generate_random_positions(count, xsize, ysize):
    positions = []
    x_indices = np.arange(0, xsize, step=1, dtype=np.int64)
    Y_indices = np.arange(0, ysize, step=1, dtype=np.int64)
    ret = np.array([x for x in itertools.product(np.arange(0, xsize, step=1, dtype=np.int64),
                                                 np.arange(0, ysize, step=1, dtype=np.int64))])
    np.random.shuffle(ret)
    return ret[:count]


def calculate_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class FactoryIndividual:
    def __init__(self, machine_count, mode_size):
        self.__MODE_SIZE = mode_size
        self.grid = np.full(self.__MODE_SIZE, -1, dtype=np.int64)
        self.__positions = {}
        self.__machine_count = machine_count
        self.distance_matrix = np.zeros((self.__machine_count, self.__machine_count), dtype=np.int64)

    def random_start(self):
        x, y = self.grid.shape
        random_positions = generate_random_positions(self.__machine_count, x, y)
        for i, pos in enumerate(random_positions):
            self.__positions[i] = pos
            xpos, ypos = pos
            self.grid[xpos, ypos] = i
        self.distance_matrix = self.__calculate_distances()

    # def ordered_start(self):
    #     self.grid = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    #     self.__positions = {
    #         0: (0, 0),
    #         1: (0, 1),
    #         2: (0, 2),
    #         3: (1, 0),
    #         4: (1, 1),
    #         5: (1, 2),
    #         6: (2, 0),
    #         7: (2, 1),
    #         8: (2, 2)
    #     }
    #     self.distance_matrix = self.__count_distances()

    def __calculate_distances(self):
        ret = np.zeros((self.__machine_count, self.__machine_count), dtype=np.int64)
        for key_x in self.__positions:
            for key_y in self.__positions:
                x1, y1 = self.__positions[key_x]
                x2, y2 = self.__positions[key_y]
                distance = calculate_distance(x1, y1, x2, y2)
                ret[key_x, key_y] = distance
        return ret

    def fitting(self, costs):
        return np.sum(costs * self.distance_matrix)

    @property
    def machine_count(self):
        return self.__machine_count








