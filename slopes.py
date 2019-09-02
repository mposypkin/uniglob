import sys
import math
import interval
from enum import Flag, auto

# Some auxilary functions

def comp_conv_slope(a, b, c, va, vb, vc, dc):
    """
    Computes the slope for a convex function
    :param a: left bound of the interval
    :param b: right bound of the interval
    :param c: point in the interval
    :param va: value at the left end
    :param vb: value at the right end
    :param vc: point in the interval
    :param dc: derivative at this point
    :return: the computed slope
    """
    sp = [0, 0]
    if a == c:
        sp[0] = dc
    else:
        sp[0] = (va - vc) / (a - c)
    if b == c:
        sp[1] = dc
    else:
        sp[1] = (vb - vc) / (b - c)
    return interval.Interval(sp)

def comp_conc_slope(a, b, c, va, vb, vc, dc):
    """
    Computes the slope for a cocave function
    :param a: left bound of the interval
    :param b: right bound of the interval
    :param c: point in the interval
    :param va: value at the left end
    :param vb: value at the right end
    :param vc: point in the interval
    :param dc: derivative at this point
    :return: the computed slope
    """
    sp = [0, 0]
    if a == c:
        sp[1] = dc
    else:
        sp[1] = (va - vc) / (a - c)
    if b == c:
        sp[0] = dc
    else:
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
        """
        The constructor
        :param x: the source interval for x
        :param val: the point in the interval to compute slope (if different from the center
        """
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


    def comp_slopes_bound(self):
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
            nexpr.comp_slopes_bound()
        return nexpr


    def __add__(self, eother):
        nexpr = Slope(self.x)
        etmp = valueToSlope(eother, self.x)
        nexpr.value = self.value + etmp.value
        nexpr.S = self.S + etmp.S
        nexpr.x = self.x
        nexpr.range = self.range + etmp.range
        if Slope.flagRecompRange:
            nexpr.comp_slopes_bound()
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
            nexpr.comp_slopes_bound()
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
            nexpr.comp_slopes_bound()
        return nexpr

    def __rmul__(self, eother):
        return self.__mul__(eother)

    def __pow__(self, k):
        nexpr = Slope(self.x)
        nexpr.value = self.value ** k
        nexpr.range = self.range ** k
        if k == 2:
            sp = self.range + interval.Interval([self.value, self.value])
        elif k % 2:
            sp = comp_conv_slope(self.range[0], self.range[1], self.value,
                                 self.range[0] ** k, self.range[1] ** k, nexpr.value, k * self.value ** (k - 1))
        else:
            if self.range[0] >= 0:
                sp = comp_conv_slope(self.range[0], self.range[1], self.value,
                                     self.range[0] ** k, self.range[1] ** k, nexpr.value, k * self.value ** (k - 1))
            elif self.range[1] <= 0:
                sp = comp_conc_slope(self.range[0], self.range[1], self.value,
                                     self.range[0] ** k, self.range[1] ** k, nexpr.value, k * self.value ** (k - 1))
            else:
                sp = interval.Interval([k, k]) * (self.range ** (k - 1))
        nexpr.S = self.S * sp
        if Slope.flagRecompRange:
            nexpr.comp_slopes_bound()
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
                    sp = comp_conc_slope(eother.range[0], eother.range[1], eother.value,
                                         math.sin(eother.range[0]), math.sin(eother.range[1]), self.value, math.cos(self.value))
                else:
                    sp = comp_conv_slope(eother.range[0], eother.range[1], eother.value,
                                         math.sin(eother.range[0]), math.sin(eother.range[1]), self.value, math.cos(eother.value))
            else:
                sp = interval.cos(eother.range)
        self.S = eother.S * sp
        if Slope.flagRecompRange:
            self.comp_slopes_bound()

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
                    sp = comp_conc_slope(eother.range[0], eother.range[1], eother.value,
                                         math.cos(eother.range[0]), math.cos(eother.range[1]), self.value, -math.sin(eother.value))
                else:
                    sp = comp_conv_slope(eother.range[0], eother.range[1], eother.value,
                                         math.cos(eother.range[0]), math.cos(eother.range[1]), self.value, -math.sin(eother.value))
            else:
                sp = - interval.sin(eother.range)
        self.S = eother.S * sp
        if Slope.flagRecompRange:
            self.comp_slopes_bound()


class exp(Slope):
    def __init__(self, eother):
        self.x = eother.x
        self.value = math.exp(eother.value)
        self.range = interval.exp(eother.range)
        sp = interval.Interval([0, 0])
        sp = comp_conv_slope(eother.range[0], eother.range[1], eother.value,
                             math.exp(eother.range[0]), math.exp(eother.range[1]), self.value, self.value)
        self.S = eother.S * sp
        if Slope.flagRecompRange:
            self.comp_slopes_bound()

class log(Slope):
    def __init__(self, eother):
        self.x = eother.x
        self.value = math.log(eother.value)
        self.range = interval.log(eother.range)
        sp = comp_conc_slope(eother.range[0], eother.range[1], eother.value,
                             math.log(eother.range[0]), math.log(eother.range[1]), self.value, 1/eother.value)
        self.S = eother.S * sp
        if Slope.flagRecompRange:
            self.comp_slopes_bound()


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
        # return x**2 - 4 * x + 2
        # return  (x + sin(x)) * exp(-(x**2))
        # return x**4 - 10 * x**3 + 35 * x**2 - 50 * x + 24
        return (log(x + 1.25) - 0.84 * x)**2
        # return  0.02 * x**2 - 0.03 * exp(- (20 * (x - 0.875))**2)
        # return exp(x**2)
        # return x**4 - 12 * x**3 + 47 * x**2 - 60 * x - 20 * exp(-x)
        # return x**6 - 15 * x**4 + 27 * x**2 + 250

        # return  (ident(x) + cos(ident(x) - const(0.5 * math.pi, x))) * exp(- (ident(x)**2))
        # return exp(sin(ident(x)) * (ident(x)**2 - const(4, x) * ident(x) + const(2, x)))
        # return const(4, x) * ident(x)
        # return sin(x) + sin(10 / 3 * x)
    # x = [1,7]
    x = [0.75,1.75]
    Slope.flagRecompRange = False
    s = Slope(x)
    ex1 = f(s)
    Slope.flagRecompRange = True
    print("Slope = ", ex1)
    print("bnd = ", ex1.comp_slopes_bound())
    ex2 = f(Slope(x))
    print("Improved slope = ", ex2)
    print("bnd = ", ex2.comp_slopes_bound())

