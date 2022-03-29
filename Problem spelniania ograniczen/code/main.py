from data_readers import BinaryDataReader, FutoshikiDataReader
from binary_puzzle import BinaryPuzzle, generate_binary_domain, generate_binary_values
import numpy as np

# Binary
BIN_2x2 = '../data/binary_2x2'
BIN_4x4 = '../data/binary_4x4'
BIN_6x6 = '../data/binary_6x6'
BIN_8x8 = '../data/binary_8x8'
BIN_10x10 = '../data/binary_10x10'

# Futoshiki
FUT_4x4 = '../data/futoshiki_4x4'

SIZE = 10


def binary():
    bp = BinaryPuzzle(SIZE, generate_binary_values(SIZE), generate_binary_domain(SIZE))
    bp.load_from_file(BIN_10x10)
    solutions = bp.solve()
    print("Done")
    for solution in solutions:
        print(solution)
        print()


def main():
    FutoshikiDataReader.read_file(FUT_4x4, 4)


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



