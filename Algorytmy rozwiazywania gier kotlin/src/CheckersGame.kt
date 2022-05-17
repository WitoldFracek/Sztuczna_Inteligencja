import java.lang.Integer.min

open class CheckersGame(val player1: Player, val player2: Player,
                        pawnRows: Int, startColour: CheckersColour = CheckersColour.WHITE,
                        allowFirstRandom: Boolean = false) {
    var board = Board(pawnRows)
    protected var lastMove = mutableListOf<Pair<Int, Int>>()
    protected var currentPlayer = if(startColour == CheckersColour.WHITE) {
        player1
    } else {
        player2
    }

    protected var currentColour = startColour

    val colour: CheckersColour
    get() = currentColour

    val player: Player
    get() = currentPlayer

    val playerOne: Player
    get() = player1

    val playerTwo: Player
    get() = player2

    val move: List<Pair<Int, Int>>
    get() = lastMove

    protected val allowFirstRandom = allowFirstRandom
    protected var randomUsed = 0

    init {
        player1.colour = CheckersColour.WHITE
        player2.colour = CheckersColour.BLACK
    }

    fun play() {
        while(!CheckersController.hasGameEnded(board, currentColour)) {
            CheckersController.printBoard(board, lastMove, player1, player2)
            oneMove()
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

    open fun oneMove() {
        val pieces = CheckersController.getPieces(board, currentColour)
        val captures = CheckersController.getCapturingPieces(board, pieces, currentColour)
        if(captures.first.isNotEmpty() || captures.second.isNotEmpty()) {
            val pawnCaptures = CheckersController.getPossiblePawnCaptures(board, captures.first, currentColour)
            val queenCaptures = CheckersController.getPossibleQueenCaptures(board, captures.second, currentColour)
            val longestCaptures = CheckersController.getLongestCaptures(pawnCaptures, queenCaptures)
            val pos = if(allowFirstRandom and (randomUsed < 2)) {
                randomUsed = min(randomUsed + 1, 2)
                currentPlayer.capture(longestCaptures, board, true)
            } else {
                currentPlayer.capture(longestCaptures, board, false)
            }
            //val pos = currentPlayer.capture(longestCaptures, board)
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
            val pos = if(allowFirstRandom and (randomUsed < 2)) {
                randomUsed += 1
                currentPlayer.move(allMoves, board, true)
            } else {
                currentPlayer.move(allMoves, board, false)
            }
            val playerChoice = allMoves[pos]
            lastMove = mutableListOf()
            lastMove.add(playerChoice.startPair)
            lastMove.add(playerChoice.endPair)
            board = CheckersController.executeMove(board, playerChoice)
        }
        board = CheckersController.promoteToQueen(board)
        switchPlayer()
    }

}