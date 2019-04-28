import math

class Interval:
    x = [0, 0]

    def __init__(self, x):
        self.x = x.copy()


    def __repr__(self):
        return "[" + str(self.x[0]) + ", " + str(self.x[1]) + "]"

    def __getitem__(self, item):
        return self.x[item]

    def __setitem__(self, key, value):
        self.x.__setitem__(key, value)


def cos(x):
    y = [math.cos(x[0]), math.cos(x[1])]
    pi2 = 2 * math.pi
    if math.ceil(x[0]/pi2) <= math.floor(x[1]/pi2):
        b = 1
    else:
        b = max(y)

    if math.ceil((x[0] - math.pi)/pi2) <= math.floor((x[1] - math.pi)/pi2):
        a = -1
    else:
        a = min(y)
    return Interval([a,b])

if (__name__ == '__main__'):

    x = Interval([-1, 2])
    print(x)

    print(cos(Interval([0, math.pi / 2])))
    print(cos(Interval([- math.pi / 2, math.pi / 2])))
    print(cos(Interval([- 3 * math.pi / 2, - math.pi / 2])))