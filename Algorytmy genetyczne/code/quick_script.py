

class Complex:
    def __init__(self, r, i):
        self.real = r
        self.imag = i

    def __str__(self):
        return f'{self.real} + {self.imag}i'

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass


def add(c1, c2):
    real = c1.real + c2.real
    imag = c1.imag + c2.imag
    return Complex(real, imag)


if __name__ == '__main__':
    c1 = Complex(1, 0)
    c2 = Complex(0, 1)
    sum = add(c1, c2)
    sum = c1 + c2
    print(sum)




