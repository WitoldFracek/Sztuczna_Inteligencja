from colors import Color


class Piece:
    def __init__(self, colour: str, console_colour: str):
        self.colour = colour
        self.console_colour = console_colour

    @property
    def marker(self):
        return f'{self.console_colour}●{Color.END}'
        # if self.colour == self.WHITE:
        #     return '●'
        # return f'{Color.FG.BLACK}●{Color.END}'

    def __repr__(self):
        return f'{self.__class__.__name__} {self.colour}'


class Queen(Piece):
    def __init__(self, colour: str, console_colour: str):
        Piece.__init__(self, colour, console_colour)


class Pawn(Piece):
    def __init__(self, colour: str, console_colour: str):
        Piece.__init__(self, colour, console_colour)

    def transform_to_queen(self) -> Queen:
        return Queen(self.colour, self.console_colour)




