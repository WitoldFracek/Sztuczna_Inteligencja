from cell import Cell
from checkers import Checkers

if __name__ == '__main__':
    c = Checkers(pawn_rows=2)
    c.print_board()
    x, y = c.decode_alias('C7')
    print(c.board[x][y])
