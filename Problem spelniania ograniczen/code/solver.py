import numpy as np
import math
from variable import Variable
import copy

class CSPSolver:
    def solve(self):
        pass


class GridCSPSolver(CSPSolver):
    def __init__(self, variables: list[Variable], constraints):
        self.__size = int(math.sqrt(len(variables)))
        self.__grid = np.array(variables).reshape((self.__size, self.__size))
        self.__original_variables = copy.deepcopy(variables)
        self.__variables = copy.deepcopy(variables)
        self.__constraints = constraints

    def solve(self, forward_check=False):
        depth_index = 0
        solutions = []
        variable: Variable = self.__variables[0]
        while depth_index > -1:
            if variable.all_checked:
                self.__rollback(variable)
                depth_index -= 1
            else:
                value = variable.available_values.pop()
                if all([constraint(self.__grid, variable, value) for constraint in self.__constraints]):
                    variable.value = value
                    depth_index += 1
                    if forward_check:
                        pass
                    if depth_index == len(self.__variables):
                        solutions.append(copy.deepcopy(self.__grid))
                        if variable.all_checked:
                            self.__rollback(variable)
                            depth_index -= 1
                        depth_index -= 1
            variable = self.__variables[depth_index]
        return solutions

    def __rollback(self, variable: Variable):
        variable.value = None
        variable.refill()

    def __convert_to_coordinates(self, index):
        return index // self.__size, index % self.__size

    @property
    def grid(self):
        return self.__grid

    def exclude_variables(self, mockup: np.ndarray):
        new_variables = []
        for elem in self.__original_variables:
            x, y = elem.position
            if mockup[x, y] is None:
                var = copy.deepcopy(elem)
                self.__grid[x, y] = var
                new_variables.append(var)
            else:
                self.__grid[x, y].value = mockup[x, y]
        self.__variables = new_variables



