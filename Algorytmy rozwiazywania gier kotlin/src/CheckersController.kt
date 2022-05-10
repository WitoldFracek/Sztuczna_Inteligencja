import kotlin.reflect.jvm.internal.impl.util.Check

class CheckersController {

    companion object {

        private val DIRECTIONS = listOf(Pair(1, 1), Pair(1, -1), Pair(-1, 1), Pair(-1, -1))

        // === CONTROLS ===
        fun executeCapture(board: Board, capture: List<Jump>): Board {
            val firstJump = capture[0]
            val lastJump = capture[capture.size - 1]
            val movingPiece = board[firstJump.xStart][firstJump.yStart].piece
            board[firstJump.xStart][firstJump.yStart].piece = null
            for(jump in capture) { //.subList(1, capture.size)) {
                val xEnemy = jump.xCapture
                val yEnemy = jump.yCapture
                val enemyCell = board[xEnemy][yEnemy]
                if(enemyCell.piece?.colour == CheckersColour.WHITE) {
                    board.whiteCount -= 1
                } else {
                    board.blackCount -= 1
                }
                enemyCell.piece = null
            }
            board[lastJump.xEnd][lastJump.yEnd].piece = movingPiece
            return board
        }

        fun executeMove(board: Board, move: Move): Board {
            val movingPiece = board[move.xStart][move.yStart].piece
            board[move.xStart][move.yStart].piece = null
            board[move.xEnd][move.yEnd].piece = movingPiece
            return board
        }

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

        fun getAllCaptures(board: Board, colour: CheckersColour): List<List<Jump>> {
            val pieces = getPieces(board, colour)
            val capturingPieces = getCapturingPieces(board, pieces, colour)
            val pawnCaptures = getPossiblePawnCaptures(board, capturingPieces.first, colour)
            val queenCaptures = getPossibleQueenCaptures(board, capturingPieces.second, colour)
            val allCaptures = mutableListOf<List<Jump>>()
            allCaptures.addAll(pawnCaptures)
            allCaptures.addAll(queenCaptures)
            return allCaptures
        }

        fun getAllMoves(board: Board, colour: CheckersColour): List<Move> {
            val pieces = getPieces(board, colour)
            val movingPieces = getMovingPieces(board, pieces, colour)
            val pawnMoves = getPossiblePawnMoves(board, movingPieces.first, colour)
            val queenMoves = getPossibleQueenMoves(board, movingPieces.second)
            val allMoves = mutableListOf<Move>()
            allMoves.addAll(pawnMoves)
            allMoves.addAll(queenMoves)
            return allMoves
        }

        fun getPossiblePawnCaptures(board: Board, capturingPawns: List<Pair<Int, Int>>, colour: CheckersColour): List<List<Jump>> {
            val paths = mutableListOf<List<Jump>>()
            for(pawn in capturingPawns) {
                val storePiece = board[pawn.first][pawn.second].piece
                board[pawn.first][pawn.second].piece = null
                val sol = mutableListOf<List<Jump>>()
                getPawnCapturePath(board, pawn, colour, mutableListOf(), mutableListOf(), sol)
                paths.addAll(sol.toList())
                board[pawn.first][pawn.second].piece = storePiece
            }
            if(paths.isEmpty()) {
                return paths
            }
            val maxLen = paths.maxByOrNull{ it.size }!!.size
            val ret = mutableListOf<List<Jump>>()
            for(path in paths) {
                if(path.size == maxLen) {
                    ret.add(path)
                }
            }
            return ret
        }

        fun getPossibleQueenCaptures(board: Board, capturingQueens: List<Pair<Int, Int>>, colour: CheckersColour): List<List<Jump>> {
            val paths = mutableListOf<List<Jump>>()
            for(queen in capturingQueens) {
                val storeQueen = board[queen.first][queen.second].piece
                board[queen.first][queen.second].piece = null
                val sol = mutableListOf<List<Jump>>()
                getQueenCapturePath(board, queen, colour, mutableListOf(), mutableListOf(), sol)
                paths.addAll(sol.toList())
                board[queen.first][queen.second].piece = storeQueen
            }
            if(paths.isEmpty()) {
                return paths
            }
            val maxLen = paths.maxByOrNull{ it.size }!!.size
            val ret = mutableListOf<List<Jump>>()
            for(path in paths) {
                if(path.size == maxLen) {
                    ret.add(path)
                }
            }
            return ret
        }

        fun getPawnCapturePath(board: Board,
                               pawn: Pair<Int, Int>,
                               colour: CheckersColour,
                               jumpedOver: MutableList<Cell>,
                               acc: MutableList<Jump>,
                               solutions: MutableList<List<Jump>>) {
            if(canPawnCapture(board, pawn, colour, excludedCells=jumpedOver)) {
                val directions = getPawnCaptureDirections(board, pawn, colour, excludedCells=jumpedOver)
                for(direction in directions) {
                    val jump = Jump(pawn.first, pawn.second,
                    pawn.first + 2 * direction.first,
                    pawn.second + 2 * direction.second,
                    pawn.first + direction.first,
                    pawn.second + direction.second)
                    acc.add(jump)
                    val jumpedOverCopy = jumpedOver.toMutableList()
                    val accCopy = acc.toMutableList()
                    jumpedOverCopy.add(board[jump.xCapture][jump.yCapture])
                    getPawnCapturePath(board, Pair(jump.xEnd, jump.yEnd), colour, jumpedOverCopy, accCopy, solutions)
                }
            } else {
                solutions.add(acc)
            }
        }

        fun getQueenCapturePath(board: Board,
                                queen: Pair<Int, Int>,
                                colour: CheckersColour,
                                jumpedOver: MutableList<Cell>,
                                acc: MutableList<Jump>,
                                solutions: MutableList<List<Jump>>) {
            if(canQueenCapture(board, queen, colour, excludedCells=jumpedOver)) {
                val landingSpots = queenLandingSpots(board, queen, colour, excludedCells=jumpedOver)
                for(jump in landingSpots) {
                    val xEnemy = jump.xCapture
                    val yEnemy = jump.yCapture
                    val cell = board[xEnemy][yEnemy]
                    if(cell !in jumpedOver) {
                        jumpedOver.add(cell)
                    }
                    val jumpedOverCopy = jumpedOver.toMutableList()
                    val accCopy = acc.toMutableList()
                    accCopy.add(jump)
                    getQueenCapturePath(board, Pair(jump.xEnd, jump.yEnd), colour, jumpedOverCopy, accCopy, solutions)
                }
            } else {
                solutions.add(acc)
            }
        }

        fun getPossiblePawnMoves(board: Board, movingPawns: List<Pair<Int, Int>>, colour: CheckersColour): List<Move> {
            val moves = mutableListOf<Move>()
            for(pawn in movingPawns) {
                val path = getPawnMovePath(board, pawn, colour)
                moves.addAll(path)
            }
            return moves
        }

        fun getPawnMovePath(board: Board, pawn: Pair<Int, Int>, colour: CheckersColour): List<Move> {
            val moves = mutableListOf<Move>()
            if(colour == CheckersColour.WHITE) {
                if(isMovePossible(board, pawn, Pair(1, -1))) {
                    moves.add(Move(pawn.first, pawn.second, pawn.first + 1, pawn.second - 1))
                }
                if(isMovePossible(board, pawn, Pair(1, 1))) {
                    moves.add(Move(pawn.first, pawn.second, pawn.first + 1, pawn.second + 1))
                }
            } else {
                if(isMovePossible(board, pawn, Pair(-1, -1))) {
                    moves.add(Move(pawn.first, pawn.second, pawn.first - 1, pawn.second - 1))
                }
                if(isMovePossible(board, pawn, Pair(-1, 1))) {
                    moves.add(Move(pawn.first, pawn.second, pawn.first - 1, pawn.second + 1))
                }
            }
            return moves
        }

        fun getPossibleQueenMoves(board: Board, movingQueens: List<Pair<Int, Int>>): List<Move> {
            val moves = mutableListOf<Move>()
            for(queen in movingQueens) {
                val path = getQueenMovePath(board, queen)
                moves.addAll(path)
            }
            return moves
        }

        fun getQueenMovePath(board: Board, queen: Pair<Int, Int>): List<Move> {
            val moves = mutableListOf<Move>()
            for(direction in DIRECTIONS) {
                val diagonal = diagonal(board, queen, direction)
                var obstacleFound = false
                for(pos in diagonal) {
                    if(!obstacleFound) {
                        if(board[pos.first][pos.second].isEmpty) {
                            moves.add(Move(queen.first, queen.second, pos.first, pos.second))
                        } else {
                            obstacleFound = true
                        }
                    }
                }
            }
            return moves
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
                                excludedCells: List<Cell> = listOf()): Boolean {
            val xd = direction.first
            val yd = direction.second
            val diagonal = diagonal(board, queen, direction)
            if(diagonal.size < 2) {
                return false
            }
            for(pos in diagonal.subList(0, diagonal.size - 1)) {
                val cell = board[pos.first][pos.second]
                if(cell in excludedCells) {
                    return false
                }
                if(!cell.isEmpty) {
                    if(board[pos.first + xd][pos.second + yd].isEmpty) {
                        if(currentColour != cell.piece?.colour) {
                            return true
                        }
                    } else {
                        return false
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
                    if(cell.piece?.colour == CheckersColour.WHITE) {
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

        fun queenLandingSpots(board: Board, queen: Pair<Int, Int>, colour: CheckersColour, excludedCells: List<Cell>): List<Jump> {
            val landingSpots = mutableListOf<Jump>()
            for(direction in DIRECTIONS) {
                val diagonal = diagonal(board, queen, direction)
                var enemyIndex = -1
                var obstacleIndex = -1
                for((i, pos) in diagonal.withIndex()) {
                    if(obstacleIndex != -1) {
                        break
                    }
                    val cell = board[pos.first][pos.second]
                    if(cell in excludedCells) {
                        continue
                    }
                    if(!cell.isEmpty) {
                        if(cell.piece?.colour != colour) {
                            if(enemyIndex == -1) {
                                enemyIndex = i
                            } else {
                                obstacleIndex = i
                            }
                        } else {
                            obstacleIndex = i
                        }
                    } else if(enemyIndex != -1) {
                        landingSpots.add(Jump(queen.first, queen.second,
                        pos.first, pos.second,
                        diagonal[enemyIndex].first, diagonal[enemyIndex].second))
                    }
                }
            }
            return landingSpots
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
            println("   A  B  C  D  E  F  G  H \n")
        }
    }
}

fun main(args: Array<String>) {
    val diagonal = CheckersController.diagonal(Board(), Pair(3, 3), Pair(-1, 1))
    for(elem in diagonal) {
        println(elem)
    }
}