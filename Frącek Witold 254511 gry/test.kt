

fun main(args: Array<String>) {
    val b = Board().empty()
    b.board[7][3].piece = Queen(CheckersColour.WHITE, Colour.FG.WHITE)
    b.board[5][5].piece = Pawn(CheckersColour.BLACK, Colour.FG.BLACK)
    b.board[4][6].piece = Pawn(CheckersColour.BLACK, Colour.FG.BLACK)
    println(CheckersController.canQueenCapture(b, Pair(7, 3), CheckersColour.WHITE))
    CheckersController.printBoard(b, listOf())

//    println(CheckersController.isQueenJumpPossible(b, Pair(7, 3), Pair(1, 1), CheckersColour.WHITE))
    println(CheckersController.isQueenJumpPossible(b, Pair(7, 3), Pair(-1, 1), CheckersColour.WHITE))
//    println(CheckersController.isQueenJumpPossible(b, Pair(7, 3), Pair(1, -1), CheckersColour.WHITE))
//    println(CheckersController.isQueenJumpPossible(b, Pair(7, 3), Pair(-1, -1), CheckersColour.WHITE))
}