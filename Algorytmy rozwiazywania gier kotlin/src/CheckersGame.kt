class CheckersGame(val player1: Player, val player2: Player, pawnRows: Int, startColour: CheckersColour = CheckersColour.WHITE) {
    var board = Board(pawnRows)
    private var lastMove = mutableListOf<Pair<Int, Int>>()
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
            val pawnCaptures = CheckersController.getPossiblePawnCaptures(board, captures.first, currentColour)
            val queenCaptures = CheckersController.getPossibleQueenCaptures(board, captures.second, currentColour)
            val longestCaptures = CheckersController.getLongestCaptures(pawnCaptures, queenCaptures)
            val pos = currentPlayer.capture(longestCaptures, board)
            val playerChoice = longestCaptures[pos]
            lastMove = playerChoice.map{ it.startPair }.toMutableList()
            lastMove.add(playerChoice[playerChoice.size - 1].endPair)
            board = CheckersController.executeCapture(board, playerChoice)
        } else {
            val moves = CheckersController.getMovingPieces(board, pieces, currentColour)
            val pawnMoves = CheckersController.getPossiblePawnMoves(board, moves.first, currentColour)
            val queenMoves = CheckersController.getPossibleQueenMoves(board, moves.second)
            val allMoves = mutableListOf<Move>()
            allMoves.addAll(pawnMoves)
            allMoves.addAll(queenMoves)
            val pos = currentPlayer.move(allMoves, board)
            val playerChoice = allMoves[pos]
            lastMove.add(playerChoice.startPair)
            lastMove.add(playerChoice.endPair)
            board = CheckersController.executeMove(board, playerChoice)
        }
        board = CheckersController.promoteToQueen(board)
        switchPlayer()
    }

}