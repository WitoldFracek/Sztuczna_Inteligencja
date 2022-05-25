enum class CheckersColour {
    WHITE {
        override fun oppositeColour(): CheckersColour {
            return BLACK
        }
          },
    BLACK {
        override fun oppositeColour(): CheckersColour {
            return WHITE
        }
    };

    abstract fun oppositeColour(): CheckersColour
}