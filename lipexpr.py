import interval
import math


# Generic class for expressions
class Expr:
    # The value in the middle of the interval
    value = 0
    # The Lipschitz constant
    L = 0
    # The Source Interval
    x = [0, 0]
    # The resulting range
    range = [0, 0]

    def compbnd(self):
        hl = 0.5 * (self.x[1] - self.x[0])
        self.range[0] = self.value - self.L * hl
        self.range[1] = self.value + self.L * hl

    def __str__(self):
        return "value = " + str(self.value) + ", Lip = " + str(self.L) + ", range = " + str(self.range)

    def __add__(self, eother):
        nexpr = Expr()
        nexpr.value = self.value + eother.value
        nexpr.L = self.L + eother.L
        nexpr.x = self.x
        nexpr.compbnd()
        return nexpr

    def __call__(self, eother):
        nexpr = Expr()
        return nexpr

# Constant expression
class const(Expr):
    def __init__(self, value):
        self.value = value
        self.range = [value, value]

# Literal
class ident(Expr):
    def __init__(self, x):
        self.value = 0.5 * (x[0] + x[1])
        self.L = 1
        self.x = x
        self.range = x


# Helper
def getLip(x):
    return max(map(abs, x))

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
