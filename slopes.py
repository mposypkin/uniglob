import interval
import math
from enum import Flag, auto

# Some auxilary functions

def compConvSlope(newRange, newValue, oldRange, oldValue):
    sp = [0, 0]
    sp[0] = (newRange[0] - newValue) / (oldRange[0] - oldValue)
    sp[1] = (newRange[1] - newValue) / (oldRange[1] - oldValue)
    return interval.Interval(sp)

def compConcSlope(newRange, newValue, oldRange, oldValue):
    sp = [0, 0]
    sp[1] = (newRange[0] - newValue) / (oldRange[0] - oldValue)
    sp[0] = (newRange[1] - newValue) / (oldRange[1] - oldValue)
    return interval.Interval(sp)

# Options
class EvalOptions(Flag):
    # Only interval evaluation is used
    INTERVAL = auto()
    # Only solpes evaluation is used
    SLOPES = auto()

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
    flagRecompRange = EvalOptions.INTERVAL

    def compbnd(self):
        if Expr.flagRecompRange is EvalOptions.SLOPES:
            c = self.x.mid()
            xc = self.x - interval.Interval([c, c])
            fc = interval.Interval([self.value, self.value])
            bnd = fc + self.S * xc
            self.range.intersec(bnd)
            return bnd

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
        etmp = makeConst(eother, self.x)
        nexpr.value = self.value + etmp.value
        nexpr.S = self.S + etmp.S
        nexpr.x = self.x
        nexpr.range = self.range + etmp.range
        nexpr.compbnd()
        return nexpr

    def __radd__(self, eother):
        nexpr = Expr()
        etmp = makeConst(eother, self.x)
        nexpr.value = self.value + etmp.value
        nexpr.S = self.S + etmp.S
        nexpr.x = self.x
        nexpr.range = self.range + etmp.range
        nexpr.compbnd()
        return nexpr

    def __sub__(self, eother):
        nexpr = Expr()
        etmp = makeConst(eother, self.x)
        nexpr.value = self.value - etmp.value
        nexpr.S = self.S - etmp.S
        nexpr.x = self.x
        nexpr.range = self.range - etmp.range
        nexpr.compbnd()
        return nexpr

    def __rsub__(self, eother):
        nexpr = Expr()
        etmp = makeConst(eother, self.x)
        nexpr.value = etmp.value - self.value
        nexpr.S = etmp.S - self.S
        nexpr.x = self.x
        nexpr.range = etmp.range - self.range
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
            sp = compConvSlope([self.range[0] ** k, self.range[1] ** k], nexpr.value, self.range, self.value)
        else:
            if self.range[0] >= 0:
                sp = compConvSlope(nexpr.range, nexpr.value, self.range, self.value)
            elif self.range[1] <= 0:
                sp = compConcSlope(nexpr.range, nexpr.value, self.range, self.value)
            else:
                sp = interval.Interval([k, k]) * (self.range ** (k - 1))
        nexpr.S = self.S * sp
        nexpr.compbnd()
        return nexpr

    def __mul__(self, eother):
        nexpr = Expr()
        etmp = makeConst(eother, self.x)
        nexpr.value = self.value * etmp.value
        nexpr.range = self.range * etmp.range
        nexpr.S = self.range * etmp.S + self.S * interval.Interval([etmp.value, etmp.value])
        nexpr.x = self.x
        nexpr.compbnd()
        return nexpr

    def __rmul__(self, eother):
        nexpr = Expr()
        etmp = makeConst(eother, self.x)
        nexpr.value = self.value * etmp.value
        nexpr.range = self.range * etmp.range
        nexpr.S = self.range * etmp.S + self.S * interval.Interval([etmp.value, etmp.value])
        nexpr.x = self.x
        nexpr.compbnd()
        return nexpr


def makeConst(expr, x):
    if isinstance(expr, int):
        etmp = const(expr, x)
    elif isinstance(expr, float):
        etmp = const(expr, x)
    else:
        etmp = expr
    return etmp

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
        sp = interval.Interval([0, 0])
        if eother.value == eother.range[0] or eother.value == eother.range[1]:
            sp = interval.cos(eother.range)
        else:
            pil = math.floor(math.floor(eother.range[0] / math.pi))
            piu = math.ceil(math.ceil(eother.range[1] / math.pi))
            if piu == pil + 1:
                if piu % 2 == 0:
                    sp = compConcSlope(self.range, self.value, eother.range, eother.value)
                else:
                    sp = compConvSlope(self.range, self.value, eother.range, eother.value)
            else:
                sp = interval.cos(eother.range)
        self.S = eother.S * sp
        self.compbnd()

class cos(Expr):
    def __init__(self, eother):
        self.x = eother.x
        self.value = math.cos(eother.value)
        self.range = interval.cos(eother.range)
        sp = interval.Interval([0, 0])
        if eother.value == eother.range[0] or eother.value == eother.range[1]:
            sp = - interval.sin(eother.range)
        else:
            pi05 = 0.5 * math.pi
            pil = math.floor(math.floor(eother.range[0] + pi05/ math.pi))
            piu = math.ceil(math.ceil(eother.range[1]  + pi05 / math.pi))
            if piu == pil + 1:
                if piu % 2 == 0:
                    sp = compConcSlope(self.range, self.value, eother.range, eother.value)
                else:
                    sp = compConvSlope(self.range, self.value, eother.range, eother.value)
            else:
                sp = - interval.sin(eother.range)
        self.S = eother.S * sp
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
            sp = compConvSlope(self.range, self.value, eother.range, eother.value)
        self.S = eother.S * sp
        self.compbnd()

# class log(Expr):
#     def __init__(self, eother, base = math.e):
#         self.x = eother.x
#         self.value = math.log(eother.value, base)
#         self.range = interval.log(eother.range, base)
#         sp = interval.Interval([0, 0])
#         if eother.value == eother.range[0] or eother.value == eother.range[1]:
#             sp = self.range
#         else:
#             sp = compConvSlope(self.range, self.value, eother.range, eother.value)
#         self.S = eother.S * sp
#         self.compbnd()




# Check code
if (__name__ == '__main__'):

    def f(x):
        # return  (x + sin(x)) * exp(-(x**2))
        # return x**4 - 10 * x**3 + 35 * x**2 - 50 * x + 24
        # return ln(x + 1.25) - 0.84 * x
        # return  0.02 * x**2 - 0.03 * exp(- (20 * (x - 0.875))**2)
        # return exp(x**2)
        return x**4 - 12 * x**3 + 47 * x**2 - 60 * x - 20 * exp(-x)
        # return x**6 - 15 * x**4 + 27 * x**2 + 250

        # return  (ident(x) + cos(ident(x) - const(0.5 * math.pi, x))) * exp(- (ident(x)**2))
        # return exp(sin(ident(x)) * (ident(x)**2 - const(4, x) * ident(x) + const(2, x)))
        # return const(4, x) * ident(x)
        # return sin(x) + sin(10 / 3 * x)
    # x = [1,7]
    x = [0.75,1.75]
    # Expr.flagRecompRange = EvalOptions.SLOPES
    ex1 = f(ident(x))
    # ex1 = f(x)
    print(ex1)
    Expr.flagRecompRange = EvalOptions.SLOPES
    print("bnd = ", ex1.compbnd())
    print(ex1)
    ex2 = f(ident(x))
    print(ex2)

