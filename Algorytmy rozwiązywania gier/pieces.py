from colors import Color


class Piece:

    WHITE = 'w'
    BLACK = 'b'

    def __init__(self, colour: str):
        self.colour = colour

    @property
    def marker(self):
        if self.colour == self.WHITE:
            return '●'
        return f'{Color.FG.BLACK}●{Color.END}'

    def __repr__(self):
        return f'{self.__class__.__name__} {self.colour}'


class Queen(Piece):
    def __init__(self, colour: str):
        Piece.__init__(self, colour)


class Pawn(Piece):
    def __init__(self, colour: str):
        Piece.__init__(self, colour)

    def transform_to_queen(self) -> Queen:
        return Queen(self.colour)




