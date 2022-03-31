from variable import Variable
from query import Qlist
import numpy as np

class Constraint:
    def __init__(self):
        pass

    def __call__(self, grid, variable: Variable, value) -> bool:
        return False


# Binary Puzzle
class BinaryNeighbourConstraint(Constraint):
    def __init__(self):
        Constraint.__init__(self)

    def __call__(self, grid, variable: Variable, value):
        if not self.__check_neighbour_by_axes(grid, variable, value, 0):
            return False
        if not self.__check_neighbour_by_axes(grid, variable, value, 1):
            return False
        return True

    def __check_neighbour_by_axes(self, grid, variable: Variable, value, axes) -> bool:
        x, y = variable.position
        line = grid[x, :] if axes == 0 else grid[:, y]
        left = line[max(0, y - 2):y] if axes == 0 else line[max(0, x - 2):x]
        right = line[y + 1:min(len(line), y + 3)] if axes == 0 else line[x + 1:min(len(line), x + 3)]
        if not self.__is_neighbour_slice_correct(left, value):
            return False
        if not self.__is_neighbour_slice_correct(right, value):
            return False
        if not self.__are_adjacent_correct(left, right, value):
            return False
        return True

    def __is_neighbour_slice_correct(self, neighbour_slice, value) -> bool:
        if len(neighbour_slice) < 2:
            return True
        if any([v.value is None for v in neighbour_slice]):
            return True
        values = [v.value for v in neighbour_slice]
        if sum(values) + value == 0 or sum(values) + value == 3:
            return False
        return True

    def __are_adjacent_correct(self, left, right, value) -> bool:
        if len(left) < 1 or len(right) < 1:
            return True
        if left[-1] is None or right[0] is None:
            return True
        if left[-1].value == value and right[0].value == value:
            return False
        return True


class BinaryRatioConstraint(Constraint):
    def __init__(self):
        Constraint.__init__(self)

    def __call__(self, grid, variable: Variable, value) -> bool:
        x, y = variable.position
        row = Qlist(*grid[x, :])
        column = Qlist(*grid[:, y])
        if not self.__is_ratio_correct(row, value):
            return False
        if not self.__is_ratio_correct(column, value):
            return False
        return True

    def __is_ratio_correct(self, line: Qlist, value) -> bool:
        ones = line.where(lambda x: x.value == 1).len()
        zeros = line.where(lambda x: x.value == 0).len()
        free_spots = len(line) - ones - zeros
        if value == 0:
            zeros += 1
        else:
            ones += 1
        return abs(ones - zeros) <= free_spots


class UniqueRowsConstraint(Constraint):
    def __init__(self):
        Constraint.__init__(self)

    def __call__(self, grid, variable: Variable, value):
        rows = self.__grab_full_rows(grid)
        columns = self.__grab_full_columns(grid)
        if not self.__no_dupicates(rows):
            return False
        if not self.__no_dupicates(columns):
            return False
        return True

    def __grab_full_rows(self, grid):
        full_rows = []
        for row in grid:
            if None not in row:
                full_rows.append(row)
        return full_rows

    def __grab_full_columns(self, grid):
        full_columns = []
        for col_idx in range(grid.shape[1]):
            if None not in grid[:, col_idx]:
                full_columns.append(grid[:, col_idx])
        return full_columns

    def __no_dupicates(self, lines):
        for i, line in enumerate(lines):
            for j, li in enumerate(lines):
                if i != j:
                    if np.all(line == li):
                        return False
        return True

