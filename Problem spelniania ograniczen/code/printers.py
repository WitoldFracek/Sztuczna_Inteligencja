from query import Qlist
import numpy as np


def pretty_binary_print(solution, mockup=None, empty_value_marker=None, colorize_initial_values=False):
    for i, row in enumerate(solution):
        line = ''
        for j, variable in enumerate(row):
            if mockup is None:
                line = line + f'\x1b[0;30;47m {" " if variable.value is None else variable.value} \x1b[0m'
            elif mockup[i, j] is None or mockup[i, j] == empty_value_marker:
                line = line + f'\x1b[0;30;47m {" " if variable.value is None else variable.value} \x1b[0m'
            else:
                line = line + f'\x1b[6;30;42m {" " if variable.value is None else variable.value} \x1b[0m'
        print(line)


def pretty_futoshiki_print(solution: np.ndarray, inequalities, mockup=None, empty_value_marker=None, colorize_initial_values=False):
    x, y = solution.shape
    true_size = x + x - 1
    ret = [['\x1b[0;30;47m   \x1b[0m' for _ in range(true_size)] for _ in range(true_size)]
    for i, row in enumerate(solution):
        for j, variable in enumerate(row):
            if mockup is None:
                ret[i * 2][j * 2] = f'\x1b[0;30;47m {" " if variable.value is None else variable.value} \x1b[0m'
            elif mockup[i, j] is None or mockup[i, j] == empty_value_marker:
                ret[i * 2][j * 2] = f'\x1b[0;30;47m {" " if variable.value is None else variable.value} \x1b[0m'
            else:
                ret[i * 2][j * 2] = f'\x1b[6;30;42m {" " if variable.value is None else variable.value} \x1b[0m'
    for (x1, y1), (x2, y2), comp in inequalities:
        idx1 = x1 + x2
        idx2 = y1 + y2
        if x1 == x2:
            if comp == 1:
                ret[idx1][idx2] = '\x1b[0;30;47m > \x1b[0m'
            elif comp == -1:
                ret[idx1][idx2] = '\x1b[0;30;47m < \x1b[0m'
        elif y1 == y2:
            if comp == 1:
                ret[idx1][idx2] = '\x1b[0;30;47m v \x1b[0m'
            elif comp == -1:
                ret[idx1][idx2] = '\x1b[0;30;47m ^ \x1b[0m'
    for row in ret:
        print("".join(row))

