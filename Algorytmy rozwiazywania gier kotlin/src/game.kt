import kotlin.reflect.jvm.internal.impl.util.Check

fun main(args: Array<String>) {
    val human = Human("Witek")
    val dummyBot1 = DummyBot(name="Dummy")
    val dummyBot2 = DummyBot()
    val minMaxBot1 = MinMaxBot("White", searchDepth=3, CountEstimator())
    val minMaxBot2 = MinMaxBot("", searchDepth=5, AreaEstimator(3, 2, 1))
    val game = CheckersGame(minMaxBot1, minMaxBot2, pawnRows=2, startColour=CheckersColour.WHITE)
    game.play()
}