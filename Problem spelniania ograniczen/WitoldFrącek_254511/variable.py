import copy
# from constraints import Constraint
import numpy as np


class Variable:
    def __init__(self, coordinates: (int, int), domain, identifier=None, empty_value_repr=None):
        self.__x, self.__y = coordinates
        self.__domain = {*domain}
        self.__available_values = {*domain}
        self.__identifier = identifier
        self.value = None
        self.modification_history: dict = {}
        self.self_eliminated = set()
        self.empty_value_repr = empty_value_repr

    def refill(self):
        self.__available_values = self.self_eliminated.copy()
        self.self_eliminated.clear()

    @property
    def all_checked(self) -> bool:
        return len(self.__available_values) == 0

    @property
    def position(self) -> (int, int):
        return self.__x, self.__y

    @property
    def first(self):
        value = self.__available_values.pop()
        self.self_eliminated.add(value)
        return value

    @property
    def domain(self) -> set:
        return self.__domain

    @property
    def available_values(self) -> set:
        return self.__available_values

    @property
    def id(self):
        return self.__identifier

    def set_fixed_points(self, fixed_points_values):
        pass

    def __repr__(self):
        return f'Var_{self.id}: {self.empty_value_repr if self.value is None else self.value}'

    def __eq__(self, other) -> bool:
        if self.__identifier == other.id:
            return True
        elif self.position == other.position:
            return True
        return False

    def __deepcopy__(self, memo):
        cls = self.__class__
        ret = cls.__new__(cls)
        memo[id(self)] = ret
        for k, v in self.__dict__.items():
            setattr(ret, k, copy.deepcopy(v))
        return ret

    def pre_eliminate(self, grid: np.ndarray, constraints: list[...]):
        eliminated = []
        for value in self.__available_values:
            if not self.__check_if_fits(grid, constraints, value):
                eliminated.append(value)
        for value in eliminated:
            self.__available_values.remove(value)

    def eliminate(self, grid: np.ndarray, constraints: list[...], eliminator_id: int):
        eliminated = []
        for value in self.__available_values:
            if not self.__check_if_fits(grid, constraints, value):
                eliminated.append(value)
        for value in eliminated:
            self.__available_values.remove(value)
        if len(eliminated) != 0:
            if eliminator_id in self.modification_history:
                self.modification_history[eliminator_id].update(eliminated)
            else:
                self.modification_history[eliminator_id] = {*eliminated}

    def recover_from_history(self, eliminator_id: int):
        if eliminator_id not in self.modification_history:
            return
        rec = self.modification_history[eliminator_id]
        self.__available_values.update(rec)
        del self.modification_history[eliminator_id]

    def __check_if_fits(self, grid: np.ndarray, constraints: list[...], value) -> bool:
        return all([constraint(grid, self, value) for constraint in constraints])


if __name__ == '__main__':
    v1 = Variable((0, 0), [1, 2, 3])
    v2 = copy.copy(v1)
    print(v2.position)
    print(v2.position)




