class Color:

    END = '\33[0m'

    @staticmethod
    def color(r, g, b):
        return f'\033[38;2;{r};{g};{b}m'

    class Style:
        BOLD = '\33[1m'
        ITALIC = '\33[3m'
        URL = '\33[4m'
        BLINK = '\33[5m'
        BLINK2 = '\33[6m'
        SELECTED = '\33[7m'

    class FG:
        BLACK = '\33[30m'
        RED = '\33[31m'
        GREEN = '\33[32m'
        YELLOW = '\33[33m'
        BLUE = '\33[34m'
        VIOLET = '\33[35m'
        BEIGE = '\33[36m'
        WHITE = '\33[37m'
        ORANGE = '\033[38;2;255;128;0m'

    class BG:
        BLACK = '\33[40m'
        RED = '\33[41m'
        GREEN = '\33[42m'
        YELLOW = '\33[43m'
        BLUE = '\33[44m'
        VIOLET = '\33[45m'
        BEIGE = '\33[46m'
        WHITE = '\33[47m'
        ORANGE = '\033[38;2;255;153;51m'


if __name__ == '__main__':
    print(f'{Color.color(255, 200, 0)}RED{Color.END} Heeeee')
