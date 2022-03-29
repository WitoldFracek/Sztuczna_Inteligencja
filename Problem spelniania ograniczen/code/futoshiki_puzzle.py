import numpy as np
from binary_puzzle import generate_binary_values, select_where
# ograniczenie (x1, y1) (x2, y2) <-1, 0 1>


def take_row(array, index):
    return array[index, :]


def take_column(array, index):
    return array[:, index]


class FutoshikiPuzzle:
    def __init__(self, size, values, domain, grid=None, constraints: set = None):
        self.__size = size
        if grid is None:
            self.__grid = np.full((size, size), 0, dtype=np.int8)
        elif grid.shape[0] != size or grid.shape[1] != size:
            raise Exception(f"Given grid shape {grid.shape} is inconsistent with specified size ({size}).")
        self.__values = values
        self.__domain = domain
        self.__constraints = set() if constraints is None else constraints




