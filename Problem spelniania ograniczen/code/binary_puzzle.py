import numpy as np
import itertools
from data_readers import BinaryDataReader
from value_holder import ValueHolder


def generate_binary_values(size: int):
    return np.array([x for x in itertools.product(np.arange(0, size, step=1, dtype=np.int8),
                                                  np.arange(0, size, step=1, dtype=np.int8))])


def generate_binary_domain(size):
    return [(0, 1) for _ in range(size * size)]


def pretty_binary_print(solution):
    pass



def select_where(select_list, predicate) -> list:
    ret = []
    for elem in select_list:
        if predicate(elem):
            ret.append(elem)
    return ret


class BinaryPuzzle:
    def __init__(self, size, values, domain, grid=None):
        self.__size = size
        if grid is None:
            self.__grid = np.full((size, size), -1, dtype=np.int8)
        elif grid.shape[0] != size or grid.shape[1] != size:
            raise Exception(f"Given grid shape {grid.shape} is inconsistent with specified size ({size}).")
        else:
            self.__grid = grid
        self.__values = generate_binary_values(size)
        self.__domains = generate_binary_domain(size)

    def load_from_file(self, path, empty_field_marker='x'):
        grid = BinaryDataReader.read_file(path, self.__size, empty_field_marker=empty_field_marker)
        self.__grid = grid
        self.exclude_already_filled_fields()

    def convert(self, index: int) -> tuple[int, int]:
        return index // self.__size, index % self.__size

    def check_constraints(self, value, domain_value):
        if not self.check_neighbours(value, domain_value):
            return False
        if not self.check_ratio(value, domain_value):
            return False
        if not self.check_duplicate_lines():
            return False
        return True

    def check_neighbours(self, value, domain_value):
        if not self.__check_neighbour_by_axes(value, domain_value, 0):
            return False
        if not self.__check_neighbour_by_axes(value, domain_value, 1):
            return False
        return True

    def __check_neighbour_by_axes(self, value, domain_value, axes):
        x, y = value
        line = self.__grid[x, :] if axes == 0 else self.__grid[:, y]
        left = line[max(0, y - 2):y] if axes == 0 else line[max(0, x - 2):x]
        right = line[y + 1:min(len(line), y + 3)] if axes == 0 else line[x + 1:min(len(line), x + 3)]
        if not self.__is_slice_correct(left, domain_value):
            return False
        if not self.__is_slice_correct(right, domain_value):
            return False
        if not self.__are_attached_correct(left, right, domain_value):
            return False
        return True

    def __are_attached_correct(self, left, right, domain_value):
        if len(left) < 1 or len(right) < 1:
            return True
        if left[-1] == -1 or right[0] == -1:
            return True
        if left[-1] == domain_value and domain_value == right[0]:
            return False
        return True

    def __is_slice_correct(self, sl: list, domain_value):
        if len(sl) < 2:
            return True
        if -1 in sl:
            return True
        if sum(sl) + domain_value == 0 or sum(sl) + domain_value == 3:
            return False
        return True

    def check_ratio(self, value, domain_value):
        x, y = value
        row = self.__grid[x, :]
        column = self.__grid[:, y]
        if not self.__is_ratio_correct(row, domain_value):
            return False
        if not self.__is_ratio_correct(column, domain_value):
            return False
        return True

    def __is_ratio_correct(self, line, domain_value):
        ones = len(select_where(line, lambda x: x == 1))
        zeros = len(select_where(line, lambda x: x == 0))
        free_spots = len(line) - ones - zeros
        ones += 1 if domain_value == 1 else 0
        zeros += 1 if domain_value == 0 else 0
        return abs(ones - zeros) <= free_spots

    def check_duplicate_lines(self):
        rows = self.__grab_full_rows()
        columns = self.__grab_full_columns()
        if not self.__no_duplicates(rows):
            return False
        if not self.__no_duplicates(columns):
            return False
        return True

    def __grab_full_rows(self):
        full_rows = []
        for row in self.__grid:
            if -1 not in row:
                full_rows.append(row)
        return full_rows

    def __grab_full_columns(self):
        full_columns = []
        for col_idx in range(self.__grid.shape[1]):
            if -1 not in self.__grid[:, col_idx]:
                full_columns.append(self.__grid[:, col_idx])
        return full_columns

    def __no_duplicates(self, lines):
        for i, line in enumerate(lines):
            for j, li in enumerate(lines):
                if i != j:
                    if np.all(line == li):
                        return False
        return True

    def exclude_already_filled_fields(self):
        filled_fields = self.find_filled_fields()
        new_values = []
        for value in self.__values:
            x, y = value
            if (x, y) not in filled_fields:
                new_values.append([x, y])
        self.__values = np.array(new_values, dtype=np.int8)

    def find_filled_fields(self):
        ret = set()
        x, y = self.__grid.shape
        for i in range(x):
            for j in range(y):
                if self.__grid[i, j] != -1:
                    ret.add((i, j))
        return ret

    @property
    def grid(self):
        return self.__grid

    @property
    def values(self):
        return self.__values

    def test(self):
        print(self.check_constraints((0, 1), 0))

    def solve(self):
        depth_index = 0
        holders = self.__prepare_holders()
        holders[0].is_first = True
        solutions = []
        return self.__iterate(holders)

    def __prepare_holders(self):
        holders = []
        for i, value in enumerate(self.__values):
            vh = ValueHolder(value, self.__domains[i])
            holders.append(vh)
        return holders

    def __iterate(self, holders):
        depth_index = 0
        solutions = []
        holder = holders[0]
        while depth_index > -1:
            if len(holder.domain) == 0:
                self.__rollback(holder)
                depth_index -= 1
            else:
                domain_value = holder.domain.pop()
                if self.check_constraints(holder.value, domain_value):
                    self.__insert(holder, domain_value)
                    depth_index += 1
                    if depth_index == len(holders):
                        solutions.append(self.__grid.copy())
                        if len(holder.domain) == 0:
                            self.__rollback(holder)
                            depth_index -= 1
                        depth_index -= 1
            holder = holders[depth_index]
        return solutions

    def __insert(self, value_holder: ValueHolder, domain_value):
        x, y = value_holder.value
        self.__grid[x, y] = domain_value

    def __rollback(self, value_holder: ValueHolder):
        value_holder.domain = {0, 1}
        x, y = value_holder.value
        self.__grid[x, y] = -1

    def check_if(self, value, domain_value, print_info=False):
        x, y = value
        temp = self.__grid[x, y]
        self.__grid[x, y] = -1
        correct_ratio = self.check_ratio(value, domain_value)
        correct_neighbour = self.check_neighbours(value, domain_value)
        check_unique = self.check_duplicate_lines()
        self.__grid[x, y] = temp
        if print_info:
            print(f'Correct ratio 1 to 0: {correct_ratio}')
            print(f'No triple values: {correct_neighbour}')
            print(f'All columns and rows unique: {check_unique}')
        return correct_ratio, correct_neighbour, check_unique







