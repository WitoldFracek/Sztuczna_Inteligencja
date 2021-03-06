from pieces import Piece


class Cell:
    def __init__(self, alias: str, piece=None):
        self.piece: Piece = piece
        self.alias: str = alias

    def __eq__(self, other) -> bool:
        return self.alias == other.alias

    def __repr__(self):
        if self.piece is None:
            return f'{self.alias} Piece: None'
        return f'{self.alias} Piece: {self.piece}'

    @property
    def marker(self):
        if self.piece is None:
            return ' '
        return self.piece.marker

    @property
    def is_empty(self):
        return self.piece is None

    def is_opposite_colour(self, cell):
        # if cell.piece is None:
        #     return False
        return self.piece.colour != cell.piece.colour




