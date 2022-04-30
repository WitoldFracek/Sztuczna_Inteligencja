from constraints import *
from utils import *
from solver import GridCSPSolver
from data_readers import BinaryDataReader, FutoshikiDataReader
from printers import pretty_binary_print, pretty_futoshiki_print
from data_collector import DataCollector
from datetime import datetime


BIN_2x2 = '../data/binary_2x2'
BIN_4x4 = '../data/binary_4x4'
BIN_6x6 = '../data/binary_6x6'
BIN_8x8 = '../data/binary_8x8'
BIN_10x10 = '../data/binary_10x10'

BIN_TEST = '../data/comp/4x4_test'

COMP_BIN_4x4 = '../data/comp/binary_4x4'
COMP_BIN_6x6 = '../data/comp/binary_6x6'
COMP_BIN_8x8 = '../data/comp/binary_8x8'
COMP_BIN_10x10 = '../data/comp/binary_10x10'

FUT_3x3 = '../data/futoshiki_3x3'
FUT_4x4 = '../data/futoshiki_4x4'
FUT_5x5 = '../data/futoshiki_5x5'
FUT_6x6 = '../data/futoshiki_6x6'

COMP_FUT_3x3 = '../data/comp/futoshiki_3x3'
COMP_FUT_4x4 = '../data/comp/futoshiki_4x4'
COMP_FUT_5x5 = '../data/comp/futoshiki_5x5'
COMP_FUT_6x6 = '../data/comp/futoshiki_6x6'

# Binary:
BIN_SIZE = 4
BIN_MODE = BIN_TEST

# Futoshiki:
FUT_SIZE = 6
FUT_MODE = FUT_6x6

# Algorithm settings:
FORWARD_CHECK = False
ONE_SOLUTION = False
HEURISTIC = GridCSPSolver.IN_ORDER


def binary():
    mockup = BinaryDataReader.read_file(BIN_MODE, BIN_SIZE, empty_field_value=None)

    variables = generate_equal_domain_values(BIN_SIZE, [0, 1])
    constraints = [BinaryRatioConstraint(),
                   BinaryNeighbourConstraint(),
                   UniqueColumnsConstraint(),
                   UniqueRowsConstraint()]
    start = datetime.now()
    solver = GridCSPSolver(variables, constraints, heuristic=HEURISTIC, data_collector=DataCollector())
    solver.exclude_variables(mockup)
    # pretty_binary_print(solver.grid, mockup)
    solutions = solver.solve(forward_check=FORWARD_CHECK, till_first_solution=ONE_SOLUTION)
    end = datetime.now()
    print(end - start)
    print(f'Nodes: {solver.data_collector.nodes}')
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

    start = datetime.now()
    for i in range(10):
        solver = GridCSPSolver(variables, constraints, heuristic=HEURISTIC, data_collector=DataCollector())
        solver.exclude_variables(mockup)
        # pretty_futoshiki_print(solver.grid, inequalities, mockup)
        # print()
        solutions = solver.solve(forward_check=FORWARD_CHECK, till_first_solution=ONE_SOLUTION)
    end = datetime.now()
    print((end - start) / 10)
    print((end - start).microseconds * 1e-7)
    print(f'Powroty: {solver.data_collector.nodes}')


    # print(f"Solutions: {len(solutions)}")
    # for sol in solutions:
    #     pretty_futoshiki_print(sol, inequalities, mockup)
    #     print()


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


def data_profile():
    bin_sizes = [6, 8, 10]
    bin_modes = [BIN_6x6, BIN_8x8, BIN_10x10]
    fut_sizes = [4, 5, 6]
    fut_modes = [FUT_4x4, FUT_5x5, FUT_6x6]
    heuristics = [GridCSPSolver.IN_ORDER, GridCSPSolver.LEAST_VALUES_FIRST, GridCSPSolver.MOST_CONSTRAINTS_FIRST]

    for mode, size in zip(bin_modes, bin_sizes):
        measure_binary(False, mode, size)
        for heuristic in heuristics:
            measure_binary(True, mode, size, heuristic)
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    for mode, size in zip(fut_modes, fut_sizes):
        measure_futoshiki(False, mode, size)
        for heuristic in heuristics:
            measure_futoshiki(True, mode, size, heuristic)


def measure_binary(forward_check, bin_mode, bin_size, heuristic=GridCSPSolver.IN_ORDER):
    mockup = BinaryDataReader.read_file(bin_mode, bin_size, empty_field_value=None)

    variables = generate_equal_domain_values(bin_size, [0, 1])
    constraints = [BinaryRatioConstraint(),
                   BinaryNeighbourConstraint(),
                   UniqueColumnsConstraint(),
                   UniqueRowsConstraint()]
    start = datetime.now()
    for i in range(10):
        solver = GridCSPSolver(variables, constraints, heuristic=heuristic, data_collector=DataCollector())
        solver.exclude_variables(mockup)
        # pretty_binary_print(solver.grid, mockup)
        solutions = solver.solve(forward_check=forward_check, till_first_solution=ONE_SOLUTION)
    end = datetime.now()
    print(f'BINARY: {bin_size}, FC: {forward_check}')
    if forward_check:
        print(f'Heuristic: {heuristic}')
    print(f'Time: {((end - start) / 10)}')
    print(f'Nodes: {solver.data_collector.nodes}\n')


def measure_futoshiki(forward_check, fut_mode, fut_size, heuristic=GridCSPSolver.IN_ORDER):
    mockup, inequalities = FutoshikiDataReader.read_file(fut_mode, fut_size, empty_field_value=None)
    variables = generate_equal_domain_values(fut_size, [x + 1 for x in range(FUT_SIZE)])
    constraints = [UniqueRowElementsConstraint(empty_field_value=None),
                   UniqueColumnElementsConstraint(empty_field_value=None),
                   FutoshikiInequalitiesConstraint(inequalities, empty_field_value=None)]

    start = datetime.now()
    for i in range(10):
        solver = GridCSPSolver(variables, constraints, heuristic=heuristic, data_collector=DataCollector())
        solver.exclude_variables(mockup)
        # pretty_futoshiki_print(solver.grid, inequalities, mockup)
        # print()
        solutions = solver.solve(forward_check=forward_check, till_first_solution=ONE_SOLUTION)
    end = datetime.now()
    print(f'FUTOSHIKI: {fut_size}, FC: {forward_check}')
    if forward_check:
        print(f'Heuristic: {heuristic}')
    print(f'Time: {((end - start) / 10)}')
    print(f'Nodes: {solver.data_collector.nodes}\n')


if __name__ == '__main__':
    # data_profile()
    # print(f'FC: {FORWARD_CHECK}')
    # if FORWARD_CHECK:
    #     print(f'Heuristic: {HEURISTIC}')
    # print(f'Binary: {BIN_SIZE}')
    binary()
    # print()
    # print(f'Futoshiki: {FUT_SIZE}')
    # futoshiki()


    # test_list = [(4, FUT_4x4), (5, FUT_5x5), (6, FUT_6x6)]
    # for size, mode in test_list:
    #     futoshiki_heuristic_comparison(size, mode, forward_check=False)
    #     futoshiki_heuristic_comparison(size, mode, forward_check=True)

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

