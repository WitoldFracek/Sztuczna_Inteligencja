import random


class Qlist:
    def __init__(self, *args):
        self.__list = list(args)

    def append(self, *elements):
        self.__list += list(elements)

    def select(self, selection):
        return Qlist(*[selection(elem) for elem in self.__list])

    def where(self, predicate):
        ret = Qlist()
        for elem in self.__list:
            if predicate(elem):
                ret.append(elem)
        return ret

    def order_by(self, value_accessor=lambda x: x):
        xs = self.__list
        xs.sort(key=value_accessor)
        return Qlist(*xs)

    def reverse(self):
        xs = self.__list[::-1]
        return Qlist(*xs)

    def group_by(self, value_accessor=lambda arg: arg):
        unique = set()
        for elem in self.__list:
            unique.add(value_accessor(elem))
        ret = Qlist()
        for elem in unique:
            temp = self.where(lambda x: value_accessor(x) == elem)
            ret.append(temp)
        return ret

    def sum(self):
        return sum(self.__list)

    def __len__(self):
        return len(self.__list)

    def len(self):
        return len(self)

    def __iter__(self):
        return iter(self.__list)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.__list[item]
        return Qlist(*self.__list[item])

    def __str__(self):
        return f"{str(self.__list)}"

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    ql = Qlist(1, 7, 3, 6, 5, 4, 2)
    print(ql.where(lambda x: x < 5).select(lambda x: x ** 2).order_by(lambda x: x).reverse())
    s = set()
    s.update(ql)
    print(s)
