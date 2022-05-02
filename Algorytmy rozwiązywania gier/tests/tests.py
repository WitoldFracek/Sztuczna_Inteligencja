import unittest as ut
from checkers import Checkers
from pieces import Pawn
from colors import Color


class CapturingPathTest(ut.TestCase):
    def test_one_path(self):
        checkers = Checkers.empty_board_checkers()
        checkers.board[0][0].piece = Pawn(Checkers.WHITE, Color.FG.WHITE)
        checkers.board[1][1].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[3][3].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[5][5].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[7][7].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        pieces = checkers.get_pieces()
        pawns, _ = checkers.get_capturing_pieces(pieces)
        path = checkers.get_possible_pawn_captures(pawns)
        self.assertListEqual([(0, 0), (2, 2), (4, 4), (6, 6)], path[0])

    def test_two_paths(self):
        checkers = Checkers.empty_board_checkers()
        checkers.board[0][2].piece = Pawn(Checkers.WHITE, Color.FG.WHITE)
        checkers.board[1][1].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[1][3].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[3][1].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[3][5].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        pieces = checkers.get_pieces()
        pawns, _ = checkers.get_capturing_pieces(pieces)
        path = checkers.get_possible_pawn_captures(pawns)
        self.assertEqual(len(path), 2)
        self.assertListEqual([(0, 2), (2, 0), (4, 2)], path[0])
        self.assertListEqual([(0, 2), (2, 4), (4, 6)], path[1])

    def test_longest_path(self):
        checkers = Checkers.empty_board_checkers()
        checkers.board[0][2].piece = Pawn(Checkers.WHITE, Color.FG.WHITE)
        checkers.board[1][1].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[1][3].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[3][1].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[3][5].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[5][3].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        pieces = checkers.get_pieces()
        pawns, _ = checkers.get_capturing_pieces(pieces)
        path = checkers.get_possible_pawn_captures(pawns)
        self.assertEqual(len(path), 1)
        self.assertListEqual([(0, 2), (2, 0), (4, 2), (6, 4)], path[0])


class MovePawnTest(ut.TestCase):
    def test_pawn_move(self):
        c = Checkers()
        c.print_board()
        self.assertEqual(c.can_pawn_move(0, 0), False)
        self.assertEqual(c.can_pawn_move(1, 1), True)
        self.assertEqual(c.can_pawn_move(7, 7), False)
        self.assertEqual(c.can_pawn_move(6, 6), True)

