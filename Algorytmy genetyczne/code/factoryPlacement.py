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

    @classmethod
    def make_empty(cls):
        return cls(1, (1, 1))

    def random_start(self):
        x, y = self.grid.shape
        random_positions = generate_random_positions(self.__machine_count, x, y)
        for i, pos in enumerate(random_positions):
            self.__positions[i] = pos
            xpos, ypos = pos
            self.grid[xpos, ypos] = i
        self.distance_matrix = self.__calculate_distances()

    def calculate_distances(self):
        self.distance_matrix = self.__calculate_distances()

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

    def clone(self):
        cl = FactoryIndividual.make_empty()
        cl.__positions = self.__positions.copy()
        cl.grid = self.grid.copy()
        cl.__machine_count = self.__machine_count
        cl.__MODE_SIZE = self.__MODE_SIZE
        cl.distance_matrix = self.distance_matrix.copy()
        return cl

    def __mul__(self, other):
        return self.crossover(other)

    def crossover(self, other):
        new_grid, new_positions = self.__get_new_trait(other)
        new_grid, collisions, new_positions = self.__fill_if_possible(new_grid, new_positions)
        x_empty, y_empty = np.where(new_grid == -1)
        for i, v in enumerate(collisions):
            new_grid[x_empty[i], y_empty[i]] = v
            new_positions[v] = (x_empty[i], y_empty[i])
        crossed = FactoryIndividual.make_empty()
        crossed.__positions = new_positions
        crossed.grid = new_grid
        crossed.__machine_count = self.__machine_count
        crossed.__MODE_SIZE = self.__MODE_SIZE
        return crossed

    def __get_new_trait(self, other):
        genes = random.randint(1, len(other.__positions))
        grid = np.full(self.__MODE_SIZE, -1, dtype=np.int64)
        other_keys = random.sample(list(other.__positions.keys()), genes)
        pos = {}
        for key in other_keys:
            x, y = other.__positions[key]
            grid[x, y] = key
            pos[key] = (x, y)
        return grid, pos

    def __fill_if_possible(self, grid, positions):
        collisions = set()
        for key in self.__positions:
            if key not in positions:
                x, y = self.__positions[key]
                if grid[x, y] == -1:
                    grid[x, y] = key
                    positions[key] = (x, y)
                else:
                    collisions.add(key)
        return grid, collisions, positions

    def __invert__(self):
        return self.mutate()

    def mutate(self):
        to_swap = random.sample(list(self.__positions.keys()), 2)
        first = to_swap[0]
        second = to_swap[1]
        x1, y1 = self.__positions[first]
        x2, y2 = self.__positions[second]
        self.grid[x1, y1] = second
        self.grid[x2, y2] = first
        self.__positions[first] = (x2, y2)
        self.__positions[second] = (x1, y1)

    @property
    def machine_count(self):
        return self.__machine_count








