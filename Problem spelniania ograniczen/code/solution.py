from constraints import *
from utils import *
from solver import GridCSPSolver
from data_readers import BinaryDataReader, FutoshikiDataReader
from printers import pretty_binary_print

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

FORWARD_CHECK = False


def binary():

    mockup = BinaryDataReader.read_file(BIN_MODE, BIN_SIZE, empty_field_value=None)

    variables = generate_equal_domain_values(BIN_SIZE, [0, 1])
    constraints = [BinaryRatioConstraint(),
                   BinaryNeighbourConstraint(),
                   UniqueRowsConstraint(),
                   UniqueColumnsConstraint()]
    solver = GridCSPSolver(variables, constraints)
    solver.exclude_variables(mockup)

    solutions = solver.solve(forward_check=FORWARD_CHECK)
    print("Sol:")
    for sol in solutions:
        pretty_binary_print(sol, mockup)
        print()


if __name__ == '__main__':
    binary()
