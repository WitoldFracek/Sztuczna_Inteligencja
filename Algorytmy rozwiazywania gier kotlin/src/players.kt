import java.lang.Integer.min
import java.lang.System.currentTimeMillis
import kotlin.math.max

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
        val maximising = if(colour == CheckersColour.WHITE) { true } else { false }
        var bestEval = if(maximising) { Int.MIN_VALUE } else { Int.MAX_VALUE }
        println(bestEval)
        val startTime = currentTimeMillis()
        for((i, move) in possibleMoves.withIndex()) {
            var newBoard = board.copy()
            newBoard = CheckersController.executeMove(newBoard, move)
            val estimator = minmax(newBoard, searchDepth, colour, maximising)
            if(maximising and (estimator > bestEval)) {
                bestEval = estimator
                bestMoves.clear()
                bestMoves.add(i)
            } else if(!maximising and (estimator < bestEval)) {
                bestEval = estimator
                bestMoves.clear()
                bestMoves.add(i)
            } else if(estimator == bestEval) {
                bestMoves.add(i)
            }
        }
        val endTime = currentTimeMillis()
        println("Computed in ${(endTime - startTime) / 1000}s")
        return bestMoves[(Math.random() * bestMoves.size).toInt()]
    }

    override fun capture(possibleCaptures: List<List<Jump>>, board: Board): Int {
        val bestCaptures = mutableListOf<Int>()
        val maximising = if(colour == CheckersColour.WHITE) { true } else { false }
        var bestEval = if(maximising) { Int.MIN_VALUE } else { Int.MAX_VALUE }
        val startTime = currentTimeMillis()
        for((i, captureList) in possibleCaptures.withIndex()) {
            var newBoard = board.copy()
            newBoard = CheckersController.executeCapture(newBoard, captureList)
            val estimator = minmax(newBoard, searchDepth, colour, maximising)
            if(maximising and (estimator > bestEval)) {
                bestEval = estimator
                bestCaptures.clear()
                bestCaptures.add(i)
            } else if(!maximising and (estimator < bestEval)) {
                bestEval = estimator
                bestCaptures.clear()
                bestCaptures.add(i)
            } else if(estimator == bestEval) {
                bestCaptures.add(i)
            }
        }
        val endTime = currentTimeMillis()
        println("Computed in ${(endTime - startTime) / 1000}s")
        return bestCaptures[(Math.random() * bestCaptures.size).toInt()]
    }

    fun minmax(board: Board, depth: Int, colour: CheckersColour, maximising: Boolean): Int {
        if(CheckersController.hasGameEnded(board, colour)) {
            return if(maximising) {
                Int.MIN_VALUE + searchDepth - depth
            } else {
                Int.MAX_VALUE - searchDepth + depth
            }
        }
        if(depth <= 0) {
            return estimator(board, colour)
        }
        val allCaptures = CheckersController.getAllCaptures(board, colour)
        if(allCaptures.isNotEmpty()) {
            if(maximising) {
                var maxEval = Int.MIN_VALUE
                for(capture in allCaptures) {
                    var newBoard = board.copy()
                    newBoard = CheckersController.executeCapture(newBoard, capture)
                    val estimation = minmax(newBoard, depth - 1, colour.oppositeColour(), false)
                    maxEval = max(maxEval, estimation)
                }
                return maxEval
            } else {
                var minEval = Int.MAX_VALUE
                for(capture in allCaptures) {
                    var newBoard = board.copy()
                    newBoard = CheckersController.executeCapture(newBoard, capture)
                    val estimation = minmax(newBoard, depth - 1, colour.oppositeColour(), true)
                    minEval = min(minEval, estimation)
                }
                return minEval
            }
        }
        val allMoves = CheckersController.getAllMoves(board, colour)
        if(maximising) {
            var maxEval = Int.MIN_VALUE
            for(move in allMoves) {
                var newBoard = board.copy()
                newBoard = CheckersController.executeMove(newBoard, move)
                val estimation = minmax(newBoard, depth - 1, colour.oppositeColour(), false)
                maxEval = max(maxEval, estimation)
            }
            return maxEval
        } else {
            var minEval = Int.MAX_VALUE
            for(move in allMoves) {
                var newBoard = board.copy()
                newBoard = CheckersController.executeMove(newBoard, move)
                val estimation = minmax(newBoard, depth - 1, colour.oppositeColour(), true)
                minEval = min(minEval, estimation)
            }
            return minEval
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