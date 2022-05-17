package GUI
import java.awt.*
import javax.swing.*

class CheckeredBoard(fieldSize: Int): JPanel(GridLayout(8, 8)) {
    val buttons = mutableListOf<List<Field>>()

    init {
        layout = GridLayout(8, 8)
        val temp = mutableListOf<List<Field>>()
        for(i in 0 until 8){
            val tempList = mutableListOf<Field>()
            for(j in 0 until 8) {
                val fieldButton = if((j + (i % 2)) % 2 == 0) {
                    Field(fieldSize, Color.GRAY.darker().darker())
                } else {
                    Field(fieldSize, Color.WHITE)
                }
                add(fieldButton)
                tempList.add(fieldButton)
            }
            temp.add(tempList)
        }
        buttons.addAll(temp)
        setSize(8 * fieldSize, 8 * fieldSize)
    }
}

fun main() {
    val frame = JFrame()
    frame.add(CheckeredBoard(70))
    frame.setSize(70 * 8, 70 * 8)
    frame.isVisible = true
}