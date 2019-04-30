import interval
import math


# Generic class for expressions
class Expr:
    # The value in the middle of the interval
    value = 0
    # The Slope
    S = interval.Interval([0, 0])
    # The resulting range
    range = interval.Interval([0, 0])
    # The Source Interval
    x = interval.Interval([0, 0])

    def compbnd(self):
        hl = 0.5 * (self.x[1] - self.x[0])
        self.range[0] = self.value - self.L * hl
        self.range[1] = self.value + self.L * hl

    def __repr__(self):
        return "value = " + str(self.value) + ", slope = " + str(self.S) + ", range = " + str(self.range) + ", x = " + str(self.x)

    def __neg__(self):
        nexpr = Expr()
        nexpr.value = - self.value
        nexpr.S = - self.S
        nexpr.x = self.x
        nexpr.range = - self.range
        return nexpr


    def __add__(self, eother):
        nexpr = Expr()
        nexpr.value = self.value + eother.value
        nexpr.S = self.S + eother.S
        nexpr.x = self.x
        nexpr.range = self.range + eother.range
        return nexpr

    def __sub__(self, other):
        nexpr = Expr()
        nexpr.value = self.value - other.value
        nexpr.S = self.S - other.S
        nexpr.x = self.x
        nexpr.range = self.range - other.range
        return nexpr


    def __pow__(self, other):
        nexpr = Expr()
        nexpr.value = self.value ** other
        nexpr.x = self.x
        nexpr.range = self.range ** other
        if other == 2:
            nexpr.S = self.S * (self.range + interval.Interval([self.value, self.value]))
        return nexpr

    def __mul__(self, eother):
        nexpr = Expr()
        nexpr.value = self.value * eother.value
        nexpr.range = self.range * eother.range
        nexpr.S = self.range * eother.S + self.S * interval.Interval([eother.value, eother.value])
        nexpr.x = self.x
        return nexpr


    # def __call__(self, eother):
    #     nexpr = Expr()
    #     return nexpr

# Constant expression
class const(Expr):
    def __init__(self, value, x):
        self.value = value
        self.S = interval.Interval([0,0])
        self.x = interval.Interval(x)
        self.range = interval.Interval([value, value])

# Literal
class ident(Expr):
    def __init__(self, x):
        self.value = 0.5 * (x[0] + x[1])
        self.S = interval.Interval([1,1])
        self.x = interval.Interval(x)
        self.range = interval.Interval(x)



# The sinus function
class sin(Expr):
    def __init__(self, eother):
        self.x = eother.x
        self.value = math.sin(eother.value)
        y = interval.cos(self.x)
        print(self.x)
        L = getLip(y)
        # L = 1
        print(L)
        self.L = L * eother.L
        self.compbnd()

# Check code
if (__name__ == '__main__'):
    x = [1,3]
    s1 = const(42, x)
    s2 = ident(x)
    s3 = - s2
    s = s1 + s3
    print(s3)
    print(s1)
    print(s)

    def f(x):
        return ident(x)**2 - const(4, x) * ident(x) + const(2, x)
        # return const(4, x) * ident(x)
    print(f([1,7]))
