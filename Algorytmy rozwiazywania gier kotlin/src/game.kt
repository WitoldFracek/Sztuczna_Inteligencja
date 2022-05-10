import kotlin.reflect.jvm.internal.impl.util.Check

fun main(args: Array<String>) {
    val human = Human("Witek")
    val dummyBot1 = DummyBot(name="Dummy")
    val dummyBot2 = DummyBot()
    val minMaxBot1 = MinMaxBot("Four", searchDepth=4, CountEstimator())
    val minMaxBot2 = MinMaxBot("Six", searchDepth=6, CountEstimator())
    val game = CheckersGame(minMaxBot1, minMaxBot2, pawnRows=2, startColour=CheckersColour.WHITE)
    game.play()
}