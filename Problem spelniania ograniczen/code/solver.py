import numpy as np
import math
from variable import Variable
import copy
from constraints import Constraint
from printers import pretty_futoshiki_print, pretty_binary_print
from query import Qlist


class CSPSolver:
    def solve(self):
        pass


class GridCSPSolver(CSPSolver):
    def __init__(self, variables: list[Variable], constraints: list[Constraint]):
        self.__size = int(math.sqrt(len(variables)))
        self.__original_variables = copy.deepcopy(variables)
        self.__variables = copy.deepcopy(variables)
        self.__grid = np.array(self.__variables).reshape((self.__size, self.__size))
        self.__constraints = constraints

    def solve(self, forward_check=False):
        depth_index = 0
        forward_is_ok = True
        solutions = []
        variable: Variable = self.__variables[0]
        while depth_index > -1:
            if variable.all_checked:
                self.__rollback(variable)
                depth_index -= 1
            elif forward_check and self.__check_forward_domains(depth_index):
                self.__recover_forward_domains(depth_index)
                variable.available_values.pop()
            else:
                value = variable.available_values.pop()
                if all([constraint(self.__grid, variable, value) for constraint in self.__constraints]):
                    variable.value = value
                    # pretty_binary_print(self.__grid)
                    # for variable in self.__variables[depth_index + 1:]:
                    #     print(variable.position, variable.available_values)
                    # print()
                    # if forward_check:
                    #     if self.__forward_check(depth_index):
                    #         depth_index += 1
                    #     else:
                    #         variable.value = None
                    # else:
                    #     depth_index += 1
                    depth_index += 1
                    if depth_index == len(self.__variables):
                        solutions.append(copy.deepcopy(self.__grid))
                        # xs = Qlist(*self.__constraints).where(lambda cons: hasattr(cons, "inequalities"))[0].inequalities
                        # pretty_futoshiki_print(self.__grid, xs)
                        # print()
                        if variable.all_checked and forward_is_ok:
                            forward_is_ok = True
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

    def __forward_check(self, eliminator_index: int):
        eliminator_id = self.__variables[eliminator_index].id
        for variable in self.__variables[eliminator_index + 1:]:
            variable.eliminate(self.__grid, self.__constraints, eliminator_id)
        if any([variable.all_checked for variable in self.__variables[eliminator_index + 1:]]):
            for variable in self.__variables[eliminator_index + 1:]:
                variable.recover_from_history(eliminator_id)
            return False
        return True

    def index_to_coordinates(self, index: int):
        return index // self.__size, index % self.__size



