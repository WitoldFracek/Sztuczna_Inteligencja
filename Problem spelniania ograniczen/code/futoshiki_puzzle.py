import numpy as np
# ograniczenie (x1, y1) (x2, y2) <-1, 0 1>

class FutoshikiPuzzle:
    def __init__(self, size, grid=None, domain=None, constraints: set = None):
        self.__size = size
        if grid is None:
            self.__grid = np.full((size, size), 0, dtype=np.int8)
        elif grid.shape[0] != size or grid.shape[1] != size:
            raise Exception(f"Given grid shape {grid.shape} is inconsistent with specified size ({size}).")
        self.__constraints = set() if constraints is None else constraints




