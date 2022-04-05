from variable import Variable
from query import Qlist
import numpy as np


class Constraint:
    def __init__(self):
        pass

    def __call__(self, grid: np.ndarray, variable: Variable, value, **kwargs) -> bool:
        return False

    def constraint_count(self, grid: np.ndarray, variable: Variable, value, **kwargs) -> int:
        return 0


class BinaryNeighbourConstraint(Constraint):
    def __init__(self):
        Constraint.__init__(self)

    def __call__(self, grid: np.ndarray, variable: Variable, value, **kwargs):
        if not self.__check_neighbour_by_axes(grid, variable, value, 0):
            return False
        if not self.__check_neighbour_by_axes(grid, variable, value, 1):
            return False
        return True

    def constraint_count(self, grid: np.ndarray, variable: Variable, value, **kwargs):
        unmet = 0
        if not self.__check_neighbour_by_axes(grid, variable, value, 0):
            unmet += 1
        if not self.__check_neighbour_by_axes(grid, variable, value, 1):
            unmet += 1
        return unmet

    def __check_neighbour_by_axes(self, grid: np.ndarray, variable: Variable, value, axes) -> bool:
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

    def __call__(self, grid: np.ndarray, variable: Variable, value, **kwargs) -> bool:
        x, y = variable.position
        row = Qlist(*grid[x, :])
        column = Qlist(*grid[:, y])
        if not self.__is_ratio_correct(row, value):
            return False
        if not self.__is_ratio_correct(column, value):
            return False
        return True

    def constraint_count(self, grid: np.ndarray, variable: Variable, value, **kwargs) -> int:
        unmet = 0
        x, y = variable.position
        row = Qlist(*grid[x, :])
        column = Qlist(*grid[:, y])
        if not self.__is_ratio_correct(row, value):
            unmet += 1
        if not self.__is_ratio_correct(column, value):
            unmet += 1
        return unmet

    def __is_ratio_correct(self, line: Qlist, value) -> bool:
        ones = line.where(lambda x: x.value == 1).len()
        zeros = line.where(lambda x: x.value == 0).len()
        free_spots = len(line) - ones - zeros
        if value == 0:
            zeros += 1
        else:
            ones += 1
        return abs(ones - zeros) <= free_spots


class UniqueLinesConstraint(Constraint):
    def __init__(self):
        Constraint.__init__(self)

    def _no_dupicates(self, lines):
        for i, line in enumerate(lines):
            for j, li in enumerate(lines):
                if i != j:
                    if np.all(line == li):
                        return False
        return True


class UniqueRowsConstraint(UniqueLinesConstraint):
    def __init__(self):
        Constraint.__init__(self)

    def __call__(self, grid: np.ndarray, variable: Variable, value, **kwargs):
        rows = self.__grab_full_rows(grid)
        return self._no_dupicates(rows)

    def constraint_count(self, grid: np.ndarray, variable: Variable, value, **kwargs) -> int:
        unmet = 0
        rows = self.__grab_full_rows(grid)
        if not self._no_dupicates(rows):
            unmet += 1
        return unmet

    def __grab_full_rows(self, grid):
        full_rows = []
        for row in grid:
            if None not in row:
                full_rows.append(row)
        return full_rows


class UniqueColumnsConstraint(UniqueLinesConstraint):
    def __init__(self):
        Constraint.__init__(self)

    def __call__(self, grid: np.ndarray, variable: Variable, value, **kwargs):
        rows = self.__grab_full_columns(grid)
        return self._no_dupicates(rows)

    def constraint_count(self, grid: np.ndarray, variable: Variable, value, **kwargs) -> int:
        unmet = 0
        rows = self.__grab_full_columns(grid)
        if not self._no_dupicates(rows):
            unmet += 1
        return unmet

    def __grab_full_columns(self, grid):
        full_columns = []
        for col_idx in range(grid.shape[1]):
            if None not in grid[:, col_idx]:
                full_columns.append(grid[:, col_idx])
        return full_columns


class UniqueLineElementsConstraint(Constraint):
    def __init__(self, empty_field_value=None):
        Constraint.__init__(self)
        self.empty_field_value = empty_field_value


class UniqueRowElementsConstraint(UniqueLineElementsConstraint):
    def __init__(self, empty_field_value):
        UniqueLineElementsConstraint.__init__(self, empty_field_value)

    def __call__(self, grid: np.ndarray, variable: Variable, value, **kwargs):
        x, _ = variable.position
        row = Qlist(*grid[x, :])
        filled_values = row.where(lambda arg: arg.value != self.empty_field_value).select(lambda arg: arg.value)
        unique = {*filled_values}
        return value not in unique

    def constraint_count(self, grid: np.ndarray, variable: Variable, value, **kwargs) -> int:
        unmet = 0
        x, _ = variable.position
        row = Qlist(*grid[x, :])
        filled_values = row.where(lambda arg: arg.value != self.empty_field_value).select(lambda arg: arg.value)
        unique = {*filled_values}
        if value not in unique:
            unmet += 1
        return unmet


class UniqueColumnElementsConstraint(UniqueLineElementsConstraint):
    def __init__(self, empty_field_value):
        UniqueLineElementsConstraint.__init__(self, empty_field_value)

    def __call__(self, grid: np.ndarray, variable: Variable, value, **kwargs):
        _, y = variable.position
        column = Qlist(*grid[:, y])
        filled_values = column.where(lambda arg: arg.value != self.empty_field_value).select(lambda arg: arg.value)
        unique = {*filled_values}
        return value not in unique

    def constraint_count(self, grid: np.ndarray, variable: Variable, value, **kwargs) -> int:
        unmet = 0
        _, y = variable.position
        column = Qlist(*grid[:, y])
        filled_values = column.where(lambda arg: arg.value != self.empty_field_value).select(lambda arg: arg.value)
        unique = {*filled_values}
        if value not in unique:
            unmet += 1
        return unmet


class FutoshikiInequalitiesConstraint(Constraint):
    def __init__(self, inequalities: list[((int, int), (int, int), int)], empty_field_value=None):
        Constraint.__init__(self)
        self.inequalities = Qlist(*inequalities)
        self.empty_field_value = empty_field_value

    def __call__(self, grid: np.ndarray, variable: Variable, value, **kwargs):
        as_first_arg = self.inequalities.where(lambda x: x[0] == variable.position)
        as_second_arg = self.inequalities.where(lambda x: x[1] == variable.position)
        if not self.__inequalities_as_first_arg(grid, value, as_first_arg):
            return False
        if not self.__inequalities_as_second_arg(grid, value, as_second_arg):
            return False
        return True

    def constraint_count(self, grid: np.ndarray, variable: Variable, value, **kwargs) -> int:
        unmet = 0
        as_first_arg = self.inequalities.where(lambda x: x[0] == variable.position)
        as_second_arg = self.inequalities.where(lambda x: x[1] == variable.position)
        if not self.__inequalities_as_first_arg(grid, value, as_first_arg):
            unmet += 1
        if not self.__inequalities_as_second_arg(grid, value, as_second_arg):
            unmet += 1
        return unmet

    def __inequalities_as_first_arg(self, grid, value, inq):
        check_list = []
        for _, (x, y), comp in inq:
            if grid[x, y].value is None or grid[x, y].value == self.empty_field_value:
                check_list.append(True)
            elif comp == 1:
                check_list.append(value > grid[x, y].value)
            elif comp == -1:
                check_list.append(value < grid[x, y].value)
        return all(check_list)

    def __inequalities_as_second_arg(self, grid, value, inq):
        check_list = []
        for (x, y), _, comp in inq:
            if grid[x, y].value is None or grid[x, y].value == self.empty_field_value:
                check_list.append(True)
            elif comp == 1:
                check_list.append(grid[x, y].value > value)
            elif comp == -1:
                check_list.append(grid[x, y].value < value)
        return all(check_list)


