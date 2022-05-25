from constraints import *
from utils import *
from solver import GridCSPSolver
from data_readers import BinaryDataReader, FutoshikiDataReader
from printers import pretty_binary_print, pretty_futoshiki_print
from data_collector import DataCollector


BIN_2x2 = '../data/binary_2x2'
BIN_4x4 = '../data/binary_4x4'
BIN_6x6 = '../data/binary_6x6'
BIN_8x8 = '../data/binary_8x8'
BIN_10x10 = '../data/binary_10x10'

FUT_4x4 = '../data/futoshiki_4x4'
FUT_5x5 = '../data/futoshiki_5x5'
FUT_6x6 = '../data/futoshiki_6x6'

# Binary:
BIN_SIZE = 10
BIN_MODE = BIN_10x10

# Futoshiki:
FUT_SIZE = 5
FUT_MODE = FUT_5x5

# Algorithm settings:
FORWARD_CHECK = True
ONE_SOLUTION = True
HEURISTIC = GridCSPSolver.LEAST_VALUES_FIRST


def binary():
    mockup = BinaryDataReader.read_file(BIN_MODE, BIN_SIZE, empty_field_value=None)

    variables = generate_equal_domain_values(BIN_SIZE, [0, 1])
    constraints = [BinaryRatioConstraint(),
                   BinaryNeighbourConstraint(),
                   UniqueColumnsConstraint(),
                   UniqueRowsConstraint()]
    solver = GridCSPSolver(variables, constraints, heuristic=HEURISTIC)
    solver.exclude_variables(mockup)

    pretty_binary_print(solver.grid, mockup)
    solutions = solver.solve(forward_check=FORWARD_CHECK, till_first_solution=ONE_SOLUTION)
    print(f"Solutions: {len(solutions)}")
    for sol in solutions:
        pretty_binary_print(sol, mockup)
        print()


def futoshiki():
    mockup, inequalities = FutoshikiDataReader.read_file(FUT_MODE, FUT_SIZE, empty_field_value=None)
    variables = generate_equal_domain_values(FUT_SIZE, [x + 1 for x in range(FUT_SIZE)])
    constraints = [UniqueRowElementsConstraint(empty_field_value=None),
                   UniqueColumnElementsConstraint(empty_field_value=None),
                   FutoshikiInequalitiesConstraint(inequalities, empty_field_value=None)]
    solver = GridCSPSolver(variables, constraints, heuristic=HEURISTIC)
    solver.exclude_variables(mockup)

    pretty_futoshiki_print(solver.grid, inequalities, mockup)
    print()
    solutions = solver.solve(forward_check=FORWARD_CHECK, till_first_solution=ONE_SOLUTION)
    print(f"Solutions: {len(solutions)}")
    for sol in solutions:
        pretty_futoshiki_print(sol, inequalities, mockup)
        print()


def futoshiki_heuristic_comparison(size, mode, forward_check):
    dc = DataCollector()
    print(f'=== Futoshiki {size} ===')
    mockup, inequalities = FutoshikiDataReader.read_file(mode, size, empty_field_value=None)
    variables = generate_equal_domain_values(size, [x + 1 for x in range(size)])
    constraints = [UniqueRowElementsConstraint(empty_field_value=None),
                   UniqueColumnElementsConstraint(empty_field_value=None),
                   FutoshikiInequalitiesConstraint(inequalities, empty_field_value=None)]

    # --- IN ORDER ---
    solver = GridCSPSolver(variables, constraints, data_collector=dc, heuristic=GridCSPSolver.IN_ORDER)
    solver.exclude_variables(mockup)
    solver.solve(forward_check=forward_check, till_first_solution=True)
    print(f'Forward check: {forward_check}')
    print(f'Heuristic: {GridCSPSolver.IN_ORDER.upper()}')
    print(f'Steps in: {dc.step_in}')
    print(f'Steps up: {dc.step_up}')
    print(f'Till fst: {dc.steps_till_first}')
    dc.reset()
    print()

    # --- LEAST VALUES FIRST ---
    solver = GridCSPSolver(variables, constraints, data_collector=dc, heuristic=GridCSPSolver.LEAST_VALUES_FIRST)
    solver.exclude_variables(mockup)
    solver.solve(forward_check=forward_check, till_first_solution=True)
    print(f'Forward check: {forward_check}')
    print(f'Heuristic: {GridCSPSolver.LEAST_VALUES_FIRST.upper()}')
    print(f'Steps in: {dc.step_in}')
    print(f'Steps up: {dc.step_up}')
    print(f'Till fst: {dc.steps_till_first}')
    dc.reset()
    print()

    # --- MOST VALUES FIRST ---
    solver = GridCSPSolver(variables, constraints, data_collector=dc, heuristic=GridCSPSolver.MOST_VALUES_FIRST)
    solver.exclude_variables(mockup)
    solver.solve(forward_check=forward_check, till_first_solution=True)
    print(f'Forward check: {forward_check}')
    print(f'Heuristic: {GridCSPSolver.MOST_VALUES_FIRST.upper()}')
    print(f'Steps in: {dc.step_in}')
    print(f'Steps up: {dc.step_up}')
    print(f'Till fst: {dc.steps_till_first}')
    dc.reset()
    print()

    # --- LEAST CONSTRAINTS FIRST ---
    solver = GridCSPSolver(variables, constraints, data_collector=dc, heuristic=GridCSPSolver.LEAST_CONSTRAINTS_FIRST)
    solver.exclude_variables(mockup)
    solver.solve(forward_check=forward_check, till_first_solution=True)
    print(f'Forward check: {forward_check}')
    print(f'Heuristic: {GridCSPSolver.LEAST_CONSTRAINTS_FIRST.upper()}')
    print(f'Steps in: {dc.step_in}')
    print(f'Steps up: {dc.step_up}')
    print(f'Till fst: {dc.steps_till_first}')
    dc.reset()
    print()

    # --- MOST CONSTRAINTS FIRST ---
    solver = GridCSPSolver(variables, constraints, data_collector=dc, heuristic=GridCSPSolver.MOST_CONSTRAINTS_FIRST)
    solver.exclude_variables(mockup)
    solver.solve(forward_check=forward_check, till_first_solution=True)
    print(f'Forward check: {forward_check}')
    print(f'Heuristic: {GridCSPSolver.MOST_CONSTRAINTS_FIRST.upper()}')
    print(f'Steps in: {dc.step_in}')
    print(f'Steps up: {dc.step_up}')
    print(f'Till fst: {dc.steps_till_first}')
    dc.reset()
    print()


if __name__ == '__main__':
    # binary()
    # futoshiki()
    test_list = [(4, FUT_4x4), (5, FUT_5x5), (6, FUT_6x6)]
    for size, mode in test_list:
        futoshiki_heuristic_comparison(size, mode, forward_check=False)
        futoshiki_heuristic_comparison(size, mode, forward_check=True)

    # size = 6
    # mode = FUT_6x6
    # forward_check = True
    #
    # dc = DataCollector()
    # print(f'=== Futoshiki {size} ===')
    # mockup, inequalities = FutoshikiDataReader.read_file(mode, size, empty_field_value=None)
    # variables = generate_equal_domain_values(size, [x + 1 for x in range(size)])
    # constraints = [UniqueRowElementsConstraint(empty_field_value=None),
    #                UniqueColumnElementsConstraint(empty_field_value=None),
    #                FutoshikiInequalitiesConstraint(inequalities, empty_field_value=None)]
    #
    # solver = GridCSPSolver(variables, constraints, data_collector=dc, heuristic=GridCSPSolver.LEAST_CONSTRAINTS_FIRST)
    # solver.exclude_variables(mockup)
    # solver.solve(forward_check=forward_check, till_first_solution=True)
    # print(f'Forward check: {forward_check}')
    # print(f'Heuristic: {GridCSPSolver.LEAST_CONSTRAINTS_FIRST.upper()}')
    # print(f'Steps in: {dc.step_in}')
    # print(f'Steps up: {dc.step_up}')
    # print(f'Till fst: {dc.steps_till_first}')
    # dc.reset()
    # print()

