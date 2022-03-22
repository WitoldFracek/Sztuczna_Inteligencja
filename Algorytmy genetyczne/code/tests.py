import random
import matplotlib.pyplot as pyl

def chaos(r, x0, steps):
    ret = [x0]
    x = x0
    for _ in range(steps):
        x = r * x * (1 - x)
        ret.append(x)
    return ret

class DataCollector:
    def __init__(self):
        self.__measures = []

    def __add__(self, other):
        self.__measures += other
        return self
        

if __name__ == '__main__':
    dc = DataCollector()
    xs = [1, 2, 3]
    x = [1, 4, 8]
    dc += xs
    dc += x
    print(dc.__dict__)
    import winsound
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)


