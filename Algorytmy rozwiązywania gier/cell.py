from pieces import Piece


class Cell:
    def __init__(self, alias: str, piece=None):
        self.piece: Piece = piece
        self.alias: str = alias

    def __eq__(self, other) -> bool:
        return self.alias == other.alias

    def __repr__(self):
        if self.piece is None:
            return f'{self.alias}\nPiece: None'
        return f'{self.alias}\nPiece: {self.piece}'

    @property
    def marker(self):
        if self.piece is None:
            return ' '
        return self.piece.marker




