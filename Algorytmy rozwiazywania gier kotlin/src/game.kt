import GUI.CheckersGameGUI
import javax.swing.plaf.basic.BasicEditorPaneUI
import kotlin.reflect.jvm.internal.impl.util.Check

fun setLevel(arg: String): Int {
    return when(arg) {
        "Natsuki" -> 2
        "Sayori" -> 5
        "Yuri" -> 8
        "Monika" -> 10
        else -> 1
    }
}


fun main(args: Array<String>) {

    //ESTIMATORS
    val countEstimator = CountEstimator()
    val areaEstimator = AreaEstimator(3, 2, 1)
    val aggressiveEstimator = AggressiveAreaEstimator(listOf(6, 5), 3, 2, 1)

    val human = Human(name="Dominik")

    // BOTS
    val dummyBot1 = DummyBot(name="Dummy")
    val dummyBot2 = DummyBot()
    val minMaxBot1 = MinMaxBot("MinMax", searchDepth=8, areaEstimator)
    val minMaxBot2 = MinMaxBot("", searchDepth=6, AreaEstimator(3, 2, 1))
    val alphaBetaBot1 = AlphaBetaBot("AlfaBeta", searchDepth=7, areaEstimator)
    val alphaBetaBot2 = AlphaBetaBot("AlfaBeta", searchDepth=3, areaEstimator)

    val game = CheckersGameGUI(human, alphaBetaBot1, pawnRows=3, allowFirstRandom=true, 70)
    println("OK")
    game.start()
    println("Finished")
}