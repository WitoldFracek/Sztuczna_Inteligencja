package GUI
import java.awt.*
import javax.swing.*

class Field(fieldSize: Int, color: Color): JButton() {
    val originalColor = color

    init {
        this.background = color
        this.foreground = color.darker()
        this.isFocusPainted = false
        setSize(fieldSize, fieldSize)
    }
}