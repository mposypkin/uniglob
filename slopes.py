import sys
import math
import interval
from enum import Flag, auto

# Some auxilary functions

def compConvSlope(a, b, c, va, vb, vc):
    sp = [0, 0]
    sp[0] = (va - vc) / (a - c)
    sp[1] = (vb - vc) / (b - c)
    return interval.Interval(sp)

def compConcSlope(a, b, c, va, vb, vc):
    sp = [0, 0]
    sp[1] = (va - vc) / (a - c)
    sp[0] = (vb - vc) / (b - c)
    return interval.Interval(sp)

# Generic class for expressions
class Slope:
    """
    A class for slopes


    """
    # If true then reeval range at every step
    flagRecompRange = False

    def __init__(self, x, val = None):
        # The value at some point of the interval
        if val == None:
            self.value = 0.5 * (x[0] + x[1])
        else:
            self.value = val
        # The Slope
        self.S = interval.Interval([1,1])
        # The Source Interval
        self.x = interval.Interval([x[0], x[1]])
        # The resulting range
        self.range = interval.Interval([x[0], x[1]])


    def compSlopesBound(self):
        """
        Evaluates the slopes bound
        :return:
        the computed slopes bound
        """
        c = self.x.mid()
        xc = self.x - interval.Interval([c, c])
        fc = interval.Interval([self.value, self.value])
        bnd = fc + self.S * xc
        self.range.intersec(bnd)
        return bnd

    def __repr__(self):
        return "value = " + str(self.value) + ", slope = " + str(self.S) + ", range = " + str(self.range) + ", x = " + str(self.x)

    def __neg__(self):
        nexpr = Slope(self.x)
        nexpr.value = - self.value
        nexpr.S = - self.S
        nexpr.x = self.x
        nexpr.range = - self.range
        if Slope.flagRecompRange:
            nexpr.compSlopesBound()
        return nexpr


    def __add__(self, eother):
        nexpr = Slope(self.x)
        etmp = valueToSlope(eother, self.x)
        nexpr.value = self.value + etmp.value
        nexpr.S = self.S + etmp.S
        nexpr.x = self.x
        nexpr.range = self.range + etmp.range
        if Slope.flagRecompRange:
            nexpr.compSlopesBound()
        return nexpr

    def __radd__(self, eother):
        return self.__add__(eother)

    def __sub__(self, eother):
        nexpr = Slope(self.x)
        etmp = valueToSlope(eother, self.x)
        nexpr.value = self.value - etmp.value
        nexpr.S = self.S - etmp.S
        nexpr.x = self.x
        nexpr.range = self.range - etmp.range
        if Slope.flagRecompRange:
            nexpr.compSlopesBound()
        return nexpr

    def __rsub__(self, eother):
        etmp = valueToSlope(eother, self.x)
        return etmp.__sub__(self)

    def __mul__(self, eother):
        nexpr = Slope(self.x)
        etmp = valueToSlope(eother, self.x)
        nexpr.value = self.value * etmp.value
        nexpr.S = self.range * etmp.S + self.S * etmp.range
        nexpr.x = self.x
        nexpr.range = self.range * etmp.range
        if Slope.flagRecompRange:
            nexpr.compSlopesBound()
        return nexpr

    def __rmul__(self, eother):
        return self.__mul__(eother)

    def __pow__(self, k):
        nexpr = Slope(self.x)
        nexpr.value = self.value ** k
        nexpr.range = self.range ** k
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
        if Slope.flagRecompRange:
            nexpr.compSlopesBound()
        return nexpr


def valueToSlope(expr, x):
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
class const(Slope):
    def __init__(self, value, x):
        self.value = value
        self.S = interval.Interval([0,0])
        self.x = interval.Interval([x[0], x[1]])
        self.range = interval.Interval([value, value])

# Literal
# class ident(Slope):
#     def __init__(self, x):
#         self.value = 0.5 * (x[0] + x[1])
#         self.S = interval.Interval([1,1])
#         self.x = interval.Interval([x[0], x[1]])
#         self.range = interval.Interval([x[0], x[1]])


class sin(Slope):
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
                    sp = compConcSlope(eother.range[0], eother.range[1], eother.value,
                                       math.sin(eother.range[0]), math.sin(eother.range[1]), self.value )
                else:
                    sp = compConcSlope(eother.range[0], eother.range[1], eother.value,
                                       math.sin(eother.range[0]), math.sin(eother.range[1]), self.value )
            else:
                sp = interval.cos(eother.range)
        self.S = eother.S * sp
        if Slope.flagRecompRange:
            self.compSlopesBound()

class cos(Slope):
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
        if Slope.flagRecompRange:
            self.compSlopesBound()


class exp(Slope):
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
        if Slope.flagRecompRange:
            self.compSlopesBound()

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
#         self.compSlopesBound()




# Check code
if (__name__ == '__main__'):

    # help(Slope)
    def f(x):
        return x**2 - 4 * x + 2
        # return  (x + sin(x)) * exp(-(x**2))
        # return x**4 - 10 * x**3 + 35 * x**2 - 50 * x + 24
        # return ln(x + 1.25) - 0.84 * x
        # return  0.02 * x**2 - 0.03 * exp(- (20 * (x - 0.875))**2)
        # return exp(x**2)
        # return x**4 - 12 * x**3 + 47 * x**2 - 60 * x - 20 * exp(-x)
        # return x**6 - 15 * x**4 + 27 * x**2 + 250

        # return  (ident(x) + cos(ident(x) - const(0.5 * math.pi, x))) * exp(- (ident(x)**2))
        # return exp(sin(ident(x)) * (ident(x)**2 - const(4, x) * ident(x) + const(2, x)))
        # return const(4, x) * ident(x)
        # return sin(x) + sin(10 / 3 * x)
    x = [1,7]
    # x = [0.75,1.75]
    Slope.flagRecompRange = False
    s = Slope(x)
    ex1 = f(s)
    Slope.flagRecompRange = True
    print("Slope = ", ex1)
    print("bnd = ", ex1.compSlopesBound())
    ex2 = f(Slope(x))
    print(ex2)

