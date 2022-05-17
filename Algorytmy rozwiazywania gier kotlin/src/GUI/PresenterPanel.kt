package GUI
import java.awt.*
import javax.swing.*

class PresenterPanel(width: Int, height:Int): JPanel() {

    init {
        background = Color.ORANGE
        setSize(width, height)
    }
}