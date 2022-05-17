package GUI
import AlphaBetaBot
import AreaEstimator
import Board
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

class GUIController(gameController: CheckersGame, fieldSize: Int) {
    val mainFrame = JFrame("Checkers")
    val boardPanel = CheckeredBoard(fieldSize)
    val presenterPanel = PresenterPanel((boardPanel.size.width * 0.5).toInt() * 0, boardPanel.size.height)
    val controller = gameController

    init {
        mainFrame.add(boardPanel)
        mainFrame.add(presenterPanel)

        mainFrame.setSize(boardPanel.size.width + presenterPanel.size.width, boardPanel.size.height)
        mainFrame.isVisible = true
        mainFrame.defaultCloseOperation = JFrame.EXIT_ON_CLOSE
    }

    fun update(board: Board) {
        for((i, line) in board.board.withIndex()) {
            for((j, cell) in line.withIndex()) {
                boardPanel.buttons[i][j].text = if(cell.isEmpty){
                    ""
                } else if(cell.piece is Pawn) {
                    "P"
                } else {
                    "Q"
                }
                boardPanel.buttons[i][j].foreground = if(cell.isEmpty) {
                    Color.RED
                } else if(cell.piece?.colour == CheckersColour.BLACK) {
                    Color.BLACK
                } else {
                    Color.WHITE
                }
            }
        }
    }
}

fun main() {
    val human = Human("Witek")
    val dummyBot1 = DummyBot(name="Dummy")
    val dummyBot2 = DummyBot()
    val minMaxBot1 = MinMaxBot("White", searchDepth=5, AreaEstimator(3, 2, 1))
    val minMaxBot2 = MinMaxBot("", searchDepth=6, AreaEstimator(3, 2, 1))
    val alphaBetaBot1 = AlphaBetaBot("", searchDepth=9, AreaEstimator(3, 2, 1))
    val game = CheckersGame(human, alphaBetaBot1, pawnRows=3, startColour=CheckersColour.WHITE, allowFirstRandom=true)
    var gui: GUIController? = null
    val thread = Thread{
        gui = GUIController(game, 80)
    }
    thread.start()
    Thread.sleep(1000)
    println(gui?.boardPanel?.buttons)
    while(!CheckersController.hasGameEnded(game.board, game.colour)) {
        CheckersController.printBoard(game.board, game.move, game.playerOne, game.playerTwo)
        game.oneMove()
        gui?.update(game.board)
    }
    game.switchPlayer()


}