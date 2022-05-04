from colors import Color
import copy
from estimators import Estimator
from datetime import datetime


class Player:
    def __init__(self, colour, name=None):
        from checkers import Checkers
        if colour not in [Checkers.WHITE, Checkers.BLACK]:
            raise Exception(f'Invalid colour. Possible options are: {Checkers.WHITE} and {Checkers.BLACK}.')
        self.colour = colour
        self.name = self.__class__.__name__ + self.colour if name is None else name

    def move(self, possible_moves, board) -> int:
        return 0

    def capture(self, possible_moves, board) -> int:
        return 0


class Human(Player):
    def __init__(self, colour, name=None):
        Player.__init__(self, colour, name)

    def move(self, possible_moves, board) -> int:
        print(f'{Color.color(153, 255, 51)}{self.name} moves:{Color.END}')
        from checkers import Checkers as C
        for i, m in enumerate(possible_moves):
            start = C.alias_from_coordinates(m[0])
            end = C.alias_from_coordinates(m[1])
            print(f'{i}. From {start} to {end}')
        if not possible_moves:
            print('0. skip')
        is_correct = False
        pos = 0
        while not is_correct:
            try:
                pos = int(input('Move: '))
                if not possible_moves:
                    if pos == 0:
                        is_correct = True
                        pos = -1
                elif 0 <= pos < len(possible_moves):
                    is_correct = True
                else:
                    print(f'Invalid input. Type number between 0 and {len(possible_moves) - 1}')
            except ValueError:
                print(f'Invalid input. Type number between 0 and {len(possible_moves) - 1}')
        return pos

    def capture(self, possible_captures, board) -> int:
        from checkers import Checkers as C
        print(f'{Color.color(255, 128, 0)}{self.name} captures:{Color.END}')
        for i, m in enumerate(possible_captures):
            start = C.alias_from_coordinates(m[0])
            path = [C.alias_from_coordinates(coor) for coor in m[1:]]
            print(f'{i}. From {start} over {path}')
        is_correct = False
        pos = 0
        while not is_correct:
            try:
                pos = int(input('Move: '))
                if 0 <= pos < len(possible_captures):
                    is_correct = True
                else:
                    print(f'Invalid input. Type number between 0 and {len(possible_captures) - 1}')
            except ValueError:
                print(f'Invalid input. Type number between 0 and {len(possible_captures) - 1}')
        return pos


class DummyBot(Player):

    NAMES = ['Niedorzeczny Bóbr',
             'Zgryźliwa Żmija',
             'Szybki Sebastian',
             'Pijany Olek',
             'Potężna Grochówka',
             'Smutny Marek',
             'Wesoły Romek']

    def __init__(self, colour, name=None):
        import random
        n = random.choice(self.NAMES) if name is None else name
        Player.__init__(self, colour, n)

    def move(self, possible_moves, board) -> int:
        if not possible_moves:
            return -1
        if len(possible_moves) == 1:
            return 0
        import random
        return random.randint(0, len(possible_moves) - 1)

    def capture(self, possible_moves, board) -> int:
        if not possible_moves:
            return -1
        if len(possible_moves) == 1:
            return 0
        import random
        return random.randint(0, len(possible_moves) - 1)


class MinMaxBot(Player):
    NAMES = ['Minimalistyczny Bóbr',
             'Optymalizacyjna Żmija',
             'Rekurencyjny Sebastian',
             'Maksujący Olek',
             'Zbijająca Grochówka',
             'Powolny Marek',
             'Drzewny Romek']

    MAX_VALUE = int(1e9)
    MIN_VALUE = int(-1e9)

    def __init__(self, colour, estimator: Estimator, search_depth=3, name=None, time_constraint=int(1e10)):
        import random
        from checkers import Checkers
        n = random.choice(self.NAMES) if name is None else name
        Player.__init__(self, colour, n)
        self.colour = colour
        self.opposite_colour = Checkers.WHITE if self.colour == Checkers.BLACK else Checkers.BLACK
        self.search_depth = search_depth
        self.estimator = estimator
        self.time_constraint = time_constraint

    def move(self, possible_moves, board) -> int:
        start = datetime.now()
        pos = self.get_best_move(possible_moves, board)
        end = datetime.now()
        print(f'Computed in {(end - start).seconds}s')
        return pos

    def capture(self, possible_moves, board) -> int:
        start = datetime.now()
        pos = self.get_best_capture(possible_moves, board)
        end = datetime.now()
        print(f'Computed in {(end - start).seconds}s')
        return pos

    def get_best_capture(self, possible_captures, board) -> int:
        if not possible_captures:
            return -1
        if len(possible_captures) == 1:
            return 0
        best_captures = []
        best_result = 0
        from checkers import Checkers
        for i, capture in enumerate(possible_captures):
            new_board = copy.deepcopy(board)
            new_board = Checkers.API.execute_capture(new_board, self, capture)
            start = datetime.now()
            estimation = self.min(new_board, self.search_depth)
            end = datetime.now()
            if not best_captures or estimation == best_result:
                best_captures.append(i)
            elif estimation > best_result:
                best_captures = [i]
                best_result = estimation
            if (end - start).seconds > self.time_constraint:
                break
        import random
        if not best_captures:
            return random.choice([i for i in range(len(possible_captures))])
        return random.choice(best_captures)

    def get_best_move(self, possible_moves, board) -> int:
        if not possible_moves:
            return -1
        if len(possible_moves) == 1:
            return 0
        best_moves = []
        best_result = 0
        from checkers import Checkers
        for i, move in enumerate(possible_moves):
            new_board = copy.deepcopy(board)
            new_board = Checkers.API.execute_move(new_board, self, move)
            start = datetime.now()
            estimation = self.min(new_board, self.search_depth)
            if not best_moves or estimation == best_result:
                best_moves.append(i)
            elif estimation > best_result:
                best_moves = [i]
                best_result = estimation
            end = datetime.now()
            if (end - start).seconds > self.time_constraint:
                break
        import random
        if not best_moves:
            return random.choice([i for i in range(len(possible_moves))])
        return random.choice(best_moves)

    def min(self, board, depth) -> int:
        current_estimation = self.estimator(board, Player(self.opposite_colour))
        if depth <= 0:
            return current_estimation
        from checkers import Checkers
        if Checkers.API.has_game_ended(board):
            return current_estimation
        possible_captures = Checkers.API.all_captures(board, Player(self.opposite_colour))
        possible_moves = Checkers.API.all_moves(board, Player(self.opposite_colour))
        if not possible_moves and not possible_captures:
            return self.MAX_VALUE
        worst_result = self.MAX_VALUE
        if possible_captures:
            for capture in possible_captures:
                new_board = copy.deepcopy(board)
                new_board = Checkers.API.execute_capture(new_board, Player(self.opposite_colour), capture)
                estimation = self.max(new_board, depth - 1)
                if worst_result > estimation:
                    worst_result = estimation
            return worst_result
        for move in possible_moves:
            new_board = copy.deepcopy(board)
            new_board = Checkers.API.execute_move(new_board, Player(self.opposite_colour), move)
            estimation = self.max(new_board, depth - 1)
            if worst_result > estimation:
                worst_result = estimation
        return worst_result

    def max(self, board, depth) -> int:
        current_estimation = self.estimator(board, self)
        if depth <= 0:
            return current_estimation
        from checkers import Checkers
        if Checkers.API.has_game_ended(board):
            return current_estimation
        possible_captures = Checkers.API.all_captures(board, self)
        possible_moves = Checkers.API.all_moves(board, self)
        if not possible_moves and not possible_captures:
            return self.MIN_VALUE
        best_result = self.MIN_VALUE
        if possible_captures:
            for capture in possible_captures:
                new_board = copy.deepcopy(board)
                new_board = Checkers.API.execute_capture(new_board, self, capture)
                estimation = self.min(new_board, depth - 1)
                if best_result < estimation:
                    best_result = estimation
            return best_result
        for move in possible_moves:
            new_board = copy.deepcopy(board)
            new_board = Checkers.API.execute_move(new_board, self, move)
            estimation = self.min(new_board, depth - 1)
            if best_result < estimation:
                best_result = estimation
        return best_result



