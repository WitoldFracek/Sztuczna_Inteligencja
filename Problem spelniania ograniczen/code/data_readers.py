import numpy as np


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



