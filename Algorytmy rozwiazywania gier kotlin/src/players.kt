
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

fun main(args: Array<String>) {
    val h = Human("Witek")
    h.move(arrayListOf(Move(0, 0, 1, 1)), Board())
    h.capture(arrayListOf(arrayListOf(Jump(0, 0, 2, 2, 1, 1), Jump(2, 2, 4, 4, 3, 3))), Board())
}