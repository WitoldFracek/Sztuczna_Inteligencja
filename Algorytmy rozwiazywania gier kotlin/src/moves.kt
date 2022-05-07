

data class Move(val xStart: Int,
           val yStart: Int,
           val xEnd: Int,
           val yEnd: Int
           )

data class Jump(val xStart: Int,
                val yStart: Int,
                val xEnd: Int,
                val yEnd: Int,
                val xCapture: Int,
                val yCapture: Int
                )