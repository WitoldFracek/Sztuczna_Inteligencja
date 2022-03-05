import numpy as np
import random

EASY = (3, 3)
FLAT = (1, 12)
HARD = (4, 5)

MODE_SIZE = EASY


def generate_random_positions(count, xszie, ysize):
    positions = []
    for i in range(xszie):
        for j in range(ysize):
            positions.append((i, j))
    random.shuffle(positions)
    return positions[:count]


class FactoryIndividual:
    def __init__(self, machine_count):
        self.grid = np.full(MODE_SIZE, -1, dtype=np.int64)
        self.positions = {}
        self.machine_count = machine_count
        self.distance_matrix = np.zeros((self.machine_count, self.machine_count), dtype=np.int64)

    def random_start(self):
        x, y = self.grid.shape
        random_positions = generate_random_positions(self.machine_count, x, y)
        for i, pos in enumerate(random_positions):
            self.positions[i] = pos
            xpos, ypos = pos
            self.grid[xpos, ypos] = i
        self.__count_distances()
        print(self.grid)
        print(self.distance_matrix)

    def __count_distances(self):
        for key_x in self.positions:
            for key_y in self.positions:
                x1, y1 = self.positions[key_x]
                x2, y2 = self.positions[key_y]
                distance = self.__count_distance(x1, y1, x2, y2)
                self.distance_matrix[key_x, key_y] = distance

    def __count_distance(self, x1, y1, x2, y2):
        return abs(x1-x2) + abs(y1-y2)







