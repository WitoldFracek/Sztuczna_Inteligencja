from cell import Cell
from checkers import Checkers
from pieces import Piece, Pawn
from colors import Color

if __name__ == '__main__':
    c = Checkers(pawn_rows=2, start_colour=Checkers.WHITE)
    # c.board[2][2].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
    # c.board[4][4].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
    # c.board[4][2].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
    # c.board[1][3].piece = None
    c.print_board()
    c.play()
