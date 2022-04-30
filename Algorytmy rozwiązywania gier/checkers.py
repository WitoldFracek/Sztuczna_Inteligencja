from cell import Cell
from pieces import Piece, Pawn, Queen
from colors import Color
from utils import first_index

#    A B C D E F G H
#   ________________
# 1| x   x   x   x
# 2|   x   x   x   x
# 3| x   x   x   x
# 4|   x   x   x   x
# 5| x   x   x   x
# 6|   x   x   x   x
# 7| x   x   x   x
# 8|   x   x   x   x


class CapturePath:
    def __init__(self, start):
        self.start = start
        self.path = []

    def __iadd__(self, other):
        self.path.append(other)

    def get_path(self):
        return self.start, self.path


class Checkers:
    WHITE = 'w'
    BLACK = 'b'

    def __init__(self, pawn_rows=2, start_colour=WHITE):
        self.board = [[Cell(f'{letter}{number}') for letter in 'ABCDEFGH'] for number in '12345678']
        self.current_colour = start_colour
        rows = min(max(pawn_rows, 1), 3)
        for i in range(rows):
            if i % 2 == 0:
                for cell in self.board[i][::2]:
                    cell.piece = Pawn(self.WHITE, Color.FG.WHITE)
                for cell in self.board[-1 - i][1::2]:
                    cell.piece = Pawn(self.BLACK, Color.FG.BLACK)
            else:
                for cell in self.board[i][1::2]:
                    cell.piece = Pawn(self.WHITE, Color.FG.WHITE)
                for cell in self.board[-1 - i][::2]:
                    cell.piece = Pawn(self.BLACK, Color.FG.BLACK)

    def play(self):
        while True:
            # player 1
            pieces = self.get_pieces()
            capturing_pawns, capturing_queens = self.get_capturing_pieces(pieces)
            if capturing_pawns or capturing_queens:
                self.get_possible_pawn_captures(capturing_pawns)
            else:
                pass
            break

    def get_pieces(self) -> list[tuple[int, int]]:
        pawns_coordinates = []
        for i, line in enumerate(self.board):
            for j, cell in enumerate(line):
                if cell.piece is not None:
                    if cell.piece.colour == self.current_colour:
                        pawns_coordinates.append((i, j))
        return pawns_coordinates

    def get_capturing_pieces(self, pawns_coordinates) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        capturing_pawns = []
        capturing_queens = []
        for x, y in pawns_coordinates:
            cell = self.board[x][y]
            if isinstance(cell.piece, Pawn):
                if self.can_pawn_capture(x, y):
                    capturing_pawns.append((x, y))
            elif isinstance(cell.piece, Queen):
                if self.can_queen_capture(x, y):
                    capturing_queens.append((x, y))
        return capturing_pawns, capturing_queens

    def can_pawn_capture(self, x, y, excluded_cells=None) -> bool:
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direction in directions:
            if self.is_pawn_jump_possible(x, y, direction, excluded_cells=excluded_cells):
                return True
        return False

    def is_pawn_jump_possible(self, x, y, direction, excluded_cells=None):
        xd, yd = direction
        if 0 <= x + xd < len(self.board) \
                and 0 <= y + yd < len(self.board) \
                and 0 <= x + 2 * xd < len(self.board) \
                and 0 <= y + 2 * yd < len(self.board):
            cell = self.board[x + xd][y + yd]
            if excluded_cells is not None:
                if cell in excluded_cells:
                    return False
            if not cell.is_empty:
                if cell.is_opposite_colour(self.board[x][y]):
                    if self.board[x + 2 * xd][y + 2 * yd].is_empty:
                        return True
        return False

    def can_queen_capture(self, x, y) -> bool:
        return False

    def get_possible_pawn_captures(self, capturing_pawns: list[tuple[int, int]]):
        paths = []
        for x, y in capturing_pawns:
            for p in self.get_pawn_capture_path(x, y, []):
                paths.append(p)
        max_len = max(paths, key=len)
        return [p for p in paths if len(p) == max_len]

    def get_pawn_capture_path(self, x, y, jumped_over: list[Cell]):
        if self.can_pawn_capture(x, y, excluded_cells=jumped_over):
            path_lu = self.get_pawn_capture_path(x - 2, y - 2, list(jumped_over))
            path_ld = self.get_pawn_capture_path(x - 2, y + 2, list(jumped_over))
            path_ru = self.get_pawn_capture_path(x + 2, y - 2, list(jumped_over))
            path_rd = self.get_pawn_capture_path(x + 2, y + 2, list(jumped_over))
            paths = [path_lu, path_ld, path_ru, path_rd]
            max_length = max(paths, key=len)
            longest_paths = [p for p in paths if len(p) == max_length]
            return longest_paths
        return []

    def pawn_jump(self, x_start: int, y_start: int, direction: tuple[int, int]):
        xd, yd = direction
        return x_start + 2 * xd, y_start + 2 * yd, x_start + xd, y_start + yd

    def pawn_capture_directions(self, x, y, excluded_cells=None) -> list[tuple[int, int]]:
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        ret = []
        for direction in directions:
            if self.is_pawn_jump_possible(x, y, direction, excluded_cells=excluded_cells):
                ret.append(direction)
        return ret

    def print_board(self):
        print('   A  B  C  D  E  F  G  H ')
        for i, line in enumerate(self.board):
            s = f'{i + 1} '
            for j, cell in enumerate(line):
                if i % 2 == 0:
                    if j % 2 == 0:
                        s += f' {cell.marker} '
                    else:
                        s += f'{Color.BG.WHITE} {cell.marker} {Color.END}'
                else:
                    if j % 2 == 0:
                        s += f'{Color.BG.WHITE} {cell.marker} {Color.END}'
                    else:
                        s += f' {cell.marker} '
            s += f' {i + 1}'
            print(s)
        print('   A  B  C  D  E  F  G  H ')

    def decode_alias(self, alias: str):
        return first_index('12345678', lambda x: x == alias[1]), first_index('ABCDEFGH', lambda x: x == alias[0])


