import java.lang.Integer.min
import java.lang.System.currentTimeMillis
import kotlin.math.max
import kotlin.reflect.jvm.internal.impl.util.Check

fun <T> getCorrectInput(list: List<T>): Int {
    var isCorrect = false
    var pos = 0
    while(!isCorrect) {
        try {
            pos = readLine()!!.toInt()
            if(pos >= 0 && pos < list.size) {
                isCorrect = true
            } else {
                println("Invalid input. Type number between 0 and ${list.size - 1}")
            }
        } catch (e: Exception) {
            println("Invalid input. Type number between 0 and ${list.size - 1}")
        }
    }
    return pos
}


open class Player(open val name: String = "${Player::class.simpleName}") {

    lateinit var colour: CheckersColour

    open fun move(possibleMoves: List<Move>, board: Board): Int {
        return 0
    }

    open fun capture(possibleCaptures: List<List<Jump>>, board: Board): Int {
        return 0
    }

    override fun toString(): String {
        return name
    }
}

class Human(name: String): Player(name) {
    override fun move(possibleMoves: List<Move>, board: Board): Int {
        println("${Colour.colour(153, 255, 51)}${name} moves:${Colour.END}")
        for((i, move) in possibleMoves.withIndex()){
            val start = CheckersController.aliasFromCoordinates(move.xStart, move.yStart)
            val end = CheckersController.aliasFromCoordinates(move.xEnd, move.yEnd)
            println("${i}. From $start to $end")
        }
        return getCorrectInput(possibleMoves)
    }

    override fun capture(possibleCaptures: List<List<Jump>>, board: Board): Int {
        println("${Colour.colour(153, 255, 51)}${name} moves:${Colour.END}")
        for((i, jumps) in possibleCaptures.withIndex()) {
            val startJump = jumps[0]
            val start = CheckersController.aliasFromCoordinates(startJump.xStart, startJump.yStart)
            var path = ""
            for(jump in jumps) {
                path += " -> "
                path += CheckersController.aliasFromCoordinates(jump.xEnd, jump.yEnd)
            }
            println("${i}. From $start $path")
        }
        return getCorrectInput(possibleCaptures)
    }
}

class DummyBot(name: String=""): Player(name) {

    override val name = if(name == "") { NAMES[(Math.random() * NAMES.size).toInt()] } else { name }

    override fun move(possibleMoves: List<Move>, board: Board): Int {
        return (Math.random() * possibleMoves.size).toInt()
    }

    override fun capture(possibleCaptures: List<List<Jump>>, board: Board): Int {
        return (Math.random() * possibleCaptures.size).toInt()
    }

    companion object {
        private val NAMES = arrayOf(
            "Niedorzeczny Bóbr",
            "Zgryźliwa Żmija",
            "Szybki Sebastian",
            "Pijany Olek",
            "Potężna Grochówka",
            "Smutny Marek",
            "Wesoły Romek"
        )
    }

}

class MinMaxBot(name:String, val searchDepth:Int, val estimator: Estimator): Player(name) {
    override val name = if(name == "") { NAMES[(Math.random() * NAMES.size).toInt()] } else { name }

    constructor(estimator: Estimator, searchDepth: Int=3): this("", searchDepth, estimator)

    override fun move(possibleMoves: List<Move>, board: Board): Int {
        val bestMoves = mutableListOf<Int>()
        var bestEval = Int.MIN_VALUE
        val startTime = currentTimeMillis()
        for((i, move) in possibleMoves.withIndex()) {
            var newBoard = board.copy()
            newBoard = CheckersController.executeMove(newBoard, move)
            val eval = minmax(newBoard, searchDepth - 1, this.colour.oppositeColour(), false)
            if(eval > bestEval) {
                bestEval = eval
                bestMoves.clear()
                bestMoves.add(i)
            } else if(eval == bestEval) {
                bestMoves.add(i)
            }
        }
        val endTime = currentTimeMillis()
        println("Computed in ${(endTime - startTime) / 1000}s")
        println("Best estimations for $colour is $bestEval")
        return bestMoves[(Math.random() * bestMoves.size).toInt()]
    }

    override fun capture(possibleCaptures: List<List<Jump>>, board: Board): Int {
        val bestCaptures = mutableListOf<Int>()
        var bestEval = Int.MIN_VALUE
        val startTime = currentTimeMillis()
        for((i, captureList) in possibleCaptures.withIndex()) {
            var newBoard = board.copy()
            newBoard = CheckersController.executeCapture(newBoard, captureList)
            val eval = minmax(newBoard, searchDepth - 1, this.colour.oppositeColour(), false)
            if(eval > bestEval) {
                bestEval = eval
                bestCaptures.clear()
                bestCaptures.add(i)
            } else if(eval == bestEval) {
                bestCaptures.add(i)
            }
        }
        val endTime = currentTimeMillis()
        println("Computed in ${(endTime - startTime) / 1000}s")
        println("Best estimations for $colour is $bestEval")
        return bestCaptures[(Math.random() * bestCaptures.size).toInt()]
    }

    fun minmax(board: Board, depth: Int, currentColour: CheckersColour, maximising: Boolean): Int {
        if(depth == 0) {
            return estimator(board, this.colour)
        }
        when(currentColour) {
            CheckersColour.WHITE -> {
                if(board.idleWhiteMoves > board.idleMoves) {
                    return estimator(board, this.colour)
                }
            }
            CheckersColour.BLACK -> {
                if(board.idleBlackMoves > board.idleMoves) {
                    return estimator(board, this.colour)
                }
            }
        }
        val allCaptures = CheckersController.getAllCaptures(board, currentColour)
        if(allCaptures.isNotEmpty()) {
            return minmaxJumps(board, allCaptures, depth, currentColour, maximising)
        }
        val allMoves = CheckersController.getAllMoves(board, currentColour)
        if(allMoves.isNotEmpty()) {
            return minmaxMoves(board, allMoves, depth, currentColour, maximising)
        }
        val currentEstimation = estimator(board, this.colour, true)
        if(maximising) {
            return currentEstimation + searchDepth - depth
        } else {
            return currentEstimation - searchDepth + depth
        }
    }

    fun minmaxMoves(board: Board, moves: List<Move>, depth: Int, currentColour: CheckersColour, maximising: Boolean): Int {
        if(maximising) {
            var currentBest = Int.MIN_VALUE
            for(move in moves) {
                var newBoard = board.copy()
                newBoard = CheckersController.executeMove(newBoard, move)
                val est = minmax(newBoard, depth - 1, currentColour.oppositeColour(), false)
                if(est > currentBest) {
                    currentBest = est
                }
            }
            return currentBest
        } else {
            var currentWorst = Int.MAX_VALUE
            for(move in moves) {
                var newBoard = board.copy()
                newBoard = CheckersController.executeMove(newBoard, move)
                val est = minmax(newBoard, depth -1, currentColour.oppositeColour(), true)
                if(est < currentWorst) {
                    currentWorst = est
                }
            }
            return currentWorst
        }
    }

    fun minmaxJumps(board: Board, possibleJumps:List<List<Jump>>, depth: Int, currentColour: CheckersColour, maximising: Boolean): Int {
        if(maximising) {
            var currentBest = Int.MIN_VALUE
            for(jumps in possibleJumps) {
                var newBoard = board.copy()
                newBoard = CheckersController.executeCapture(newBoard, jumps)
                val est = minmax(newBoard, depth - 1, currentColour.oppositeColour(), false)
                if(est > currentBest) {
                    currentBest = est
                }
            }
            return currentBest
        } else {
            var currentWorst = Int.MAX_VALUE
            for(jumps in possibleJumps) {
                var newBoard = board.copy()
                newBoard = CheckersController.executeCapture(newBoard, jumps)
                val est = minmax(newBoard, depth - 1, currentColour.oppositeColour(), true)
                if(est < currentWorst) {
                    currentWorst = est
                }
            }
            return currentWorst
        }
    }

    companion object {
        private val NAMES = arrayOf(
            "Niedorzeczny Bóbr",
            "Zgryźliwa Żmija",
            "Szybki Sebastian",
            "Pijany Olek",
            "Potężna Grochówka",
            "Smutny Marek",
            "Wesoły Romek"
        )
    }
}

class AlphaBetaBot(name:String, val searchDepth:Int, val estimator: Estimator): Player(name) {
    override val name = if(name == "") { NAMES[(Math.random() * NAMES.size).toInt()] } else { name }

    constructor(estimator: Estimator, searchDepth: Int=3): this("", searchDepth, estimator)

    override fun move(possibleMoves: List<Move>, board: Board): Int {
        val bestMoves = mutableListOf<Int>()
        var bestEval = Int.MIN_VALUE
        val startTime = currentTimeMillis()
        for((i, move) in possibleMoves.withIndex()) {
            var newBoard = board.copy()
            newBoard = CheckersController.executeMove(newBoard, move)
            val eval = alphabeta(newBoard, searchDepth - 1, this.colour.oppositeColour(), false, Int.MIN_VALUE, Int.MAX_VALUE)
            if(eval > bestEval) {
                bestEval = eval
                bestMoves.clear()
                bestMoves.add(i)
            } else if(eval == bestEval) {
                bestMoves.add(i)
            }
        }
        val endTime = currentTimeMillis()
        println("Computed in ${(endTime - startTime) / 1000}s")
        println("Best estimations for $colour is $bestEval")
        return bestMoves[(Math.random() * bestMoves.size).toInt()]
    }

    override fun capture(possibleCaptures: List<List<Jump>>, board: Board): Int {
        val bestCaptures = mutableListOf<Int>()
        var bestEval = Int.MIN_VALUE
        val startTime = currentTimeMillis()
        for((i, captureList) in possibleCaptures.withIndex()) {
            var newBoard = board.copy()
            newBoard = CheckersController.executeCapture(newBoard, captureList)
            val eval = alphabeta(newBoard, searchDepth - 1, this.colour.oppositeColour(), false, Int.MIN_VALUE, Int.MAX_VALUE)
            if(eval > bestEval) {
                bestEval = eval
                bestCaptures.clear()
                bestCaptures.add(i)
            } else if(eval == bestEval) {
                bestCaptures.add(i)
            }
        }
        val endTime = currentTimeMillis()
        println("Computed in ${(endTime - startTime) / 1000}s")
        println("Best estimations for $colour is $bestEval")
        return bestCaptures[(Math.random() * bestCaptures.size).toInt()]
    }

    fun alphabeta(board: Board, depth: Int, currentColour: CheckersColour, maximising: Boolean, alpha: Int, beta: Int): Int {
        if(depth == 0) {
            return estimator(board, this.colour)
        }
        when(currentColour) {
            CheckersColour.WHITE -> {
                if(board.idleWhiteMoves > board.idleMoves) {
                    return estimator(board, this.colour)
                }
            }
            CheckersColour.BLACK -> {
                if(board.idleBlackMoves > board.idleMoves) {
                    return estimator(board, this.colour)
                }
            }
        }
        val allCaptures = CheckersController.getAllCaptures(board, currentColour)
        if(allCaptures.isNotEmpty()) {
            return alphaBetaJumps(board, allCaptures, depth, currentColour, maximising, alpha, beta)
        }
        val allMoves = CheckersController.getAllMoves(board, currentColour)
        if(allMoves.isNotEmpty()) {
            return alphaBetaMoves(board, allMoves, depth, currentColour, maximising, alpha, beta)
        }
        val currentEstimation = estimator(board, this.colour, true)
        if(maximising) {
            return currentEstimation + searchDepth - depth
        } else {
            return currentEstimation - searchDepth + depth
        }
    }

    fun alphaBetaMoves(board: Board, moves: List<Move>, depth: Int, currentColour: CheckersColour, maximising: Boolean, alpha: Int, beta: Int): Int {
        if(maximising) {
            var currentBest = Int.MIN_VALUE
            var newAlpha = currentBest
            for(move in moves) {
                var newBoard = board.copy()
                newBoard = CheckersController.executeMove(newBoard, move)
                val est = alphabeta(newBoard, depth - 1, currentColour.oppositeColour(), false, newAlpha, beta)
                if(est > currentBest) {
                    currentBest = est
                }
                if(est > newAlpha) {
                    newAlpha = est
                }
                if(beta <= newAlpha) {
                    break
                }
            }
            return currentBest
        } else {
            var currentWorst = Int.MAX_VALUE
            var newBeta = currentWorst
            for(move in moves) {
                var newBoard = board.copy()
                newBoard = CheckersController.executeMove(newBoard, move)
                val est = alphabeta(newBoard, depth -1, currentColour.oppositeColour(), true, alpha, newBeta)
                if(est < currentWorst) {
                    currentWorst = est
                }
                if(est < newBeta) {
                    newBeta = est
                }
                if(newBeta <= alpha) {
                    break
                }
            }
            return currentWorst
        }
    }

    fun alphaBetaJumps(board: Board, possibleJumps:List<List<Jump>>, depth: Int, currentColour: CheckersColour, maximising: Boolean, alpha: Int, beta: Int): Int {
        if(maximising) {
            var currentBest = Int.MIN_VALUE
            var newAlpha = currentBest
            for(jumps in possibleJumps) {
                var newBoard = board.copy()
                newBoard = CheckersController.executeCapture(newBoard, jumps)
                val est = alphabeta(newBoard, depth - 1, currentColour.oppositeColour(), false, newAlpha, beta)
                if(est > currentBest) {
                    currentBest = est
                }
                if(est > newAlpha) {
                    newAlpha = est
                }
                if(beta <= newAlpha) {
                    break
                }
            }
            return currentBest
        } else {
            var currentWorst = Int.MAX_VALUE
            var newBeta = currentWorst
            for(jumps in possibleJumps) {
                var newBoard = board.copy()
                newBoard = CheckersController.executeCapture(newBoard, jumps)
                val est = alphabeta(newBoard, depth - 1, currentColour.oppositeColour(), true, alpha, newBeta)
                if(est < currentWorst) {
                    currentWorst = est
                }
                if(est < newBeta) {
                    newBeta = est
                }
                if(newBeta <= alpha) {
                    break
                }
            }
            return currentWorst
        }
    }

    companion object {
        private val NAMES = arrayOf(
            "Niedorzeczny Bóbr",
            "Zgryźliwa Żmija",
            "Szybki Sebastian",
            "Pijany Olek",
            "Potężna Grochówka",
            "Smutny Marek",
            "Wesoły Romek"
        )
    }
}

fun main(args: Array<String>) {
    val h = Human("Witek")
    h.move(arrayListOf(Move(0, 0, 1, 1)), Board())
    h.capture(arrayListOf(arrayListOf(Jump(0, 0, 2, 2, 1, 1), Jump(2, 2, 4, 4, 3, 3))), Board())
}