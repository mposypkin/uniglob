# from lipexpr import *
import interval
# from advlip import *
import slopes as slp
import numpy as np
import sympy as smp


class Problem:
    """
    A class for defining a problem
    """
    def __init__(self, name, range, xvar, fexpr):
        """
        Constructor
        :param name: name of the problem
        :param range: range of the variable
        :param xvar: symbol of a variable
        :param fexpr: objective expression
        """
        self.name = name
        self.range = range
        self.fexpr = fexpr
        self.xvar = xvar

    def __repr__(self):
        return "[" + self.name + "] min " + str(self.fexpr) + " on " + str(self.range)

class SolutionInfo:
    """
    A class for storing solution information
    """
    def __init__(self, value, x):
        """
        Constructor
        :param value: value of the solution
        :param x: vector
        """
        self.value = value
        self.x = x

    def __repr__(self):
        return str(self.value) + "  = f(" + str(self.x) + ")"

def simple_bnb(problem, eps, solinfo, maxsteps):
    """
    A standard slope based BnB solver
    :param problem: problem to solve
    :param eps: tolerance
    :param solinfo: information for the solution
    :return: number of steps actually done
    """
    P = []
    P.append(interval.Interval(problem.range))
    fr = solinfo.value
    steps = 0
    f = smp.lambdify(problem.xvar, problem.fexpr)
    fslp = smp.lambdify(problem.xvar, problem.fexpr, slp)

    # Expr.flagRecompRange = True
    while len(P) > 0 and steps <= maxsteps:
        steps = steps + 1
        x = P.pop(0)
        e = fslp(slp.Slope(x))
        if e.value < fr:
            xr = 0.5 * (e.x[0] + e.x[1])
            fr = e.value
        if fr - e.range[0] > eps:
            m = 0.5 * (x[0] + x[1])
            x1 = interval.Interval([x[0], m])
            x2 = interval.Interval([m, x[1]])
            P.append(x1)
            P.append(x2)
    solinfo.value = fr
    solinfo.x = xr
    return steps

def pijavBnB(problem, eps, solinfo, maxsteps):
    """
    Pijavsky method enhanced with slopes
    :param problem: problem to solver
    :param eps: tolerance
    :param solinfo: obtained solution
    :return: actual steps performed
    """
    class Sub:
        def __init__(self, s1, s2, ival):
            self.s1 = s1
            self.s2 = s2
            self.ival = ival
            a = ival[0]
            b = ival[1]
            La = s1.S[0]
            Lb = s2.S[1]
            va = s1.value
            vb = s2.value
            self.c = (vb - va + La * a - Lb * b)/(La - Lb)
            self.bound = va + La * (self.c - a)
            boundcheck = vb + Lb * (self.c - b)
            if abs(self.bound - boundcheck) > 0.01:
                print("bound = ", self.bound, ", check ", boundcheck)
                print("a = ", a, ", b = ", b, ", va = ", va, ", vb = ", vb, ", La = ", La, ", Lb = ", Lb)
                print("s1 = ", s1)
                print("s2 = ", s2)

        def bnd(self):
            return self.bound

        def __repr__(self):
            return "s1 = " + str(self.s1) + ", s2 = " + str(self.s2) + ", interval = " + str(self.ival)\
                    + "c =" + str(self.c) + ", bound = " + str(self.bound)


    f = smp.lambdify(problem.xvar, problem.fexpr)
    fslp = smp.lambdify(problem.xvar, problem.fexpr, slp)
    P = []
    ival = interval.Interval(problem.range)
    s1 = fslp(slp.Slope(ival, ival[0]))
    s2 = fslp(slp.Slope(ival, ival[1]))
    P.append(Sub(s1, s2, ival))
    fr = solinfo.value
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
            # print("at ", sub.c, " ns = ", ns)
            if ns.value < fr:
                fr = ns.value
                xr = sub.c
            P.append(Sub(sub.s1, ns, x1))
            P.append(Sub(ns, sub.s2, x2))
    solinfo.value = fr
    solinfo.x = xr
    return steps


def check_slope(problem, c, ival):
    fslp = smp.lambdify(problem.xvar, problem.fexpr, slp)
    ns = fslp(slp.Slope(ival, c))
    print("slope = ", ns)


#=============
MAX_STEPS = 10000
x = smp.symbols('x')
# fexpr = smp.sin(x) + smp.sin(10/3 * x)
# fexpr = smp.sin(2 * x)
fexpr = smp.cos(10*x) * (smp.log(x + 1.25) - 0.84 * x)**2

# problem = Problem("problem1", [2.7, 7.5], x, fexpr)
problem = Problem("problem2", [0.75, 1.75], x, fexpr)

# check_slope(problem, 5.013243513478913, interval.Interval([4.891846041674883, 5.013243513478914]))
# exit(0)

solinfo = SolutionInfo(10000000, 0)
steps = simple_bnb(problem, 1e-3, solinfo, MAX_STEPS)
print("For a problem ", problem, ", found solution ", solinfo, " in ", steps, " steps.")

solinfo = SolutionInfo(10000000, 0)
steps = pijavBnB(problem, 1e-3, solinfo, MAX_STEPS)
print("For a problem ", problem, ", found solution ", solinfo, " in ", steps, " steps.")