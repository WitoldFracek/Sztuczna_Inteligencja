class CheckersGame(val player1: Player, val player2: Player, pawnRows: Int, startColour: CheckersColour = CheckersColour.WHITE) {
    var board = Board(pawnRows)
    private var lastMove = listOf<Pair<Int, Int>>()
    private var currentPlayer = if(startColour == CheckersColour.WHITE) {
        player1
    } else {
        player2
    }
    private var currentColour = startColour
    private val directions = listOf(Pair(1, 1), Pair(1, -1), Pair(-1, 1), Pair(-1, -1))

    fun play() {
        while(!CheckersController.hasGameEnded(board, currentColour)) {
            CheckersController.printBoard(board, lastMove, player1, player2)
            //one move
        }
        switchPlayer()
        CheckersController.printBoard(board, lastMove, player1, player2)
        println("Player $currentPlayer win!")
    }

    fun switchPlayer() {
        if(currentColour == CheckersColour.WHITE){
            currentPlayer = player2
            currentColour = CheckersColour.BLACK
        } else {
            currentPlayer = player1
            currentColour = CheckersColour.WHITE
        }
    }

    fun oneMove() {
        val pieces = CheckersController.getPieces(board, currentColour)
        val captures = CheckersController.getCapturingPieces(board, pieces, currentColour)
        if(captures.first.isNotEmpty() || captures.second.isNotEmpty()) {
            // getPossiblePawnCaptures
            // getPossibleQueenCaptures

            // executeCapture
        } else {
            val moves = CheckersController.getMovingPieces(board, pieces, currentColour)
            // getPossiblePawnMoves
            // getPossibleQueenMoves

            // executeMove
        }
        board = CheckersController.promoteToQueen(board)
        switchPlayer()
    }

}