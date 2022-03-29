import numpy as np
import itertools


def generate_binary_values(size):
    return np.array([x for x in itertools.product(np.arange(0, size, step=1, dtype=np.int8),
                                                  np.arange(0, size, step=1, dtype=np.int8))])


def generate_binary_domain(size):
    return [[0, 1] for _ in range(size)]


class BinaryPuzzle:
    def __init__(self, size):
        self.__size = size
        self.__grid = np.full((size, size), -1, dtype=np.int8)

    def check_neighbours(self, value, domain_value, axes):
        x, y = value
        row = self.__grid[x, :] if axes == 0 else self.__grid[:, y]
        left = row[max(0, x - 2):x] if axes == 0 else row[max(0, y - 2):y]
        right = row[x:min(len(row), x + 2)] if axes == 0 else row[y:min(len(row), y + 2)]
        if not self.__is_slice_correct(left, domain_value):
            return False
        if not self.__is_slice_correct(right, domain_value):
            return False

    def __is_slice_correct(self, sl: list, domain_value):
        if -1 in sl:
            return True
        if sum(sl) + domain_value == 0 or sum(sl) + domain_value == 3:
            return False
        return True

    def check_lines(self):
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
            if not -1 in row:
                full_rows.append(row)
        return full_rows

    def __grab_full_columns(self):
        full_columns = []
        for col_idx in range(self.__grid.shape[1]):
            if not -1 in a[:, col_idx]:
                full_columns.append(a[:, col_idx])
        return full_columns

    def __no_duplicates(self, lines):
        for i, line in enumerate(lines):
            for j, li in enumerate(lines):
                if i != j:
                    if np.all(line == li):
                        return False
        return True


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

