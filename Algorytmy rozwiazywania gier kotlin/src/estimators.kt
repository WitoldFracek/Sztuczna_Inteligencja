

open class Estimator {
    open operator fun invoke(board: Board, colour: CheckersColour): Int {
        return 0
    }
}

open class CountEstimator(private val pawnWeight: Double = 1.0, private val queenWeight: Double = 3.0): Estimator() {
    override operator fun invoke(board: Board, colour: CheckersColour): Int {
        var score = 0.0
        for(line in board.board) {
            for(cell in line) {
                if(!cell.isEmpty) {
                    val sign = if(cell.piece?.colour == CheckersColour.WHITE) {
                        1
                    } else {
                        -1
                    }

                    if(cell.piece is Pawn) {
                        score += sign * pawnWeight
                    } else if(cell.piece is Queen) {
                        score += sign * queenWeight
                    }
                }
            }
        }
        return score.toInt()
    }
}