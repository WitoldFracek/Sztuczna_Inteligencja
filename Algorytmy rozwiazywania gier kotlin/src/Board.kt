class Board(rows: Int = 2, newBoard: List<List<Cell>>? = null) {
    val board: List<List<Cell>>
    var whiteCount: Int
    var blackCount: Int
    var idleMoves: Int = 0

    init {
        if(newBoard != null){
            board = newBoard
            val wb = getPiecesCount()
            whiteCount = wb.first
            blackCount = wb.second
        } else {
            val tempBoard = emptyBoard()
            for( i in 0 until rows) {
                if(i % 2 == 0) {
                    for(j in tempBoard[i].indices) {
                        if(j % 2 == 0 ) {
                            tempBoard[i][j].piece = Pawn(CheckersColour.WHITE, Colour.FG.WHITE)
                        } else {
                            tempBoard[tempBoard.size - 1 - i][j].piece = Pawn(CheckersColour.BLACK, Colour.FG.BLACK)
                        }
                    }
                } else {
                    for(j in tempBoard[i].indices) {
                        if(j % 2 == 1 ) {
                            tempBoard[i][j].piece = Pawn(CheckersColour.WHITE, Colour.FG.WHITE)
                        } else {
                            tempBoard[tempBoard.size - 1 - i][j].piece = Pawn(CheckersColour.BLACK, Colour.FG.BLACK)
                        }
                    }
                }
            }
            board = tempBoard
            whiteCount = 4 * rows
            blackCount = 4 * rows
        }
    }

    operator fun get(index: Int):List<Cell> {
        return board[index]
    }

    private fun getPiecesCount(): Pair<Int, Int> {
        var whites = 0
        var blacks = 0
        for(row in board) {
            for(cell in row){
                if(!cell.isEmpty) {
                    if(cell.piece?.colour == CheckersColour.WHITE) {
                        whites += 1
                    } else {
                        blacks += 1
                    }
                }
            }
        }
        return Pair(whites, blacks)
    }



    private fun emptyBoard(): List<List<Cell>> {
        val tempBoard = mutableListOf<List<Cell>>()
        for(number in "12345678") {
            val row = mutableListOf<Cell>()
            for (letter in "ABCDEFGH") {
                row.add(Cell("$letter$number"))
            }
            tempBoard.add(row)
        }
        return tempBoard
    }

    fun empty(): Board {
        val emptyBoard = emptyBoard()
        return Board(newBoard=emptyBoard)
    }

    fun copy(): Board {
        val newBoard = mutableListOf<MutableList<Cell>>()
        for(line in board) {
            val row = mutableListOf<Cell>()
            for(cell in line) {
                row.add(Cell(cell.alias, cell.piece))
            }
            newBoard.add(row)
        }
        return Board(newBoard=newBoard)
    }
}

fun main(args: Array<String>) {
    val b = Board(2)
    for(row in b.board) {
        println(row)
    }
}