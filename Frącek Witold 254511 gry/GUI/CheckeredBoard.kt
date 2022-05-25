package GUI
import java.awt.*
import javax.imageio.ImageIO
import javax.swing.*

class CheckeredBoard(fieldSize: Int): JPanel(GridLayout(8, 8)) {
    val buttons = mutableListOf<List<Field>>()
    val images = loadImages()

    init {
        layout = GridLayout(8, 8)
        val temp = mutableListOf<List<Field>>()
        for(i in 0 until 8){
            val tempList = mutableListOf<Field>()
            for(j in 0 until 8) {
                val fieldButton = if((j + (i % 2)) % 2 == 0) {
                    Field(fieldSize, Color.GRAY.darker())
                } else {
                    val f = Field(fieldSize, Color.WHITE)
                    f.isEnabled = false
                    f
                }
                add(fieldButton)
                tempList.add(fieldButton)
            }
            temp.add(tempList)
        }
        buttons.addAll(temp)
        setSize(8 * fieldSize, 8 * fieldSize)
    }

    fun loadImages(): HashMap<String, ImageIcon> {
        try{
            val blackPawn = ImageIO.read(javaClass.getResource("..\\images\\black_pawn.png"))
            val blackPawnImg = ImageIcon(blackPawn)
            val blackQueen = ImageIO.read(javaClass.getResource("..\\images\\black_queen.png"))
            val blackQueenImg = ImageIcon(blackQueen)
            val whitePawn = ImageIO.read(javaClass.getResource("..\\images\\white_pawn.png"))
            val whitePawnImg = ImageIcon(whitePawn)
            val whiteQueen = ImageIO.read(javaClass.getResource("..\\images\\white_queen.png"))
            val whiteQueenImg = ImageIcon(whiteQueen)
            return hashMapOf(Pair("black pawn", blackPawnImg),
                                Pair("black queen", blackQueenImg),
                                Pair("white pawn", whitePawnImg),
                                Pair("white queen", whiteQueenImg))
        } catch(e: Exception) {
            return hashMapOf()
        }

    }
}

fun main() {
    val frame = JFrame()
    frame.add(CheckeredBoard(70))
    frame.setSize(70 * 8, 70 * 8)
    frame.isVisible = true
}