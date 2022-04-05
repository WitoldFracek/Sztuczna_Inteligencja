import numpy as np
import math
from variable import Variable
import copy
from constraints import Constraint
from printers import pretty_futoshiki_print, pretty_binary_print
from query import Qlist


class CSPSolver:

    # Heuristics:
    IN_ORDER = 'in order'

    def solve(self):
        pass


class GridCSPSolver(CSPSolver):
    def __init__(self, variables: list[Variable], constraints: list[Constraint], heuristic='in order'):
        self.__size = int(math.sqrt(len(variables)))
        self.__original_variables = copy.deepcopy(variables)
        self.__variables = copy.deepcopy(variables)
        self.__grid = np.array(self.__variables).reshape((self.__size, self.__size))
        self.__constraints = constraints
        self.__heuristic = heuristic
        self.__history = []

    def solve(self, forward_check=False):
        depth_index = 0
        solutions = []
        variable: Variable = self.__take_next()
        while variable is not None:  # depth_index > -1:
            if variable.all_checked:
                self.__rollback(variable)
                variable = self.__take_previous()
                # depth_index -= 1
            elif forward_check and self.__check_forward_domains(variable.id):
                self.__recover_forward_domains(variable.id)
                variable.available_values.pop()
            else:
                value = variable.available_values.pop()
                if all([constraint(self.__grid, variable, value) for constraint in self.__constraints]):
                    variable.value = value
                    # depth_index += 1
                    variable = self.__take_next(variable)
                    if variable is None:  # depth_index == len(self.__variables):
                        solutions.append(copy.deepcopy(self.__grid))
                        variable = self.__take_previous()
                        if variable.all_checked:
                            self.__rollback(variable)
                            variable = self.__take_previous()
                            # depth_index -= 1
                        # depth_index -= 1
            # variable = self.__variables[depth_index]
        return solutions

    def __rollback(self, variable: Variable):
        variable.value = None
        variable.refill()

    def __convert_to_coordinates(self, index):
        return index // self.__size, index % self.__size

    @property
    def grid(self):
        return self.__grid

    def exclude_variables(self, mockup: np.ndarray, empty_value_marker=None):
        new_variables = []
        for elem in self.__original_variables:
            x, y = elem.position
            if mockup[x, y] is None or mockup[x, y] == empty_value_marker:
                var = copy.deepcopy(elem)
                self.__grid[x, y] = var
                new_variables.append(var)
            else:
                self.__grid[x, y].value = mockup[x, y]
        self.__variables = new_variables

    def __forward_elimination(self, eliminator_index: int):
        eliminator_id = self.__variables[eliminator_index].id
        for variable in self.__variables[eliminator_index + 1:]:
            variable.eliminate(self.__grid, self.__constraints, eliminator_id)

    def __check_forward_domains(self, eliminator_index: int) -> bool:
        return any([variable.all_checked for variable in self.__variables[eliminator_index + 1:]])

    def __recover_forward_domains(self, eliminator_index: int):
        eliminator_id = self.__variables[eliminator_index].id
        for variable in self.__variables[eliminator_index + 1:]:
            variable.recover_from_history(eliminator_id)

    def __take_next(self, current=None) -> Variable:
        if current is not None:
            self.__history.append(current)
        if self.__heuristic == CSPSolver.IN_ORDER:
            return self.__take_in_order()
        ...

    def __take_previous(self):
        if self.__history:
            prev = self.__history[-1]
            self.__history = self.__history[:-1]
            return prev
        return None

    def __take_in_order(self):
        not_set = self.__not_set_variables()
        if not_set:
            return not_set[0]
        return None

    def __not_set_variables(self) -> list[Variable]:
        return Qlist(*self.__variables).where(lambda x: x.value is None).to_list()



