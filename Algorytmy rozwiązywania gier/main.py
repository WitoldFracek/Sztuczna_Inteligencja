from cell import Cell
from checkers import Checkers
from pieces import Piece, Pawn
from colors import Color
from players import Human, DummyBot

if __name__ == '__main__':
    c = Checkers(DummyBot(Checkers.WHITE, name='Witek'), DummyBot(Checkers.BLACK), pawn_rows=3, start_colour=Checkers.WHITE)
    # c.board[2][2].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
    # c.board[4][4].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
    # c.board[4][2].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
    # c.board[1][3].piece = None
    c.play()
    # c.is_queen_jump_possible(3, 3, (-1, -1))
