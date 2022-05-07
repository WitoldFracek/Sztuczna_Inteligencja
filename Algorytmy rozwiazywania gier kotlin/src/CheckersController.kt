

class CheckersController {

    companion object {

        private val DIRECTIONS = listOf(Pair(1, 1), Pair(1, -1), Pair(-1, 1), Pair(-1, -1))

        // === PIECE ACCESSORS ===
        fun getPieces(board: Board, colour: CheckersColour): List<Pair<Int, Int>> {
            val coordinates: MutableList<Pair<Int, Int>> = mutableListOf()
            for((i, line) in board.board.withIndex()) {
                for((j, cell) in line.withIndex()) {
                    if(!cell.isEmpty) {
                        if(cell.piece?.colour == colour) {
                            coordinates.add(Pair(i, j))
                        }
                    }
                }
            }
            return coordinates
        }

        // === CHECKS ===
        fun canPawnCapture(board: Board,
                           pawn: Pair<Int, Int>,
                           currentColour: CheckersColour,
                           excludedCells: List<Cell> = listOf()): Boolean {
            for(direction in DIRECTIONS) {
                if(isPawnJumpPossible(board, pawn, direction, currentColour, excludedCells=excludedCells)) {
                    return true
                }
            }
            return false
        }

        fun isPawnJumpPossible(board: Board,
                               pawn: Pair<Int, Int>,
                               direction: Pair<Int, Int>,
                               currentColour: CheckersColour,
                               excludedCells: List<Cell> = listOf()): Boolean {
            val x = pawn.first
            val y = pawn.second
            val xd = direction.first
            val yd = direction.second
            if(!isInBounds(board, x + xd, y + yd)) {
                return false
            }
            if(!isInBounds(board, x + 2 * xd, y + 2 * yd)) {
                return false
            }
            val cell = board[x + xd][y + yd]
            if(cell in excludedCells) {
                return false
            }
            if(cell.isEmpty){
                return false
            }
            if(cell.piece?.colour == currentColour) {
                return false
            }
            return board[x + 2 * xd][y + 2 * yd].isEmpty
        }

        fun isInBounds(board: Board, x: Int, y: Int): Boolean {
            if(x < 0) {
                return false
            }
            if(x >= board.board.size) {
                return false
            }
            if(y < 0) {
                return false
            }
            if(y >= board.board[0].size) {
                return false
            }
            return true
        }

        fun aliasFromCoordinates(x: Int, y: Int): String {
            return "ABCDEFGH"[y].toString() + "12345678"[x]
        }

        fun printBoard(board: Board, lastMove: List<Pair<Int, Int>>, player1: Player? = null, player2: Player? = null) {
            println("   A  B  C  D  E  F  G  H ")
            for((i, line) in board.board.withIndex()) {
                var s = "${i + 1} "
                for((j, cell) in line.withIndex()) {
                    val pair = Pair(i, j)
                    if( i % 2 == 0) {
                        if(j % 2 == 0) {
                            if(pair in lastMove) {
                                s += "${Colour.BG.YELLOW} ${cell.marker}${Colour.BG.YELLOW} ${Colour.END}"
                            } else {
                                s += " ${cell.marker} "
                            }
                        } else {
                            s += "${Colour.BG.WHITE} ${cell.marker} ${Colour.END}"
                        }
                    } else {
                        if(j % 2 == 0) {
                            s += "${Colour.BG.WHITE} ${cell.marker} ${Colour.END}"
                        } else {
                            if(pair in lastMove) {
                                s += "${Colour.BG.YELLOW} ${cell.marker}${Colour.BG.YELLOW} ${Colour.END}"
                            } else {
                                s += " ${cell.marker} "
                            }
                        }
                    }
                }
                s += " ${i + 1}"
                if(i == 0 && player1 != null) {
                    s += "  ${Colour.FG.WHITE}${player1.name} ${board.whiteCount}${Colour.END}"
                }
                if(i == 1 && player2 != null) {
                    s += "  ${Colour.FG.BLACK}${player2.name} ${board.blackCount}${Colour.END}"
                }
                println(s)
            }
        }
    }
}

fun main(args: Array<String>) {
    val b = Board(2)
    val p1 = Pair(1, 2)
    val p2 = Pair(3, 4)
    val p3 = Pair(3, 4)
    val xs = listOf(p1, p2)
    println(p3 in xs)
    CheckersController.printBoard(b, listOf(), Human("Witek"), Human("Maciek"))
}