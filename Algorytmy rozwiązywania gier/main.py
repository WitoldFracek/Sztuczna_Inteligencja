from cell import Cell
from checkers import Checkers
from pieces import Piece, Pawn
from colors import Color
from players import Human, DummyBot, MinMaxBot
from estimators import BasicEstimator

if __name__ == '__main__':
    # c = Checkers(DummyBot(Checkers.WHITE, name='Witek'), DummyBot(Checkers.BLACK), pawn_rows=3, start_colour=Checkers.WHITE)
    est = BasicEstimator()
    c = Checkers(Human(Checkers.BLACK, name='Witek'),
                 MinMaxBot(Checkers.WHITE, est, search_depth=3, time_constraint=20),
                 pawn_rows=2,
                 start_colour=Checkers.WHITE)
    # c = Checkers(MinMaxBot(Checkers.WHITE, est, search_depth=3),
    #              MinMaxBot(Checkers.BLACK, est, search_depth=3),
    #              pawn_rows=2,
    #              start_colour=Checkers.WHITE)
    c.play()
