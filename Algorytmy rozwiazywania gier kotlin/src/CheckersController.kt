

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

        fun getCapturingPieces(board: Board, pieces: List<Pair<Int, Int>>, colour: CheckersColour): Pair<List<Pair<Int, Int>>, List<Pair<Int, Int>>> {
            val capturingPawns = mutableListOf<Pair<Int, Int>>()
            val capturingQueens = mutableListOf<Pair<Int, Int>>()
            for(piece in pieces) {
                val cell = board[piece.first][piece.second]
                if(cell.piece is Pawn) {
                    if(canPawnCapture(board, piece, colour)) {
                        capturingPawns.add(piece)
                    }
                } else if(cell.piece is Queen) {
                    if(canQueenCapture(board, piece, colour)) {
                        capturingQueens.add(piece)
                    }
                }
            }
            return Pair(capturingPawns, capturingQueens)
        }

        fun getMovingPieces(board: Board, pieces: List<Pair<Int, Int>>, colour: CheckersColour): Pair<List<Pair<Int, Int>>, List<Pair<Int, Int>>> {
            val movingPawns = mutableListOf<Pair<Int, Int>>()
            val movingQueens = mutableListOf<Pair<Int, Int>>()
            for(piece in pieces) {
                val cell = board[piece.first][piece.second]
                if(cell.piece is Pawn) {
                    if(canPawnMove(board, piece, colour)) {
                        movingPawns.add(piece)
                    }
                } else if(cell.piece is Queen) {
                    if(canQueenMove(board, piece, colour)) {
                        movingQueens.add(piece)
                    }
                }
            }
            return Pair(movingPawns, movingQueens)
        }

        fun getPawnCaptureDirections(board: Board,
                                     pawn: Pair<Int, Int>,
                                     colour: CheckersColour,
                                     excludedCells: List<Cell> = listOf()): List<Pair<Int, Int>> {
            val ret: MutableList<Pair<Int, Int>> = mutableListOf()
            for(direction in DIRECTIONS) {
                if(isPawnJumpPossible(board, pawn, direction, colour, excludedCells=excludedCells)) {
                    ret.add(direction)
                }
            }
            return ret
        }

        fun getLongestCaptures(capturingPieces: List<List<Jump>>, capturingQueens: List<List<Jump>>): List<List<Jump>> {
            val allCaptures = mutableListOf<List<Jump>>()
            allCaptures.addAll(capturingPieces)
            allCaptures.addAll(capturingQueens)
            if(allCaptures.size == 0) {
                return listOf()
            }
            val maxLength = allCaptures.maxByOrNull { it.size }!!.size
            val maxPath = mutableListOf<List<Jump>>()
            for(list in allCaptures) {
                if(list.size == maxLength) {
                    maxPath.add(list)
                }
            }
            return maxPath
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

        fun canQueenCapture(board: Board,
                            queen: Pair<Int, Int>,
                            currentColour: CheckersColour,
                            excludedCells: List<Cell> = listOf()): Boolean {
            for(direction in DIRECTIONS) {
                if(isQueenJumpPossible(board, queen, direction, currentColour, excludedCells=excludedCells)) {
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

        fun isQueenJumpPossible(board: Board,
                                queen: Pair<Int, Int>,
                                direction: Pair<Int, Int>,
                                currentColour: CheckersColour,
                                excludedCells: List<Cell> = listOf()):Boolean {
            val xd = direction.first
            val yd = direction.second
            val diagonal = diagonal(board, queen, direction)
            for(pair in diagonal.subList(0, diagonal.size - 1)) {
                val cell = board[pair.first][pair.second]
                if(cell in excludedCells) {
                    return false
                }
                if(!cell.isEmpty) {
                    if(board[queen.first + xd][queen.second + yd].isEmpty) {
                        if(currentColour != cell.piece?.colour) {
                            return true
                        }
                    }
                }

            }
            return false
        }

        fun canPawnMove(board: Board, pawn: Pair<Int, Int>, currentColour: CheckersColour): Boolean {
            if(currentColour == CheckersColour.WHITE) {
                return isMovePossible(board, pawn, Pair(1, -1)) || isMovePossible(board, pawn, Pair(1, 1))
            }
            return isMovePossible(board, pawn, Pair(-1, -1)) || isMovePossible(board, pawn, Pair(-1, 1))
        }

        fun canQueenMove(board: Board, queen: Pair<Int, Int>, currentColour: CheckersColour): Boolean {
            for(direction in DIRECTIONS) {
                if(isMovePossible(board, queen, direction)) {
                    return true
                }
            }
            return false
        }

        fun isMovePossible(board: Board, pawn: Pair<Int, Int>, direction: Pair<Int, Int>): Boolean {
            val xd = direction.first
            val yd = direction.second
            if(isInBounds(board, pawn.first + xd, pawn.second + yd)) {
                return board[pawn.first + xd][pawn.second + yd].isEmpty
            }
            return false
        }

        // === UTILS ===
        fun promoteToQueen(board: Board): Board {
            for(cell in board[0]) {
                if(!cell.isEmpty) {
                    if(cell.piece?.colour == CheckersColour.BLACK) {
                        if(cell.piece is Pawn) {
                            val pawn = cell.piece as Pawn
                            cell.piece = pawn.promote()
                        }
                    }
                }
            }
            for(cell in board[board.board.size - 1]) {
                if(!cell.isEmpty) {
                    if(cell.piece?.colour == CheckersColour.BLACK) {
                        if(cell.piece is Pawn) {
                            val pawn = cell.piece as Pawn
                            cell.piece = pawn.promote()
                        }
                    }
                }
            }
            return board
        }

        fun hasGameEnded(board: Board, colour: CheckersColour): Boolean {
            if(colour == CheckersColour.WHITE) {
                if(board.whiteCount == 0) {
                    return true
                }
            } else {
                if(board.blackCount == 0) {
                    return true
                }
            }
            val pieces = getPieces(board, colour)
            val captures = getCapturingPieces(board, pieces, colour)
            if(captures.first.isNotEmpty() || captures.second.isNotEmpty()) {
                return false
            }
            val moves = getMovingPieces(board, pieces, colour)
            if(moves.first.isNotEmpty() || moves.second.isNotEmpty()) {
                return false
            }
            return true
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

        fun diagonal(board: Board, queen: Pair<Int, Int>, direction: Pair<Int, Int>): List<Pair<Int, Int>> {
            val xd = direction.first
            val yd = direction.second
            val ret = mutableListOf<Pair<Int, Int>>()
            for(i in 1 until board.board.size) {
                if(isInBounds(board, queen.first + i * xd, queen.second + i * yd)) {
                    ret.add(Pair(queen.first + i * xd, queen.second + i * yd))
                }
            }
            return ret
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
    val diagonal = CheckersController.diagonal(Board(), Pair(3, 3), Pair(-1, 1))
    for(elem in diagonal) {
        println(elem)
    }
}