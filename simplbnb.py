# from lipexpr import *
import interval
# from advlip import *
import slopes as slp
import numpy as np
import sympy as smp

# def f(x):
#     return -(ident(x) * sin(ident(x)))
# xrange = [0, 10]

x = smp.symbols('x')
fexpr = smp.sin(x) + smp.sin(10/3 * x)
f = smp.lambdify(x, fexpr)
fslp =  smp.lambdify(x, fexpr, slp)
xrange = interval.Interval([2.7, 7.5])

# def f(x):
#     return sin(ident(x))
# xrange = interval.Interval([2.7, 7.5])


P = []
P.append(xrange)
fr = 100000000
eps = 1e-3
maxsteps = 10000
steps = 0
# Expr.flagRecompRange = True
while len(P) > 0 and steps <= maxsteps:
    steps = steps + 1
    x = P.pop(0)
    e = fslp(slp.Slope(x))
    print("Treat ", x)
    if e.value < fr:
        xr = 0.5 * (e.x[0] + e.x[1])
        fr = e.value
        print("e: <", e, ">\n")
    if fr - e.range[0] > eps:
        m = 0.5 * (x[0] + x[1])
        x1 = interval.Interval([x[0], m])
        print("Add ", x1)
        x2 = interval.Interval([m, x[1]])
        print("Add ", x2)
        P.append(x1)
        P.append(x2)

print("Steps performed: " + str(steps))
print("Record: " + str(-fr) + " at " + str(xr))
print("Hi")
print("Check: " + str(f(xr)))
print("By")