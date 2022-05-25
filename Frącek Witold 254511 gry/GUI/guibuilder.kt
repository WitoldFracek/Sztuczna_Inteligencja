package GUI
import AlphaBetaBot
import AreaEstimator
import Board
import CheckersColour
import CheckersController
import CheckersGame
import DummyBot
import Human
import MinMaxBot
import Pawn
import java.awt.Color
import java.awt.GridBagConstraints
import java.awt.GridBagLayout
import java.awt.GridLayout
import javax.swing.*

class GUIController(fieldSize: Int) {
    val mainFrame = JFrame("Checkers")
    val boardPanel = CheckeredBoard(fieldSize)
    val presenterPanel = PresenterPanel((boardPanel.size.width * 0.5).toInt() * 0, boardPanel.size.height)

    init {
        mainFrame.add(boardPanel)
        //mainFrame.add(presenterPanel)

        mainFrame.setSize(boardPanel.size.width + presenterPanel.size.width, boardPanel.size.height)
        mainFrame.isVisible = true
        mainFrame.defaultCloseOperation = JFrame.EXIT_ON_CLOSE
    }

    fun update(board: Board, lastMove: List<Pair<Int, Int>> = listOf()) {
        for((i, line) in board.board.withIndex()) {
            for((j, cell) in line.withIndex()) {
                boardPanel.buttons[i][j].background = boardPanel.buttons[i][j].originalColor
                boardPanel.buttons[i][j].icon = if(cell.isEmpty) {
                    null
                } else if(cell.piece is Pawn) {
                    if(cell.piece?.colour == CheckersColour.WHITE) {
                        boardPanel.images["white pawn"]
                    } else {
                        boardPanel.images["black pawn"]
                    }
                } else {
                    if(cell.piece?.colour == CheckersColour.WHITE) {
                        boardPanel.images["white queen"]
                    } else {
                        boardPanel.images["black queen"]
                    }
                }
            }
        }
        for((x, y) in lastMove) {
            boardPanel.buttons[x][y].background = Color.YELLOW
        }
    }

    fun markMovingPieces(movingPieces: List<Pair<Int, Int>>) {
        for((x, y) in movingPieces) {
            boardPanel.buttons[x][y].background = Color.GREEN
        }
    }
}
