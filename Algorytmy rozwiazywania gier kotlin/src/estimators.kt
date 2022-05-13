import kotlin.math.max

abstract class Estimator {
    open operator fun invoke(board: Board, maximisingColour: CheckersColour, checkForEndgame: Boolean = false): Int {
        return 0
    }
}

class CountEstimator(private val pawnWeight: Double = 1.0, private val queenWeight: Double = 3.0): Estimator() {
    override operator fun invoke(board: Board, maximisingColour: CheckersColour, checkForEndgame: Boolean): Int {
        if(checkForEndgame) {
            if(CheckersController.hasGameEnded(board, CheckersColour.WHITE)) {
                return when(maximisingColour) {
                    CheckersColour.WHITE -> Int.MIN_VALUE
                    CheckersColour.BLACK -> Int.MAX_VALUE
                }
            } else if(CheckersController.hasGameEnded(board, CheckersColour.BLACK)) {
                return when(maximisingColour) {
                    CheckersColour.WHITE -> Int.MAX_VALUE
                    CheckersColour.BLACK -> Int.MIN_VALUE
                }
            }
        }
        var score = 0.0
        for(line in board.board) {
            for(cell in line) {
                if(!cell.isEmpty) {
                    val sign = if(cell.piece?.colour == maximisingColour) {
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

class AreaEstimator(private val outerZone: Int = 3,
                    private val middleZone: Int = 2,
                    private val innerZone: Int = 1,
                    private val queenWeight: Int = 3): Estimator() {
    private val weights = getZoneWeighs()

    override fun invoke(board: Board, maximisingColour: CheckersColour, checkForEndgame: Boolean): Int {
        if(checkForEndgame) {
            if(CheckersController.hasGameEnded(board, CheckersColour.WHITE)) {
                return when(maximisingColour) {
                    CheckersColour.WHITE -> Int.MIN_VALUE
                    CheckersColour.BLACK -> Int.MAX_VALUE
                }
            } else if(CheckersController.hasGameEnded(board, CheckersColour.BLACK)) {
                return when(maximisingColour) {
                    CheckersColour.WHITE -> Int.MAX_VALUE
                    CheckersColour.BLACK -> Int.MIN_VALUE
                }
            }
        }
        var score = 0
        var whiteCount = 0
        var blackCount = 0
        for((i, line) in board.board.withIndex()) {
            for((j, cell) in line.withIndex()) {
                if(!cell.isEmpty) {
                    val mul = if(cell.piece?.colour == maximisingColour) {
                        1
                    } else {
                        -1
                    }
                    if(cell.piece?.colour == CheckersColour.WHITE) {
                        whiteCount += 1
                    } else {
                        blackCount += 1
                    }
                    if(cell.piece is Queen) {
                        score += queenWeight * mul
                    } else {
                        score += weights[i][j] * mul
                    }
                }
            }
        }
        score += if(maximisingColour == CheckersColour.WHITE) {
            (whiteCount - blackCount) * 5
        } else {
            (blackCount - whiteCount) * 5
        }
        return score
    }

    private fun getZoneWeighs(): List<List<Int>> {
        val weightZone = mutableListOf<List<Int>>()
        for(i in 0 until 8) {
            val weights = mutableListOf<Int>()
            for(j in 0 until 8) {
                if((i == 0) or (j == 7) or (i == 7) or (j == 0)) {
                    weights.add(outerZone)
                } else if((i > 1) and (i < 6) and (j > 1) and (j < 6)) {
                    weights.add(innerZone)
                } else {
                    weights.add(middleZone)
                }
            }
            weightZone.add(weights)
        }
//        for(row in weightZone) {
//            println(row)
//        }
        return weightZone
    }
}