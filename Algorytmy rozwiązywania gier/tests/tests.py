import unittest as ut
from checkers import Checkers
from pieces import Pawn, Queen
from colors import Color
from players import Player


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

    def test_no_loop_paths(self):
        checkers = Checkers.empty_board_checkers()
        checkers.board[2][2].piece = Pawn(Checkers.WHITE, Color.FG.WHITE)
        checkers.board[1][3].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[3][3].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[3][1].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[5][1].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[5][3].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        pieces = checkers.get_pieces()
        pawns, _ = checkers.get_capturing_pieces(pieces)
        path = checkers.get_possible_pawn_captures(pawns)
        self.assertEqual(path, [[(2, 2), (4, 0), (6, 2), (4, 4), (2, 2), (0, 4)], [(2, 2), (4, 4), (6, 2), (4, 0), (2, 2), (0, 4)]])

    def test_pawn_move(self):
        c = Checkers(Player(Checkers.WHITE), Player(Checkers.BLACK))
        self.assertEqual(c.can_pawn_move(0, 0), False)
        self.assertEqual(c.can_pawn_move(1, 1), True)
        self.assertEqual(c.can_pawn_move(7, 7), False)
        self.assertEqual(c.can_pawn_move(6, 6), False)
        c.current_colour = c.BLACK
        self.assertEqual(c.can_pawn_move(1, 1), False)
        self.assertEqual(c.can_pawn_move(6, 6), True)

    def test_can_queen_capture(self):
        checkers = Checkers.empty_board_checkers()
        checkers.board[5][1].piece = Queen(Checkers.WHITE, Color.FG.WHITE)
        checkers.board[2][4].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        cqc = checkers.can_queen_capture(5, 1, [])
        self.assertEqual(cqc, True)
        checkers = Checkers.empty_board_checkers()
        checkers.board[5][1].piece = Queen(Checkers.WHITE, Color.FG.WHITE)
        checkers.board[0][6].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        cqc = checkers.can_queen_capture(5, 1, [])
        self.assertEqual(cqc, False)

    def test_queen_landing_spots(self):
        checkers = Checkers.empty_board_checkers()
        checkers.board[4][4].piece = Queen(Checkers.WHITE, Color.FG.WHITE)
        checkers.board[3][5].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[2][2].piece = Queen(Checkers.BLACK, Color.FG.BLACK)
        spots_pair = checkers.get_queen_landing_spots(4, 4, [])
        spots1 = spots_pair[0][1]
        enemy1 = spots_pair[0][0]
        spots2 = spots_pair[1][1]
        enemy2 = spots_pair[1][0]
        self.assertListEqual(spots1, [(1, 1), (0, 0)])
        self.assertEqual(enemy1, (2, 2))
        self.assertEqual(enemy2, (3, 5))
        self.assertListEqual(spots2, [(2, 6), (1, 7)])

        checkers = Checkers.empty_board_checkers()
        checkers.board[5][5].piece = Queen(Checkers.WHITE, Color.FG.WHITE)
        checkers.board[4][6].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[4][4].piece = Queen(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[1][1].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        spots_pair = checkers.get_queen_landing_spots(5, 5, [checkers.board[4][6]])
        spots = spots_pair[0][1]
        enemy = spots_pair[0][0]
        self.assertListEqual(spots, [(3, 3), (2, 2)])
        self.assertEqual(enemy, (4, 4))

    def test_queen_capture_path(self):
        checkers = Checkers.empty_board_checkers()
        checkers.board[7][3].piece = Queen(Checkers.WHITE, Color.FG.WHITE)
        checkers.board[5][5].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[1][5].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[1][3].piece = Queen(Checkers.BLACK, Color.FG.BLACK)
        checkers.board[4][2].piece = Pawn(Checkers.BLACK, Color.FG.BLACK)
        checkers.print_board()
        cap = checkers.get_possible_queen_captures([(7, 3)])
        self.assertEqual(len(cap), 3)



