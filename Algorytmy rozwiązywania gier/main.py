from cell import Cell
from checkers import Checkers
from pieces import Piece, Pawn

if __name__ == '__main__':
    c = Checkers(pawn_rows=2)
    c.board[2][2].piece = Pawn(Piece.BLACK)
    c.print_board()
    print(c.can_capture(Piece.BLACK))
