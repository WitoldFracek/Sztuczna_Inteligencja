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


class Checkers:
    def __init__(self, pawn_rows=2):
        self.board = [[Cell(f'{letter}{number}') for letter in 'ABCDEFGH'] for number in '12345678']
        for i in range(pawn_rows):
            if i % 2 == 0:
                for cell in self.board[i][::2]:
                    cell.piece = Pawn(Pawn.WHITE)
                for cell in self.board[-1 - i][1::2]:
                    cell.piece = Pawn(Pawn.BLACK)
            else:
                for cell in self.board[i][1::2]:
                    cell.piece = Pawn(Pawn.WHITE)
                for cell in self.board[-1 - i][::2]:
                    cell.piece = Pawn(Pawn.BLACK)

    def can_capture(self) -> bool:
        pawns_coordinates = []
        for i, line in enumerate(self.board):
            for j, cell in enumerate(line):
                if cell.piece is not None:
                    pawns_coordinates.append((i, j))
        return any([self.can_pawn_capture(x, y) for x, y in pawns_coordinates])

    def can_pawn_capture(self, x, y) -> bool:
        pass

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


