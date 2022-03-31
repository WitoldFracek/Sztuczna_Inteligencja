from data_readers import BinaryDataReader, FutoshikiDataReader
from binary_puzzle import BinaryPuzzle, generate_binary_domain, generate_grid_values, pretty_binary_print
from futoshiki_puzzle import FutoshikiPuzzle, generate_futoshiki_domain, pretty_futoshiki_print
import numpy as np

# Binary
BIN_2x2 = '../data/binary_2x2'
BIN_4x4 = '../data/binary_4x4'
BIN_6x6 = '../data/binary_6x6'
BIN_8x8 = '../data/binary_8x8'
BIN_10x10 = '../data/binary_10x10'

# Futoshiki
FUT_4x4 = '../data/futoshiki_4x4'
FUT_5x5 = '../data/futoshiki_5x5'
FUT_6x6 = '../data/futoshiki_6x6'

BIN_SIZE = 10
BIN_MODE = BIN_10x10

FUT_SIZE = 6
FUT_MODE = FUT_6x6


def binary():
    bp = BinaryPuzzle(BIN_SIZE, generate_grid_values(BIN_SIZE), generate_binary_domain(BIN_SIZE))
    bp.load_from_file(BIN_MODE)
    print('Start')
    pretty_binary_print(bp.grid)
    print()
    solutions = bp.solve()

    print("Solutions:")
    for solution in solutions:
        pretty_binary_print(solution)
        print()


def futoshiki():
    domain = generate_futoshiki_domain(FUT_SIZE)
    values = generate_grid_values(FUT_SIZE)
    fp = FutoshikiPuzzle(FUT_SIZE, values, domain)
    fp.load_from_file(FUT_MODE)
    print("Start")
    pretty_futoshiki_print(fp.grid, fp.constraints)
    print()
    solutions = fp.solve()
    print("Solutions:")
    print(f'Number of solutions: {len(solutions)}')
    # for solution in solutions:
    #     pretty_futoshiki_print(solution, fp.constraints)


def main():
    futoshiki()
    # binary()


def check_whole_grid(puzzle: BinaryPuzzle):
    ret = []
    x, y = puzzle.grid.shape
    for i in range(x):
        for j in range(y):
            store = puzzle.grid[i, j]
            puzzle.grid[i, j] = -1
            # print(store)
            tpl = (puzzle.check_ratio((i, j), store),
                   puzzle.check_duplicate_lines(),
                   puzzle.check_neighbours((i, j), store),
                   (i, j))
            puzzle.grid[i, j] = store
            ret.append(tpl)
            # if i == 0 and j == 1:
            #     return ret
    return ret


if __name__ == '__main__':
    main()



