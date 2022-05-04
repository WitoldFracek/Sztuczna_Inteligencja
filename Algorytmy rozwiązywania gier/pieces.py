from colors import Color


class Piece:
    def __init__(self, colour: str, console_colour: str):
        self.colour = colour
        self.console_colour = console_colour

    @property
    def marker(self):
        return f'{self.console_colour}●{Color.END}'

    def __repr__(self):
        return f'{self.__class__.__name__} {self.colour}'


class Queen(Piece):
    def __init__(self, colour: str, console_colour: str):
        Piece.__init__(self, colour, console_colour)

    @property
    def marker(self):
        return f'{self.console_colour}Q{Color.END}'


class Pawn(Piece):
    def __init__(self, colour: str, console_colour: str):
        Piece.__init__(self, colour, console_colour)

    def transform_to_queen(self) -> Queen: #promote
        return Queen(self.colour, self.console_colour)




