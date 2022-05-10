import kotlin.reflect.jvm.internal.impl.util.Check

fun main(args: Array<String>) {
    val human = Human("Witek")
    val dummyBot1 = DummyBot(name="Dummy")
    val dummyBot2 = DummyBot()
    val minMaxBot1 = MinMaxBot("White", searchDepth=5, CountEstimator())
    val minMaxBot2 = MinMaxBot("Black", searchDepth=5, CountEstimator())
    val game = CheckersGame(dummyBot1, minMaxBot2, pawnRows=2, startColour=CheckersColour.WHITE)
    game.play()
}