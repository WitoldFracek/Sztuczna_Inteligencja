import kotlin.reflect.jvm.internal.impl.util.Check

fun main(args: Array<String>) {
    val human = Human("Witek")
    val dummyBot1 = DummyBot()
    val dummyBot2 = DummyBot()
    val game = CheckersGame(dummyBot1, dummyBot2, pawnRows=3, startColour=CheckersColour.WHITE)
    game.play()
}