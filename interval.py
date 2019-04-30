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

    def __neg__(self):
        ninterval = Interval(self.x)
        ninterval.x[0] = - self.x[1]
        ninterval.x[1] = - self.x[0]
        return ninterval

    def __add__(self, other):
        ninterval = Interval(self.x)
        ninterval.x[0] = self.x[0] + other.x[0]
        ninterval.x[1] = self.x[1] + other.x[1]
        return ninterval

    def __sub__(self, other):
        ninterval = Interval(self.x)
        ninterval.x[0] = self.x[0] - other.x[1]
        ninterval.x[1] = self.x[1] - other.x[0]
        return ninterval

    def __pow__(self, other):
        ninterval = Interval(self.x)
        if other == 2:
            u = self.x[0] * self.x[0]
            v = self.x[1] * self.x[1]
            ninterval.x[1] = max(u, v)
            if self.x[0] <= 0 and self.x[1] >= 0:
                ninterval.x[0] = 0
            else:
                ninterval.x[0] = min(u, v)
        return ninterval

    def __mul__(self, other):
        v = [self.x[0] * other.x[0], self.x[0] * other.x[1], self.x[1] * other.x[0], self.x[1] * other.x[1]]
        b = [min(v), max(v)]
        return Interval(b)




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
    print(-x)
    print(x**2)
    y = Interval([5,6])
    print(x + y)
    print(x * y)

    print(cos(Interval([0, math.pi / 2])))
    print(cos(Interval([- math.pi / 2, math.pi / 2])))
    print(cos(Interval([- 3 * math.pi / 2, - math.pi / 2])))