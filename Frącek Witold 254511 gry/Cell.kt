

class Cell(val alias: String, var piece: Piece? = null) {

    val marker: String
        get() = piece?.marker ?: " "

    val isEmpty: Boolean
        get() = piece == null

    override fun equals(other: Any?): Boolean {
        if(other !is Cell){
            return false
        }
        return alias == other.alias
    }

    override fun hashCode(): Int {
        var result = alias.hashCode()
        result = 31 * result + (piece?.hashCode() ?: 0)
        return result
    }

    override fun toString(): String {
        return marker
    }
}