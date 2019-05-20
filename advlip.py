import sys
import math
import interval


# Generic class for expressions
class Expr:

    # If true then reeval range at every step
    flagRecompRange = False

    def __init__(self):
        # The value in the middle of the interval
        self.value = 0
        # The Lipschitz constant
        self.L = sys.float_info.max
        # The Source Interval
        self.x = interval.Interval([-sys.float_info.max, sys.float_info.max])
        # The resulting range
        self.range = interval.Interval([-sys.float_info.max, sys.float_info.max])

    def getbnd(self):
        hl = 0.5 * (self.x[1] - self.x[0])
        bnd = interval.Interval([self.value - self.L * hl, self.value + self.L * hl])
        self.range.intersec(bnd)
        return bnd

    def compbnd(self):
        if Expr.flagRecompRange:
            return self.getbnd()

    def __repr__(self):
        return "value = " + str(self.value) + ", Lip = " + str(self.L) + ", range = " + str(self.range) + ", x = " + str(self.x)

    def __neg__(self):
        nexpr = Expr()
        nexpr.value = - self.value
        nexpr.L = self.L
        nexpr.x = self.x
        nexpr.compbnd()
        return nexpr


    def __add__(self, eother):
        nexpr = Expr()
        etmp = makeConst(eother, self.x)
        nexpr.value = self.value + etmp.value
        nexpr.L = self.L + etmp.L
        nexpr.x = self.x
        nexpr.compbnd()
        return nexpr

    def __radd__(self, eother):
        return self.__add__(eother)

    def __mul__(self, eother):
        nexpr = Expr()
        nexpr.value = self.value * eother.value
        mself = max(map(abs,self.range))
        mother = max(map(abs, eother.range))
        nexpr.L = self.L * mother + eother.L * mself
        nexpr.x = self.x
        nexpr.compbnd()
        return nexpr


    # def __call__(self, eother):
    #     nexpr = Expr()
    #     return nexpr

# Constant expression
class const(Expr):
    def __init__(self, value, x):
        Expr.__init__(self)
        self.L = 0
        self.value = value
        self.range = interval.Interval([value, value])
        self.x = x

# Literal
class ident(Expr):
    def __init__(self, x):
        Expr.__init__(self)
        self.value = 0.5 * (x[0] + x[1])
        self.L = 1
        self.x = x
        self.range[0] = x[0]
        self.range[1] = x[1]


# Helper
def getLip(x):
    return max(map(abs, x))

# The sinus function
class sin(Expr):
    def __init__(self, eother):
        self.x = eother.x
        self.value = math.sin(eother.value)
        y = interval.cos(self.range)
        L = getLip(y)
        self.L = L * eother.L
        self.compbnd()

def makeConst(expr, x):
    if isinstance(expr, int):
        etmp = const(expr, x)
    elif isinstance(expr, float):
        etmp = const(expr, x)
    else:
        etmp = expr
    return etmp

if (__name__ == '__main__'):
    x = ident([0,1])
    print("x + 1 = ", x + 1 )
    print("x + 1 = ", (x + 1).getbnd())