class Board(rows: Int = 2) {
    val board: List<List<Cell>>

    init {
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
    }

    operator fun get(index: Int):List<Cell> {
        return board[index]
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
}

fun main(args: Array<String>) {
    val b = Board(2)
    for(row in b.board) {
        println(row)
    }
}