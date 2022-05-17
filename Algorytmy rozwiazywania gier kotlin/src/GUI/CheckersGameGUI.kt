package GUI

import Bot
import CheckersController
import CheckersGame
import Human
import Jump
import Move
import Player
import java.awt.Color
import java.util.concurrent.atomic.AtomicBoolean
import javax.swing.JFrame

class CheckersGameGUI(player1: Player,
                      player2: Player,
                      pawnRows: Int,
                      allowFirstRandom: Boolean,
                      fieldSize: Int
): CheckersGame(player1, player2, pawnRows, CheckersColour.WHITE, allowFirstRandom) {
    private var gui: GUIController = GUIController(fieldSize)
    private var firstClicked = false
    private var isLocked = AtomicBoolean(true)
    private var firstCoordinate = Pair(-1, -1)
    private var secondCoordinate = Pair(-1, -1)
    private var check = AtomicBoolean(false)

    init {
        for((i, row) in gui.boardPanel.buttons.withIndex()) {
            for((j, button) in row.withIndex()) {
                button.addActionListener {
                    checkForMove(i, j)
                }
            }
        }
        gui.update(board)
    }

    fun start() {
        isLocked.set(false)
        while(true) {
            if(check.get() || currentPlayer is Bot) {
                executeOneCycle()
                if(CheckersController.hasGameEnded(board, currentColour)){
                    break
                }
                check.set(false)
            }
        }
    }

    private fun checkForMove(x: Int, y: Int) {
        if(isLocked.get()) return
        if(!firstClicked) {
            firstCoordinate = Pair(x, y)
            firstClicked = true
        } else {
            secondCoordinate = Pair(x, y)
            firstClicked = false
            isLocked.set(true)
            check.set(true)
        }
        highlightField(firstCoordinate.first, firstCoordinate.second, firstClicked)
    }

    private fun executeOneCycle() {
        CheckersController.printBoard(board, lastMove, player1, player2)
        if(currentPlayer is Human) {
            humanMove()
            isLocked.set(false)
        } else {
            botMove()
            isLocked.set(false)
        }
    }

    private fun humanMove() {
        val pieces = CheckersController.getPieces(board, currentColour)
        val captures = CheckersController.getCapturingPieces(board, pieces, currentColour)
        if(captures.first.isNotEmpty() || captures.second.isNotEmpty()) {
            val pawnCaptures = CheckersController.getPossiblePawnCaptures(board, captures.first, currentColour)
            val queenCaptures = CheckersController.getPossibleQueenCaptures(board, captures.second, currentColour)
            val longestCaptures = CheckersController.getLongestCaptures(pawnCaptures, queenCaptures)
            val movingStarts = longestCaptures.map{ it[0].startPair }
            gui.markMovingPieces(movingStarts)
            val pos = isPlayerCaptureInputCorrect(longestCaptures)
            if(pos == -1) {
                println("${Colour.FG.ORANGE}Invalid input${Colour.END}")
                return
            }
            val playerChoice = longestCaptures[pos]
            lastMove = playerChoice.map{ it.startPair }.toMutableList()
            lastMove.add(playerChoice.last().endPair)
            board = CheckersController.executeCapture(board, playerChoice)
        } else {
            val moves = CheckersController.getMovingPieces(board, pieces, currentColour)
            val pawnMoves = CheckersController.getPossiblePawnMoves(board, moves.first, currentColour)
            val queenMoves = CheckersController.getPossibleQueenMoves(board, moves.second)
            val allMoves = mutableListOf<Move>()
            allMoves.addAll(pawnMoves)
            allMoves.addAll(queenMoves)
            val movingStarts = allMoves.map{ it.startPair }
            gui.markMovingPieces(movingStarts)
            val pos = isPlayerMoveInputCorrect(allMoves)
            if(pos == -1) {
                println("${Colour.FG.ORANGE}Invalid input${Colour.END}")
                return
            }
            val playerChoice = allMoves[pos]
            lastMove = mutableListOf()
            lastMove.add(playerChoice.startPair)
            lastMove.add(playerChoice.endPair)
            board = CheckersController.executeMove(board, playerChoice)
        }
        board = CheckersController.promoteToQueen(board)
        gui.update(board, lastMove)
        switchPlayer()
    }

    private fun isPlayerCaptureInputCorrect(longestCaptures: List<List<Jump>>): Int {
        var index = -1
        for((i, capture) in longestCaptures.withIndex()) {
            if(capture[0].startPair == firstCoordinate && capture.last().endPair == secondCoordinate) {
                index = i
            }
        }
        return index
    }

    private fun isPlayerMoveInputCorrect(allMoves: List<Move>): Int {
        var index = -1
        for((i, move) in allMoves.withIndex()) {
            if(move.startPair == firstCoordinate && move.endPair == secondCoordinate) {
                index = i
            }
        }
        return index
    }

    private fun botMove() {
        oneMove()
        gui.update(board, lastMove)
    }

    private fun highlightField(x: Int, y: Int, isHighlighted: Boolean) {
        if(isHighlighted) {
            gui.boardPanel.buttons[x][y].background = Color.CYAN
        } else {
            gui.boardPanel.buttons[x][y].background = gui.boardPanel.buttons[x][y].originalColor
        }
    }

}