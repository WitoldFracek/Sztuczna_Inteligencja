class Colour {

    class Style {
        companion object {
            const val BOLD = "\u001b[1m"
            const val ITALIC = "\u001b[3m"
            const val URL = "\u001b[4m"
            const val BLINK = "\u001b[5m"
            const val BLINK2 = "\u001b[6m"
            const val SELECTED = "\u001b[7m"
        }
    }

    class FG {
        companion object {
            const val BLACK = "\u001b[30m"
            const val RED = "\u001b[31m"
            const val GREEN = "\u001b[32m"
            const val YELLOW = "\u001b3[33m"
            const val BLUE = "\u001b[34m"
            const val VIOLET = "\u001b[35m"
            const val BEIGE = "\u001b[36m"
            const val WHITE = "\u001b[37m"
            const val ORANGE = "\u001b[38;2;255;128;0m"
        }
    }

    class BG {
        companion object {
            const val BLACK = "\u001b[40m"
            const val RED = "\u001b[41m"
            const val GREEN = "\u001b[42m"
            const val YELLOW = "\u001b[43m"
            const val BLUE = "\u001b[44m"
            const val VIOLET = "\u001b[45m"
            const val BEIGE = "\u001b[46m"
            const val WHITE = "\u001b[47m"
            const val ORANGE = "\u001b[38;2;255;153;51m"
        }
    }


    companion object {
        const val END = "\u001b[0m"

        fun colour(r: Int, g: Int, b: Int): String {
            return "\u001b[38;2;${r};${g};${b}m"
        }
    }
}


fun main(args: Array<String>) {
    println("${Colour.colour(100, 0 , 200)}${Colour.BG.YELLOW}Witold Frącek ${Colour.END}")
}