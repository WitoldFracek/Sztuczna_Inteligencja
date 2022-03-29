from data_readers import BinaryDataReader
from binary_puzzle import BinaryPuzzle
import numpy as np

# Binary
PATH_6x6 = '../data/binary_6x6'
PATH_8x8 = '../data/binary_8x8'
PATH_10x10 = '../data/binary_10x10'


def main():
    grid = np.array([[1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 0, 1, 1],
                     [1, 0, 0, 1, 0, 1],
                     [0, 1, 1, 0, 1, 0],
                     [0, 0, 1, 1, 0, 1],
                     [1, 1, 0, 1, 0, 0]], dtype=np.int8)
    bp = BinaryPuzzle(6, grid=grid)
    ok = check_whole_grid(bp)
    # print(grid[:, 0])
    for elem in ok:
        print(elem)
    # print(bp.check_ratio((0, 0), 0))
    # print(bp.check_duplicate_lines())
    # print(bp.check_neighbours((0, 0), 0, axes=0))
    # print(bp.check_neighbours((0, 0), 0, axes=1))


def check_whole_grid(puzzle: BinaryPuzzle):
    ret = []
    x, y = puzzle.grid.shape
    for i in range(x):
        for j in range(y):
            store = puzzle.grid[i, j]
            puzzle.grid[i, j] = -1
            print(store)
            tpl = (puzzle.check_ratio((i, j), store),
                   puzzle.check_duplicate_lines(),
                   puzzle.check_neighbours((i, j), store, 0),
                   puzzle.check_neighbours((i, j), store, 1),
                   (i, j))
            puzzle.grid[i, j] = store
            ret.append(tpl)
            if i == 0 and j == 1:
                return ret
    return ret


if __name__ == '__main__':
    main()



