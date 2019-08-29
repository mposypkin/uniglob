# from lipexpr import *
import interval
# from advlip import *
import slopes as slp
import numpy as np
import sympy as smp


class Problem:
    def __init__(self, name, range, xvar, fexpr):
        self.name = name
        self.range = range
        self.fexpr = fexpr
        self.xvar = xvar
    def __repr__(self):
        return "[" + self.name + "] min " + str(self.fexpr) + " on " + str(self.range)

class SolutionInfo:
    def __init__(self, value, x, steps):
        self.value = value
        self.x = x
        self.steps = steps

    def __repr__(self):
        return str(self.value) + "  = f(" + str(self.x) + ") obtained in " + str(self.steps) + " steps"

def simpleBnB(problem, eps, solinfo):
    P = []
    P.append(interval.Interval(problem.range))
    fr = solinfo.value
    maxsteps = solinfo.steps
    steps = 0
    f = smp.lambdify(problem.xvar, problem.fexpr)
    fslp = smp.lambdify(problem.xvar, problem.fexpr, slp)

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
    solinfo.value = fr
    solinfo.x = xr
    solinfo.steps = steps

def pijavBnB(problem, eps, solinfo):
    class Sub:
        def __init__(self, s1, s2, ival):
            self.s1 = s1
            self.s2 = s2
            self.ival = ival
            self.c = (self.s1.value - self.s2.value + self.ival[1] * self.s2.S[1] - self.ival[0] * self.s1.S[0])/(self.s2.S[1] - self.s1.S[0])
            self.bound = self.s1.value + (self.c - self.ival[0]) * self.s1.S[0]
            boundcheck = self.s2.value + (self.c - self.ival[1]) * self.s2.S[1]
            print("bound = ", self.bound, ", check ", boundcheck)

        def bnd(self):
            return self.bound

        def __repr__(self):
            return "s1 = " + str(self.s1) + ", s2 = " + str(self.s2) + ", interval = " + str(self.ival)\
                    + "c =" + str(self.c) + ", bound = " + str(self.bound)


    print("Hi")
    f = smp.lambdify(problem.xvar, problem.fexpr)
    fslp = smp.lambdify(problem.xvar, problem.fexpr, slp)
    P = []
    ival = interval.Interval(problem.range)
    s1 = fslp(slp.Slope(ival, ival[0]))
    s2 = fslp(slp.Slope(ival, ival[1]))
    P.append(Sub(s1, s2, ival))
    print(P)
    # return
    fr = solinfo.value
    maxsteps = solinfo.steps
    steps = 0

    # Expr.flagRecompRange = True
    while len(P) > 0 and steps <= maxsteps:
        steps = steps + 1
        sub = P.pop(0)
        if fr - sub.bnd() > eps:
            x1 = interval.Interval([sub.ival[0], sub.c])
            # print("Add ", x1)
            x2 = interval.Interval([sub.c, sub.ival[1]])
            # print("Add ", x2)
            ns = fslp(slp.Slope(sub.ival, sub.c))
            if ns.value < fr:
                fr = ns.value
                xr = sub.c
            P.append(Sub(sub.s1, ns, x1))
            P.append(Sub(ns, sub.s2, x2))
    solinfo.value = fr
    solinfo.x = xr
    solinfo.steps = steps


x = smp.symbols('x')
fexpr = smp.sin(x) + smp.sin(10/3 * x)
problem = Problem("problem1", [2.7, 7.5], x, fexpr)

solinfo = SolutionInfo(10000000, 0, 10000)
simpleBnB(problem, 1e-3, solinfo)
print("For a problem ", problem, ", found solution ", solinfo)

solinfo = SolutionInfo(10000000, 0, 10000)
pijavBnB(problem, 1e-3, solinfo)
print("For a problem ", problem, ", found solution ", solinfo)