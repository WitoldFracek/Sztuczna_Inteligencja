

class Variable:
    def __init__(self, coordinates: (int, int), domain, identifier=None):
        self.__x, self.__y = coordinates
        self.__domain = {*domain}
        self.__available_values = {*domain}
        self.__identifier = identifier
        self.value = None
        self.modification_history: dict = {}

    def refill(self):
        self.__available_values = self.__domain.copy()

    @property
    def all_checked(self) -> bool:
        return len(self.__available_values) == 0

    @property
    def position(self) -> (int, int):
        return self.__x, self.__y

    @property
    def domain(self) -> set:
        return self.__domain

    @property
    def available_values(self) -> set:
        return self.__available_values

    @property
    def id(self):
        return self.__identifier


if __name__ == '__main__':
    xs = [1, None, 1]
    print(sum(xs))



