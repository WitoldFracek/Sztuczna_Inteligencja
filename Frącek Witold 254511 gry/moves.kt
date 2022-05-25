

open class Move(val xStart: Int,
           val yStart: Int,
           val xEnd: Int,
           val yEnd: Int
           ) {

    val startPair: Pair<Int, Int>
        get() = Pair(xStart, yStart)

    val endPair: Pair<Int, Int>
        get() = Pair(xEnd, yEnd)

    override fun toString(): String {
        return "${CheckersController.aliasFromCoordinates(xStart, yStart)}-${CheckersController.aliasFromCoordinates(xEnd, yEnd)}"
    }
}

class Jump(xStart: Int,
           yStart: Int,
           xEnd: Int,
           yEnd: Int,
           val xCapture: Int,
           val yCapture: Int
           ): Move(xStart, yStart, xEnd, yEnd) {
               val capturePair: Pair<Int, Int>
               get() = Pair(xCapture, yCapture)
           }