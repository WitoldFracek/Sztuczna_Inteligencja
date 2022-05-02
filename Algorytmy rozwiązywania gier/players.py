

class Player:
    def __init__(self, colour):
        self.colour = colour

    def move(self, possible_moves, board) -> int:
        return 0


class Human(Player):
    def __init__(self, colour):
        Player.__init__(self, colour)

    def move(self, possible_moves, board) -> int:
        from checkers import Checkers as C
        for i, m in enumerate(possible_moves):
            start = C.alias_from_coordinates(m[0])
            path = [C.alias_from_coordinates(coor) for coor in m[1:]]
            print(f'{i}. Start: {start} to {path}')
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

