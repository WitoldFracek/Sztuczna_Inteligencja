from data_readers import BinaryDataReader
from binary_puzzle import BinaryPuzzle
import numpy as np

# Binary
PATH_6x6 = '../data/binary_6x6'
PATH_8x8 = '../data/binary_8x8'
PATH_10x10 = '../data/binary_10x10'


def main():
    bp = BinaryPuzzle(6)
    bp.load_from_file(PATH_6x6)
    xs = bp.solve()
    print("Done")
    print(xs)


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



