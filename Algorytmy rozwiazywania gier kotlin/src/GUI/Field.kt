package GUI
import java.awt.*
import javax.swing.*

class Field(fieldSize: Int, color: Color): JButton() {

    init{
        this.background = color
        this.foreground = color.darker()
        setSize(fieldSize, fieldSize)
    }
}