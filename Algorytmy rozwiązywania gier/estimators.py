from pieces import Piece, Pawn, Queen


class Estimator:
    def __call__(self, board, player) -> int:
        return 0


class BasicEstimator(Estimator):

    def __call__(self, board, player):
        score = 0
        for i, line in enumerate(board):
            for j, cell in enumerate(line):
                if not cell.is_empty:
                    if cell.piece.colour == player.colour:
                        if isinstance(cell.piece, Pawn):
                            score += 1
                        elif isinstance(cell.piece, Queen):
                            score += 3
        return score


