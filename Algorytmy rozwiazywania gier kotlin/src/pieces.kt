open class Piece(val colour: CheckersColour, protected val consoleColour: String) {
    open val marker: String
        get() = "$consoleColour●${Colour.END}"
}

class Queen(colour: CheckersColour, consoleColour: String): Piece(colour, consoleColour) {
    override val marker
        get() = "${consoleColour}Q${Colour.END}"
}

class Pawn(colour: CheckersColour, consoleColour: String): Piece(colour, consoleColour) {
    fun promote(): Queen {
        return Queen(colour, consoleColour)
    }
}
