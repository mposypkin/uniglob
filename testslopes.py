import unittest
import math
from slopes import *

class TestSlopes(unittest.TestCase):
    def test1(self):
        def f(x):
            return (x + sin(x)) * exp(-(x**2))
        x = [0.75, 1.75]
        Expr.flagRecompRange = False
        ex1 = f(ident(x))
        self.assertAlmostEqual(ex1.S[0], -2.740, 3)
        self.assertAlmostEqual(ex1.S[1], 0.011, 3)

    def test2(self):
        def f(x):
            return x**6 - 15 * x**4 + 27 * x**2 + 250
        x = [0.75, 1.75]
        Expr.flagRecompRange = False
        ex1 = f(ident(x))
        self.assertAlmostEqual(ex1.S[0], -146.852, 3)
        self.assertAlmostEqual(ex1.S[1], 67.066, 3)


