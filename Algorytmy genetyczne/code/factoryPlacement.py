import numpy as np
import random

# EASY_SIZE = (3, 3)
# FLAT_SIZE = (1, 12)
# HARD_SIZE = (4, 5)
#
# MODE_SIZE = EASY_SIZE


def generate_random_positions(count, xszie, ysize):
    positions = []
    for i in range(xszie):
        for j in range(ysize):
            positions.append((i, j))
    random.shuffle(positions)
    return positions[:count]


def count_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + (y1 - y2)


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
        self.distance_matrix = self.__count_distances()

    def __count_distances(self):
        ret = np.zeros((self.__machine_count, self.__machine_count), dtype=np.int64)
        for key_x in self.__positions:
            for key_y in self.__positions:
                x1, y1 = self.__positions[key_x]
                x2, y2 = self.__positions[key_y]
                distance = count_distance(x1, y1, x2, y2)
                ret[key_x, key_y] = distance
        return ret

    def adaptation(self, costs):
        return np.sum(costs * self.distance_matrix)

    @property
    def machine_count(self):
        return self.__machine_count








