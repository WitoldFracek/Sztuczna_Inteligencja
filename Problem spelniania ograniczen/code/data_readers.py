import numpy as np
import typing

class BinaryDataReader:

    @staticmethod
    def read_file(path, puzzle_size, empty_field_marker='x'):
        with open(path, encoding='utf-8') as file:
            lines = file.readlines()
        if len(lines) != puzzle_size:
            raise BinaryDataException(message=f"""
            Number of lines in the specified file is inconsistent with given puzzle size.
            File at {path}
            Given puzzle size: {puzzle_size}
            Lines fetched: {len(lines)}
            """)
        ret = np.full((puzzle_size, puzzle_size), -1, dtype=np.int8)
        for i, line in enumerate(lines):
            line = line.strip()
            if len(line) != puzzle_size:
                raise BinaryDataException(message=f"""
                Incorrect data in file. Given puzzle size is {puzzle_size} but the length of line is {len(line)}
                """)
            for j, elem in enumerate(line):
                if elem != empty_field_marker:
                    value = int(elem)
                    ret[i, j] = value
        return ret


class BinaryDataException(Exception):
    def __init__(self, message=""):
        Exception.__init__(self, message)


class FutoshikiDataReader:

    @staticmethod
    def read_file(path, puzzle_size, empty_field_marker='x', gt_marker='>', lt_marker='<', ignore_marker='-'):
        with open(path, encoding='utf-8') as file:
            data = file.readlines()
        lines = [line.strip() for line in data]
        value_lines = lines[::2]
        if len(value_lines) != puzzle_size:
            raise FutoshikiDataException(message=f"""
                        Number of value lines in the specified file is inconsistent with given puzzle size.
                        File at {path}
                        Given puzzle size: {puzzle_size}
                        Value lines fetched: {len(value_lines)}
                        """)
        constraint_lines = lines[1::2]
        if len(constraint_lines) + 1 != puzzle_size:
            raise FutoshikiDataException(message=f"""
                                    Number of constraint lines in the specified file is inconsistent with given puzzle size.
                                    File at {path}
                                    Given puzzle size: {puzzle_size}
                                    Value lines fetched: {len(value_lines)} (one between each value line).
                                    """)
        grid = FutoshikiDataReader.__fetch_values_data(value_lines, puzzle_size, empty_field_marker)
        formatted = FutoshikiDataReader.__convert_to_2D_array(constraint_lines, value_lines, ignore_marker)
        con = FutoshikiDataReader.__find_constraints(formatted, lt_marker, gt_marker, ignore_marker)
        return grid, con

    @staticmethod
    def __fetch_values_data(value_lines, puzzle_size, empty_field_marker):
        ret = np.full((puzzle_size, puzzle_size), 0, dtype=np.int8)
        for i, line in enumerate(value_lines):
            if len(line) // 2 + 1 != puzzle_size:
                raise FutoshikiDataException(message=f"""
                Incorrect data in file. Given puzzle size is {puzzle_size} but the length of line is {len(line) // 2 + 1}
                """)
            for j, elem in enumerate(line[::2]):
                if elem != empty_field_marker:
                    ret[i, j] = int(elem)
        return ret

    @staticmethod
    def __convert_to_2D_array(constraints_list, value_list, ignore_marker):
        ret = []
        for i in range(len(value_list)):
            row = []
            for marker in value_list[i]:
                row.append(marker)
            ret.append(row)
            if i < len(value_list) - 1:
                row = []
                for marker in constraints_list[i]:
                    row.append(marker)
                    row.append(ignore_marker)
                ret.append(row[:-1])
        return ret

    @staticmethod
    def __find_constraints(formatted, lt_marker, gt_marker, ignore_marker):
        constraints = []
        for i in range(len(formatted)):
            for j in range(len(formatted[i])):
                res = FutoshikiDataReader.__check_vertical(formatted, i, j, lt_marker, gt_marker, ignore_marker)
                if len(res) == 3:
                    constraints.append(res)
                res = FutoshikiDataReader.__check_horizontal(formatted, i, j, lt_marker, gt_marker, ignore_marker)
                if len(res) == 3:
                    constraints.append(res)
        return constraints

    @staticmethod
    def __check_vertical(formatted, x, y, lt_marker, gt_marker, ignore_marker):
        ops = {lt_marker, gt_marker, ignore_marker}
        if y - 1 < 0:
            return ()
        if y + 1 > len(formatted[x]):
            return ()
        if formatted[x][y] in ops:
            if formatted[x][y-1] in ops:
                return ()
            elif formatted[x][y] == lt_marker:
                return (x // 2, (y - 1) // 2), (x // 2, (y + 1) // 2), -1
            elif formatted[x][y] == gt_marker:
                return (x // 2, (y - 1) // 2), (x // 2, (y + 1) // 2), 1
        return ()

    @staticmethod
    def __check_horizontal(formatted, x, y, lt_marker, gt_marker, ignore_marker):
        ops = {lt_marker, gt_marker, ignore_marker}
        if x - 1 < 0:
            return ()
        if x + 1 > len(formatted):
            return ()
        if formatted[x][y] in ops:
            if formatted[x - 1][y] in ops:
                return ()
            elif formatted[x][y] == lt_marker:
                return ((x - 1) // 2, y // 2), ((x + 1) // 2, y // 2), -1
            elif formatted[x][y] == gt_marker:
                return ((x - 1) // 2, y // 2), ((x + 1) // 2, y // 2), 1
        return ()


class FutoshikiDataException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)




