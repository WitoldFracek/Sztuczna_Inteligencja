import numpy as np
from binary_puzzle import select_where
from value_holder import ValueHolder
from data_readers import FutoshikiDataReader
import random
import os
# ograniczenie (x1, y1) (x2, y2) <-1, 0 1>


def pretty_futoshiki_print(solution, constraints):
    x, y = solution.shape
    for i in range(x):
        line = ''
        cons = ''
        for j in range(y):
            xs = select_where(constraints, lambda arg: arg[0] == (i, j))
            right = (i, j + 1)
            down = (i + 1, j)
            if not xs:
                line = line + f' {solution[i, j]} ' + '   '
                cons = cons + '   ' + '   '
            elif len(xs) == 1:
                _, arg, comp = xs[0]
                if arg == right:
                    if comp == 1:
                        line = line + f' {solution[i, j]} ' + ' > '
                    else:
                        line = line + f' {solution[i, j]} ' + ' < '
                    cons = cons + '   ' + '   '
                elif arg == down:
                    if comp == 1:
                        cons = cons + ' V ' + '   '
                    else:
                        cons = cons + ' ^ ' + '   '
                    line = line + f' {solution[i, j]} ' + '   '
            elif len(xs) == 2:
                _, arg1, comp1 = xs[0]
                _, arg2, comp2 = xs[1]
                if arg1 == right:
                    if comp1 == 1:
                        line = line + f' {solution[i, j]} ' + ' > '
                    else:
                        line = line + f' {solution[i, j]} ' + ' < '
                    if comp2 == 1:
                        cons = cons + ' V ' + '   '
                    else:
                        cons = cons + ' ^ ' + '   '
                else:
                    if comp2 == 1:
                        line = line + f' {solution[i, j]} ' + ' > '
                    else:
                        line = line + f' {solution[i, j]} ' + ' < '
                    if comp1 == 1:
                        cons = cons + ' V ' + '   '
                    else:
                        cons = cons + ' ^ ' + '   '
        print(line.replace('0', '□'))
        print(cons)


def take_row(array, index):
    return array[index, :]


def take_column(array, index):
    return array[:, index]


def generate_futoshiki_domain(size):
    return [tuple(range(1, size + 1)) for _ in range(size * size)]


class FutoshikiPuzzle:
    def __init__(self, size, values, domain, grid=None, constraints: set = None):
        self.__size = size
        if grid is None:
            self.__grid = np.full((size, size), 0, dtype=np.int8)
        elif grid.shape[0] != size or grid.shape[1] != size:
            raise Exception(f"Given grid shape {grid.shape} is inconsistent with specified size ({size}).")
        else:
            self.__grid = grid
        self.__values = values
        self.__domain = domain
        self.__constraints = set() if constraints is None else constraints

    def load_from_file(self, path, empty_field_marker='x', lt_marker='<', gt_marker='>', ignore_marker='-'):
        grid, constraints = FutoshikiDataReader.read_file(path, self.__size, empty_field_marker=empty_field_marker,
                                                          gt_marker=gt_marker, lt_marker=lt_marker,
                                                          ignore_marker=ignore_marker)
        self.__grid = grid
        self.__constraints = constraints
        self.__exclude_already_filled_fields()

    def __exclude_already_filled_fields(self):
        filled_fields = self.__find_filled_fields()
        new_values = []
        for value in self.__values:
            x, y = value
            if (x, y) not in filled_fields:
                new_values.append([x, y])
        self.__values = np.array(new_values, dtype=np.int8)

    def __find_filled_fields(self):
        ret = set()
        x, y = self.__grid.shape
        for i in range(x):
            for j in range(y):
                if self.__grid[i, j] != 0:
                    ret.add((i, j))
        return ret

    def check_constraints(self, value, domain_value):
        if not self.__is_line_correct(value, domain_value, 0):
            return False
        if not self.__is_line_correct(value, domain_value, 1):
            return False
        if not self.__are_inequalities_satisfied(value, domain_value):
            return False
        return True

    def __is_line_correct(self, value, domain_value, axes=0):
        x, y = value
        line = take_row(self.__grid, x) if axes == 0 else take_column(self.__grid, y)
        filled_values = select_where(line, lambda arg: arg != 0)
        unique = set()
        unique.update(filled_values)
        return domain_value not in unique

    def __are_inequalities_satisfied(self, value, domain_value):
        con_as_first = select_where(self.__constraints, lambda x: x[0] == tuple(value))
        con_as_second = select_where(self.__constraints, lambda x: x[1] == tuple(value))
        check_list = []
        check_list += self.__inequalities_first_pos(value, domain_value, con_as_first)
        check_list += self.__inequalities_second_pos(value, domain_value, con_as_second)
        return all(check_list)

    def __inequalities_first_pos(self, value, domain_value, constraints):
        check_list = []
        for _, snd, comp in constraints:
            x2, y2 = snd
            if self.__grid[x2, y2] == 0:
                check_list.append(True)
            elif comp == 1:
                check_list.append(domain_value > self.__grid[x2, y2])
            elif comp == -1:
                check_list.append(domain_value < self.__grid[x2, y2])
        return check_list

    def __inequalities_second_pos(self, value, domain_value, constraints):
        check_list = []
        for fst, _, comp in constraints:
            x1, y1 = fst
            if self.__grid[x1, y1] == 0:
                check_list.append(True)
            elif comp == 1:
                check_list.append(self.__grid[x1, y1] > domain_value)
            elif comp == -1:
                check_list.append(self.__grid[x1, y1] < domain_value)
        return check_list

    def solve(self):
        holders = self.__prepare_holders()
        holders[0].is_first = True
        return self.__iterate(holders)

    def __prepare_holders(self):
        holders = []
        for i, value in enumerate(self.__values):
            vh = ValueHolder(value, self.__domain[i])
            holders.append(vh)
        return holders

    def __iterate(self, holders):
        depth_index = 0
        solutions = []
        holder = holders[0]
        loops = 0
        while depth_index > -1:
            loops += 1
            if loops % 1_000_000 == 0:
                pretty_futoshiki_print(self.__grid, self.__constraints)
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

    def __rollback(self, value_holder: ValueHolder):
        value_holder.domain = {x for x in range(1, self.__size + 1)}
        x, y = value_holder.value
        self.__grid[x, y] = 0

    def __insert(self, value_holder: ValueHolder, domain_value):
        x, y = value_holder.value
        self.__grid[x, y] = domain_value

    @property
    def constraints(self):
        return self.__constraints

    @property
    def grid(self):
        return self.__grid




