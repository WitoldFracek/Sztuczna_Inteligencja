from variable import Variable


# Binary Puzzle
def binary_check_neighbours(grid, variable: Variable, value):
    pass


def __check_neighbour_by_axes(grid, variable: Variable, value, axes: int):
    x, y = variable.position
    line = grid[x:, :] if axes == 0 else grid[:, y]
    left = line[max(0, y - 2):y] if axes == 0 else line[max(0, x - 2):x]
    right = line[y + 1:min(len(line), y + 3)] if axes == 0 else line[x + 1:min(len(line), x + 3)]


def __is_neighbour_slice_correct(neighbour_slice, grid, value):
    if len(neighbour_slice) < 2:
        return True
    if any([v.value is None for v in neighbour_slice]):
        return True
    values = [v.value for v in neighbour_slice]
    if sum(values) + value == 0 or sum(values) + value == 3:
        return False
    return True



