import cell
from cell import Cell
from pieces import Piece, Pawn, Queen
from colors import Color
from utils import first_index
from players import Player, Human

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
    WHITE = 'w'
    BLACK = 'b'

    def __init__(self, player1: Player, player2: Player, pawn_rows=2, start_colour=WHITE):
        self.board = [[Cell(f'{letter}{number}') for letter in 'ABCDEFGH'] for number in '12345678']
        self.current_colour = start_colour
        self.white_count = 4 * pawn_rows
        self.black_count = 4 * pawn_rows
        self.last_move = []
        if player1 is None or player2 is None:
            raise Exception(f'Given players are None values')
        if player1.colour == player2.colour:
            raise Exception(f'Players have the same colour! Given :{player1.colour}')
        self.player1 = player1
        self.player2 = player2
        if self.player1.colour == start_colour:
            self.current_player = player1
        else:
            self.current_player = player2
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
        self.__directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    @classmethod
    def empty_board_checkers(cls, start_colour=WHITE):
        c = cls(Player(cls.WHITE), Player(cls.BLACK), start_colour=start_colour)
        for line in c.board:
            for cell in line:
                cell.piece = None
        return c

    # === CONTROLS === -------------------------------------------------------------------------------
    def play(self):
        while self.white_count and self.black_count:
            self.print_board()
            self.one_move()
        self.__switch_player()
        self.print_board()
        print(f'Player {self.current_player.name} win!')

    def __switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.current_colour = self.current_player.colour
        else:
            self.current_player = self.player1
            self.current_colour = self.current_player.colour

    def one_move(self):
        pieces = self.get_pieces()
        capturing_pawns, capturing_queens = self.get_capturing_pieces(pieces)
        if capturing_pawns or capturing_queens:
            pawn_captures = self.get_possible_pawn_captures(capturing_pawns)
            queen_captures = self.get_possible_queen_captures(capturing_queens)
            captures = self.__get_longest_captures(pawn_captures, queen_captures)
            pos = self.current_player.capture(captures, self.board)
            self.execute_capture(pos, captures)
        else:
            moving_pawns, moving_queens = self.get_moving_pieces(pieces)
            pawn_moves = self.get_possible_pawn_moves(moving_pawns)
            queen_moves = self.get_possible_queen_moves(moving_queens)
            pos = self.current_player.move(pawn_moves + queen_moves, self.board)
            self.execute_move(pos, pawn_moves + queen_moves)
        self.promote_to_queen()
        self.__switch_player()

    def execute_move(self, pos, available_moves):
        move = available_moves[pos]
        self.last_move = move
        start_x, start_y = move[0]
        end_x, end_y = move[1]
        moving_piece = self.board[start_x][start_y].piece
        self.board[start_x][start_y].piece = None
        self.board[end_x][end_y].piece = moving_piece

    def execute_capture(self, pos, available_captures):
        capture = available_captures[pos]
        self.last_move = capture
        sx, sy = capture[0]
        moving_piece = self.board[sx][sy].piece
        self.board[sx][sy].piece = None
        for ex, ey in capture[1:]:
            cx, cy = self.__get_captured_enemy(sx, sy, ex, ey)
            if self.current_colour == self.WHITE:
                self.black_count -= 1
            else:
                self.white_count -= 1
            self.board[cx][cy].piece = None
            sx = ex
            sy = ey
        self.board[sx][sy].piece = moving_piece

    def promote_to_queen(self):
        for i in range(8):
            cell1 = self.board[0][i]
            if not cell1.is_empty:
                if cell1.piece.colour == self.BLACK:
                    if isinstance(cell1.piece, Pawn):
                        cell1.piece = cell1.piece.transform_to_queen()
            cell2 = self.board[7][i]
            if not cell2.is_empty:
                if cell2.piece.colour == self.WHITE:
                    if isinstance(cell2.piece, Pawn):
                        cell2.piece = cell2.piece.transform_to_queen()

    # === PIECE ACCESSORS === --------------------------------------------------------------------------------
    def get_pieces(self) -> list[tuple[int, int]]:
        pawns_coordinates = []
        for i, line in enumerate(self.board):
            for j, cell in enumerate(line):
                if cell.piece is not None:
                    if cell.piece.colour == self.current_colour:
                        pawns_coordinates.append((i, j))
        return pawns_coordinates

    def get_capturing_pieces(self, pieces_coordinates) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        capturing_pawns = []
        capturing_queens = []
        for x, y in pieces_coordinates:
            cell = self.board[x][y]
            if isinstance(cell.piece, Pawn):
                if self.can_pawn_capture(x, y):
                    capturing_pawns.append((x, y))
            elif isinstance(cell.piece, Queen):
                if self.can_queen_capture(x, y, []):
                    capturing_queens.append((x, y))
        return capturing_pawns, capturing_queens

    def get_moving_pieces(self, pieces_coordinates) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        moving_pawns = []
        moving_queens = []
        for x, y in pieces_coordinates:
            piece = self.board[x][y].piece
            if isinstance(piece, Pawn):
                if self.can_pawn_move(x, y):
                    moving_pawns.append((x, y))
            elif isinstance(piece, Queen):
                if self.can_queen_move(x, y):
                    moving_queens.append((x, y))
        return moving_pawns, moving_queens

    # === MOVES ACCESSORS === --------------------------------------------------------------------------------
    def get_possible_pawn_moves(self, moving_pawns: list[tuple[int, int]]):
        moves = []
        for x, y in moving_pawns:
            paths = self.get_pawn_move_path(x, y)
            moves += paths
        return moves

    def get_possible_pawn_captures(self, capturing_pawns: list[tuple[int, int]]):
        paths = []
        for x, y in capturing_pawns:
            piece = self.board[x][y].piece
            self.board[x][y].piece = None
            sol = []
            self.get_pawn_capture_path(x, y, [], [], sol)
            paths += sol
            self.board[x][y].piece = piece
        if not paths:
            return []
        max_len = len(max(paths, key=len))
        return [p for p in paths if len(p) == max_len]

    def get_pawn_capture_path(self, x, y, jumped_over: list[Cell], acc: list, solutions: list):
        acc.append((x, y))
        if self.can_pawn_capture(x, y, excluded_cells=jumped_over):
            directions = self.pawn_capture_directions(x, y, excluded_cells=jumped_over)
            for direction in directions:
                new_x, new_y, capture_x, capture_y = self.pawn_jump(x, y, direction)
                jumped_over_copy = jumped_over.copy()
                acc_copy = acc.copy()
                jumped_over_copy.append(self.board[capture_x][capture_y])
                self.get_pawn_capture_path(new_x, new_y, jumped_over_copy, acc_copy, solutions)
        else:
            solutions.append(acc)

    def get_pawn_move_path(self, x, y):
        moves = []
        if self.current_colour == self.WHITE:
            if self.is_pawn_move_possible(x, y, (1, -1)):
                moves.append([(x, y), (x + 1, y - 1)])
            if self.is_pawn_move_possible(x, y, (1, 1)):
                moves.append([(x, y), (x + 1, y + 1)])
        else:
            if self.is_pawn_move_possible(x, y, (-1, -1)):
                moves.append([(x, y), (x - 1, y - 1)])
            if self.is_pawn_move_possible(x, y, (-1, 1)):
                moves.append([(x, y), (x - 1, y + 1)])
        return moves

    def get_possible_queen_moves(self, moving_queens: list[tuple[int, int]]):
        moves = []
        for qx, qy in moving_queens:
            moves += self.get_queen_move_path(qx, qy)
        return moves

    def get_possible_queen_captures(self, capturing_queens: list[tuple[int, int]]):
        paths = []
        for x, y in capturing_queens:
            piece = self.board[x][y].piece
            self.board[x][y].piece = None
            sol = []
            self.get_queen_capture_path(x, y, [], [], sol)
            paths += sol
            self.board[x][y].piece = piece
        if not paths:
            return []
        max_len = len(max(paths, key=len))
        return [p for p in paths if len(p) == max_len]

    def get_queen_move_path(self, x, y):
        moves = []
        diagonals = [self.__diagonal(x, y, direction) for direction in self.__directions]
        for diagonal in diagonals:
            obstacle_found = False
            for dx, dy in diagonal:
                if not obstacle_found:
                    if self.board[dx][dy].is_empty:
                        moves.append([(x, y), (dx, dy)])
                    else:
                        obstacle_found = True
        return moves

    def get_queen_capture_path(self, x, y, jumped_over: list[Cell], acc: list, solutions):
        acc.append((x, y))
        if self.can_queen_capture(x, y, excluded_cells=jumped_over):
            landing_spots = self.get_queen_landing_spots(x, y, excluded_cells=jumped_over)
            for enemy, spots in landing_spots:
                ex, ey = enemy
                jumped_over.append(self.board[ex][ey])
                for sx, sy in spots:
                    jumped_over_copy = jumped_over.copy()
                    acc_copy = acc.copy()
                    self.get_queen_capture_path(sx, sy, jumped_over_copy, acc_copy, solutions)
        else:
            solutions.append(acc)

    def get_queen_landing_spots(self, x, y, excluded_cells: list[Cell]):
        landing_pairs = []
        for direction in self.__directions:
            diagonal = self.__diagonal(x, y, direction)
            first_enemy = -1
            enemy = (-1, -1)
            second_enemy = -1
            for i, (dx, dy) in enumerate(diagonal):
                cell = self.board[dx][dy]
                if not cell.is_empty:
                    if cell.piece.colour != self.current_colour:
                        if cell not in excluded_cells:
                            if first_enemy == -1:
                                first_enemy = i
                                enemy = (dx, dy)
                            elif second_enemy == -1:
                                second_enemy = i
            if second_enemy == -1:
                second_enemy = len(diagonal)
            if first_enemy != -1:
                landing_pairs += [(enemy, diagonal[first_enemy + 1:second_enemy])]
        return landing_pairs

    # === CHECKS === -----------------------------------------------------------------------------------------
    def can_pawn_capture(self, x, y, excluded_cells=None) -> bool:
        for direction in self.__directions:
            if self.is_pawn_jump_possible(x, y, direction, excluded_cells=excluded_cells):
                return True
        return False

    def can_pawn_move(self, x, y):
        if self.current_colour == self.WHITE:
            return self.is_pawn_move_possible(x, y, (1, -1)) or self.is_pawn_move_possible(x, y, (1, 1))
        return self.is_pawn_move_possible(x, y, (-1, -1)) or self.is_pawn_move_possible(x, y, (-1, 1))

    def is_pawn_move_possible(self, x, y, direction):
        xd, yd = direction
        if self.__is_in_bounds(x + xd, y + yd):
            cell = self.board[x + xd][y + yd]
            return cell.is_empty
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
                if cell.piece.colour != self.current_colour:
                    if self.board[x + 2 * xd][y + 2 * yd].is_empty:
                        return True
        return False

    def is_queen_move_possible(self, x, y, direction):
        xd, yd = direction
        if self.__is_in_bounds(x + xd, y + yd):
            return self.board[x + xd][y + yd].is_empty
        return False

    def can_queen_move(self, x, y):
        for direction in self.__directions:
            if self.is_queen_move_possible(x, y, direction):
                return True
        return False


    def can_queen_capture(self, x, y, excluded_cells: list[Cell]) -> bool:
        for direction in self.__directions:
            if self.is_queen_jump_possible(x, y, direction, excluded_cells=excluded_cells):
                return True
        return False

    def __diagonal(self, queen_x, queen_y, direction) -> list[tuple[int, int]]:
        xd, yd = direction
        return [(queen_x + (i * xd), queen_y + (i * yd)) for i in range(1, 8)
                if self.__is_in_bounds(queen_x + (i * xd), queen_y + (i * yd))]

    def is_queen_jump_possible(self, x, y, direction, excluded_cells=None):
        xd, yd = direction
        diagonal = self.__diagonal(x, y, direction)
        for land_x, land_y in diagonal[:-1]:
            cell = self.board[land_x][land_y]
            if excluded_cells is not None:
                if cell in excluded_cells:
                    return False
            if not cell.is_empty:
                if self.board[land_x + xd][land_y + yd].is_empty:
                    if self.current_colour != cell.piece.colour:
                        return True
        return False

    # === JUMPS / CAPTURES UTILS === ------------------------------------------------------------------
    def pawn_jump(self, x_start: int, y_start: int, direction: tuple[int, int]):
        xd, yd = direction
        return x_start + 2 * xd, y_start + 2 * yd, x_start + xd, y_start + yd

    def pawn_capture_directions(self, x, y, excluded_cells=None) -> list[tuple[int, int]]:
        ret = []
        for direction in self.__directions:
            if self.is_pawn_jump_possible(x, y, direction, excluded_cells=excluded_cells):
                ret.append(direction)
        return ret

    def __is_in_bounds(self, x, y):
        return 0 <= x < len(self.board) and 0 <= y < len(self.board)

    def __get_captured_enemy(self, start_x, start_y, land_x, land_y):
        xd = 1 if land_x > start_x else -1
        yd = 1 if land_y > start_y else -1
        diagonal = self.__diagonal(start_x, start_y, (xd, yd))
        for diag_x, diag_y in diagonal:
            if not self.board[diag_x][diag_y].is_empty:
                if self.board[diag_x][diag_y].piece.colour != self.current_colour:
                    return diag_x, diag_y

    def __get_longest_captures(self, pawn_captures, queen_captures):
        captures = pawn_captures + queen_captures
        max_len = len(max(captures, key=len))
        return [c for c in captures if len(c) == max_len]


    # === UTILS === -----------------------------------------------------------------------------------
    def print_board(self):
        print('   A  B  C  D  E  F  G  H ')
        for i, line in enumerate(self.board):
            s = f'{i + 1} '
            for j, cell in enumerate(line):
                if i % 2 == 0:
                    if j % 2 == 0:
                        if (i, j) in self.last_move:
                            s += f'{Color.BG.YELLOW} {cell.marker}{Color.BG.YELLOW} {Color.END}'
                        else:
                            s += f' {cell.marker} '
                    else:
                        s += f'{Color.BG.WHITE} {cell.marker} {Color.END}'
                else:
                    if j % 2 == 0:
                        s += f'{Color.BG.WHITE} {cell.marker} {Color.END}'
                    else:
                        if (i, j) in self.last_move:
                            s += f'{Color.BG.YELLOW} {cell.marker}{Color.BG.YELLOW} {Color.END}'
                        else:
                            s += f' {cell.marker} '
            s += f' {i + 1}'
            if i == 0:
                s += f'  {Color.FG.WHITE}{self.player1.name} {self.white_count}{Color.END}'
            if i == 1:
                s += f'  {Color.FG.BLACK}{self.player2.name} {self.black_count}{Color.END}'
            print(s)
        print('   A  B  C  D  E  F  G  H ')

    @staticmethod
    def decode_alias(alias: str):
        return first_index('12345678', lambda x: x == alias[1]), first_index('ABCDEFGH', lambda x: x == alias[0])

    @staticmethod
    def alias_from_coordinates(coordinates):
        return 'ABCDEFGH'[coordinates[1]] + '12345678'[coordinates[0]]



