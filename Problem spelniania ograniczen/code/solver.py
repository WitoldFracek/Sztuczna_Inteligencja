import numpy as np
import math
from variable import Variable
import copy
from constraints import Constraint
from printers import pretty_futoshiki_print, pretty_binary_print
from query import Qlist
from data_collector import DataCollector


class CSPSolver:
    # Heuristics:
    IN_ORDER = 'in order'
    MOST_VALUES_FIRST = 'most values first'
    LEAST_VALUES_FIRST = 'least values first'
    MOST_CONSTRAINTS_FIRST = 'most constraints first'
    LEAST_CONSTRAINTS_FIRST = 'least constraints first'

    def solve(self, till_first_solution=False):
        pass


class GridCSPSolver(CSPSolver):
    def __init__(self, variables: list[Variable], constraints: list[Constraint],
                 heuristic='in order', data_collector: DataCollector = None):
        self.__size = int(math.sqrt(len(variables)))
        self.__original_variables = copy.deepcopy(variables)
        self.__variables = copy.deepcopy(variables)
        self.__grid = np.array(self.__variables).reshape((self.__size, self.__size))
        self.__constraints = constraints
        self.__heuristic = heuristic
        self.__history = []
        self.__data_collector = data_collector

    def solve(self, forward_check=False, till_first_solution=False):
        solutions = []
        variable: Variable = self.__take_next()
        if forward_check:
            self.__pre_eliminate()
        while variable is not None:
            # pretty_binary_print(self.__grid)
            # print()
            if variable.all_checked:
                self.__rollback(variable)
                variable = self.__take_previous()
                if forward_check:
                    if variable is not None:
                        self.__recover_forward_domains(variable.id)
            else:
                value = variable.first
                if self.__data_collector is not None:
                    self.__data_collector.nodes += 1
                if all([constraint(self.__grid, variable, value) for constraint in self.__constraints]):
                    #tutaj dodac liczenie wezlow
                    variable.value = value
                    if forward_check:
                        self.__forward_elimination(variable.id)  # profiler
                    if forward_check and self.__empty_forward_domains():
                        self.__recover_forward_domains(variable.id)
                    else:
                        variable = self.__take_next(variable)
                    if variable is None:
                        solutions.append(copy.deepcopy(self.__grid))
                        if self.__data_collector is not None:
                            if not self.__data_collector.first_found:
                                self.__data_collector.first_found = True
                                self.__data_collector.steps_till_first = self.__data_collector.nodes
                        if till_first_solution:
                            break
                        variable = self.__take_previous()
                        if variable.all_checked:
                            self.__rollback(variable)
                            if forward_check:
                                self.__recover_forward_domains(variable.id)
                            variable = self.__take_previous()
        return solutions

    def __rollback(self, variable: Variable):
        variable.value = None
        variable.refill()

    def __convert_to_coordinates(self, index):
        return index // self.__size, index % self.__size

    @property
    def grid(self):
        return self.__grid

    @property
    def data_collector(self):
        return self.__data_collector

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

    def __pre_eliminate(self):
        for variable in self.__variables:
            variable.pre_eliminate(self.__grid, self.__constraints)

    def __forward_elimination(self, eliminator_id: int):
        for variable in self.__not_set_variables():
            variable.eliminate(self.__grid, self.__constraints, eliminator_id)

    def __empty_forward_domains(self) -> bool:
        return any([variable.all_checked for variable in self.__not_set_variables()])

    def __recover_forward_domains(self, eliminator_id: int):
        for variable in self.__not_set_variables():
            variable.recover_from_history(eliminator_id)

    def __take_next(self, current=None) -> Variable:
        if current is not None:
            self.__history.append(current)
        if self.__heuristic == CSPSolver.IN_ORDER:
            return self.__take_in_order()
        if self.__heuristic == CSPSolver.MOST_VALUES_FIRST:
            return self.__least_values_first(reverse=True)
        if self.__heuristic == CSPSolver.LEAST_VALUES_FIRST:
            return self.__least_values_first(reverse=False)
        if self.__heuristic == CSPSolver.MOST_CONSTRAINTS_FIRST:
            return self.__most_constraints_first(reverse=False)
        if self.__heuristic == CSPSolver.LEAST_CONSTRAINTS_FIRST:
            return self.__most_constraints_first(reverse=True)
        raise Exception(f'No heuristic name \'{self.__heuristic}\' found.')

    def __take_previous(self):
        # if self.__data_collector is not None:
        #     self.__data_collector.step_up += 1
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

    def __least_values_first(self, reverse=False):
        not_set = self.__not_set_variables()
        if not not_set:
            return None
        pairs = Qlist(*not_set) \
            .select(lambda variable: (variable, len(variable.available_values))) \
            .order_by(lambda pair: pair[1])
        if reverse:
            pairs = pairs.reverse()
        return pairs[0][0]

    def __most_constraints_first(self, reverse=False):
        not_set = self.__not_set_variables()
        if not not_set:
            return None
        constraints_number = Qlist()
        for variable in not_set:
            partial_sum = 0
            for value in variable.available_values:
                partial_sum += sum([constraint.constraint_count(self.__grid, variable, value) for constraint in self.__constraints])
            constraints_number.append((variable, partial_sum))
        constraints_number.order_by(lambda pair: pair[1])
        if reverse:
            constraints_number = constraints_number.reverse()
        return constraints_number[0][0]

    def print_all_domains(self):
        ret = []
        for variable in self.__variables:
            ret.append(str(variable.id) + str(variable.available_values) + str(variable.modification_history))
        print(ret)

