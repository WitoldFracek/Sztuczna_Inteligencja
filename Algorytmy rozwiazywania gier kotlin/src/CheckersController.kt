

class CheckersController {



    companion object {
        fun aliasFromCoordinates(x: Int, y: Int): String {
            return "ABCDEFGH"[y].toString() + "12345678"[x]
        }

        fun printBoard(board: Board) {
            println("   A  B  C  D  E  F  G  H ")
            for((i, line) in board.board.withIndex()) {
                var s = "${i + 1} "
                for((j, cell) in line.withIndex()) {
                    if( i % 2 == 0) {
                        if(j % 2 == 0) {
                            s += " ${cell.marker} "
                        } else {
                            s += "${Colour.BG.WHITE} ${cell.marker} ${Colour.END}"
                        }
                    } else {
                        if(j % 2 == 0) {
                            s += "${Colour.BG.WHITE} ${cell.marker} ${Colour.END}"
                        } else {
                            s += " ${cell.marker} "
                        }
                    }
                }
                println(s)
            }
        }
    }
}

fun main(args: Array<String>) {
    val b = Board(3)
    CheckersController.printBoard(b)
}