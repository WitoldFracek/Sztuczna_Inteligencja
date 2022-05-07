class CheckersGame(val player1: Player, val player2: Player, pawnRows: Int, startColour: CheckersColour = CheckersColour.WHITE) {
    val board = Board(pawnRows)
    private var lastMove = listOf<Pair<Int, Int>>()
    private var currentPlayer = if(startColour == CheckersColour.WHITE) {
        player1
    } else {
        player2
    }
    private var currentColour = startColour
    private val directions = listOf(Pair(1, 1), Pair(1, -1), Pair(-1, 1), Pair(-1, -1))

}