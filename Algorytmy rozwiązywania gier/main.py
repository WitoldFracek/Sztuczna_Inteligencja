from cell import Cell
from checkers import Checkers
from pieces import Piece, Pawn
from colors import Color

if __name__ == '__main__':
    c = Checkers(pawn_rows=2)
    c.board[2][2].piece = Pawn(c.BLACK, Color.FG.BLACK)
    c.board[4][4].piece = Pawn(c.BLACK, Color.FG.BLACK)
    # c.board[7][3].piece = None
    c.print_board()
    pieces = c.get_pieces()
    cp, _ = c.get_capturing_pieces(pieces)
    p = c.get_possible_pawn_captures(cp)
    print(p)
