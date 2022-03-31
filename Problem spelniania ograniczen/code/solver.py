import numpy as np
import math
from variable import Variable


class CSPSolver:
    pass


class GridCSPSolver(CSPSolver):
    def __init__(self, variables, constraints):
        self.__size = int(math.sqrt(len(variables)))
        self.__grid = np.array(variables).reshape((self.__size, self.__size))
        self.__variables = variables
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
                domain_value = variable.available_values.pop()
                if all([constraint(self.__grid, variable, domain_value) for constraint in self.__constraints]):
                    variable.value = domain_value
                    depth_index += 1
                    if forward_check:
                        pass
                    if depth_index == len(self.__variables):
                        solutions.append(self.__grid.copy())
                        if variable.all_checked:
                            self.__rollback(variable)
                            depth_index -= 1
                        depth_index -= 1
            variable = self.__variables[depth_index]

    def __rollback(self, variable: Variable):
        variable.value = None
        variable.refill()

    def __convert_to_coordinates(self, index):
        return index // self.__size, index % self.__size

