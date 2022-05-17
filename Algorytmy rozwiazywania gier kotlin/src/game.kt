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
    val level = setLevel("Natsuki")
    val human = Human("Witek")
    val dummyBot1 = DummyBot(name="Dummy")
    val dummyBot2 = DummyBot()
    val minMaxBot1 = MinMaxBot("White", searchDepth=5, AreaEstimator(3, 2, 1))
    val minMaxBot2 = MinMaxBot("", searchDepth=6, AreaEstimator(3, 2, 1))
    val alphaBetaBot1 = AlphaBetaBot("", searchDepth=9, AreaEstimator(3, 2, 1))
    val game = CheckersGame(human, alphaBetaBot1, pawnRows=3, startColour=CheckersColour.WHITE, allowFirstRandom=true)
    game.play()
}