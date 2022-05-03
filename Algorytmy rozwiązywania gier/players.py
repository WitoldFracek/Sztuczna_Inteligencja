from colors import Color


class Player:
    def __init__(self, colour, name=None):
        self.colour = colour
        self.name = self.__class__.__name__ + self.colour if name is None else name

    def move(self, possible_moves, board) -> int:
        return 0

    def capture(self, possible_moves, board) -> int:
        return 0


class Human(Player):
    def __init__(self, colour, name):
        Player.__init__(self, colour, name)

    def move(self, possible_moves, board) -> int:
        print(f'{Color.color(153, 255, 51)}{self.name} moves:{Color.END}')
        from checkers import Checkers as C
        for i, m in enumerate(possible_moves):
            start = C.alias_from_coordinates(m[0])
            end = C.alias_from_coordinates(m[1])
            print(f'{i}. From {start} to {end}')
        is_correct = False
        pos = 0
        while not is_correct:
            try:
                pos = int(input('Move: '))
                if 0 <= pos < len(possible_moves):
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

