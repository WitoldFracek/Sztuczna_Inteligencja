import numpy as np
import itertools
from data_readers import BinaryDataReader
from value_holder import ValueHolder

def generate_binary_values(size: int):
    return np.array([x for x in itertools.product(np.arange(0, size, step=1, dtype=np.int8),
                                                  np.arange(0, size, step=1, dtype=np.int8))])


def generate_binary_domain(size):
    return [(0, 1) for _ in range(size)]


def select_where(select_list, predicate) -> list:
    ret = []
    for elem in select_list:
        if predicate(elem):
            ret.append(elem)
    return ret


class BinaryPuzzle:
    def __init__(self, size, grid=None):
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

    def start(self):
        pass

    def check_constraints(self, value, domain_value):
        if not self.check_neighbours(value, domain_value, 0):
            return False
        if not self.check_neighbours(value, domain_value, 1):
            return False
        if not self.check_ratio(value, domain_value):
            return False
        if not self.check_duplicate_lines():
            return False

    def check_neighbours(self, value, domain_value):
        if not self.__check_neighbour_in_row(value, domain_value):
            return False
        if not self.__check_neighbour_in_column(value, domain_value):
            return False
        return True

    def __check_neighbour_in_row(self, value, domain_value):
        x, y = value
        row = self.__grid[x, :]
        left = row[max(0, y - 2):y]
        right = row[y + 1:min(len(row), y + 3)]
        if not self.__is_slice_correct(left, domain_value):
            return False
        if not self.__is_slice_correct(right, domain_value):
            return False
        return True

    def __check_neighbour_in_column(self, value, domain_value):
        x, y = value
        column = self.__grid[:, y]
        left = column[max(0, x - 2):x]
        right = column[x + 1:min(len(column), x + 3)]
        if not self.__is_slice_correct(left, domain_value):
            return False
        if not self.__is_slice_correct(right, domain_value):
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


def no_dup(lines):
    for i, line in enumerate(lines):
        for j, li in enumerate(lines):
            if i != j:
                if np.all(line == li):
                    return False
    return True


if __name__ == '__main__':
    a = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 2, 3]])

    xs = [a[0, :], a[1, :], a[2, :]]
    print(no_dup(xs))

    # b = a.copy()
    # b[2, 2] = -1
    # print(np.all(b == a))

