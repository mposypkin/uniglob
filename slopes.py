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
    # If true then reeval range at every step
    flagRecompRange = False

    def compbnd(self):
        if Expr.flagRecompRange:
            c = self.x.mid()
            xc = self.x - interval.Interval([c, c])
            fc = interval.Interval([self.value, self.value])
            bnd = fc + self.S * xc
            print("bnd = ", bnd)
            self.range.intersec(bnd)


    def __repr__(self):
        return "value = " + str(self.value) + ", slope = " + str(self.S) + ", range = " + str(self.range) + ", x = " + str(self.x)

    def __neg__(self):
        nexpr = Expr()
        nexpr.value = - self.value
        nexpr.S = - self.S
        nexpr.x = self.x
        nexpr.range = - self.range
        nexpr.compbnd()
        return nexpr


    def __add__(self, eother):
        nexpr = Expr()
        nexpr.value = self.value + eother.value
        nexpr.S = self.S + eother.S
        nexpr.x = self.x
        nexpr.range = self.range + eother.range
        nexpr.compbnd()
        return nexpr

    def __sub__(self, other):
        nexpr = Expr()
        nexpr.value = self.value - other.value
        nexpr.S = self.S - other.S
        nexpr.x = self.x
        nexpr.range = self.range - other.range
        nexpr.compbnd()
        return nexpr


    def __pow__(self, k):
        nexpr = Expr()
        nexpr.value = self.value ** k
        nexpr.x = self.x
        nexpr.range = self.range ** k
        sp = interval.Interval([0,0])
        if self.value == self.range[0] or self.value == self.range[1]:
            sp = interval.Interval([k, k]) * (self.range ** (k - 1))
        elif k == 2:
            sp = self.range + interval.Interval([self.value, self.value])
        elif k % 2:
            sp[0] = (self.range[0] ** k - nexpr.value) / (self.range[0] - self.value)
            sp[1] = (self.range[1] ** k - nexpr.value) / (self.range[1] - self.value)
        else:
            if self.range[0] >= 0:
                sp[0] = (nexpr.range[0] - nexpr.value) / (self.range[0] - self.value)
                sp[1] = (nexpr.range[1] - nexpr.value) / (self.range[1] - self.value)
            elif self.range[1] <= 0:
                sp[1] = (nexpr.range[0] - nexpr.value) / (self.range[0] - self.value)
                sp[0] = (nexpr.range[1] - nexpr.value) / (self.range[1] - self.value)
            else:
                sp = interval.Interval([k, k]) * (self.range ** (k - 1))
        nexpr.S = self.S * sp
        nexpr.compbnd()
        return nexpr

    def __mul__(self, eother):
        nexpr = Expr()
        nexpr.value = self.value * eother.value
        nexpr.range = self.range * eother.range
        nexpr.S = self.range * eother.S + self.S * interval.Interval([eother.value, eother.value])
        nexpr.x = self.x
        nexpr.compbnd()
        return nexpr


    # def __call__(self, eother):
    #     nexpr = Expr()
    #     return nexpr

# Constant expression
class const(Expr):
    def __init__(self, value, x):
        self.value = value
        self.S = interval.Interval([0,0])
        self.x = interval.Interval([x[0], x[1]])
        self.range = interval.Interval([value, value])

# Literal
class ident(Expr):
    def __init__(self, x):
        self.value = 0.5 * (x[0] + x[1])
        self.S = interval.Interval([1,1])
        self.x = interval.Interval([x[0], x[1]])
        self.range = interval.Interval([x[0], x[1]])


class sin(Expr):
    def __init__(self, eother):
        self.x = eother.x
        self.value = math.sin(eother.value)
        self.range = interval.sin(eother.range)
        y = interval.cos(eother.range)
        self.S = eother.S * y
        self.compbnd()


class exp(Expr):
    def __init__(self, eother):
        self.x = eother.x
        self.value = math.exp(eother.value)
        self.range = interval.exp(eother.range)
        sp = interval.Interval([0, 0])
        if eother.value == eother.range[0] or eother.value == eother.range[1]:
            sp = self.range
        else:
            sp[0] = (self.range[0] - self.value) / (eother.range[0] - eother.value)
            sp[1] = (self.range[1] - self.value) / (eother.range[1] - eother.value)
        self.S = eother.S * sp
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
        # return sin(ident(x)) + sin(const(10 / 3, x) * ident(x))
        return exp(ident(x)**2)
        # return  (ident(x) + sin(ident(x))) * exp(- (ident(x)**2))
        # return ident(x)**6 - const(15, x) * ident(x)**4 + const(27, x) * ident(x)**2 + const(250,x)
        # return ident(x)**4 - const(10, x) * ident(x)**3 + const(35, x) * ident(x)**2 - const(50, x) * ident(x) + const(24,x)
        # return ident(x) * (ident(x)**2 - const(4, x) * ident(x) + const(2, x))
        # return const(4, x) * ident(x)
    # x = [1,7]
    x = [0.75,1.75]
    ex1 = f(x)
    print(ex1)
    Expr.flagRecompRange = True
    ex1.compbnd()
    print(ex1)
    ex2 = f(x)
    # Expr.flagRecompRange = True
    # ex.compbnd()
    print(ex2)

