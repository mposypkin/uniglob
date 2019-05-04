import unittest
import math
import interval


class TestInterval(unittest.TestCase):
    def testNeg(self):
        x = interval.Interval([-1, 2])
        y = -x
        self.assertEqual(y.x, [-2, 1])

    def testAdd(self):
        x = interval.Interval([-1, 2])
        y = interval.Interval([1, 2])
        z = x + y
        self.assertEqual(z.x, [0, 4])

    def testSub(self):
        x = interval.Interval([-1, 2])
        y = interval.Interval([1, 2])
        z = y - x
        self.assertEqual(z.x, [-1, 3])

    def testMul(self):
        x = interval.Interval([-1, 2])
        y = interval.Interval([1, 2])
        z = x * y
        self.assertEqual(z.x, [-2, 4])
        u = interval.Interval([-2, -1])
        v = interval.Interval([-3, -2])
        z = u * v
        self.assertEqual(z.x, [2, 6])

    def testPow(self):
        x = interval.Interval([-1, 2])
        z = x ** 3
        self.assertEqual(z.x, [-1,8])
        z = x ** 4
        self.assertEqual(z.x, [0,16])

    def testSin(self):
        x = interval.Interval([-math.pi/6, 2])
        z = interval.sin(x)
        for i in range(len(z.x)):
            self.assertAlmostEqual(z.x[i], [-0.5,1][i])

    def testCos(self):
        x = interval.Interval([-1, 2 * math.pi/3])
        z = interval.cos(x)
        for i in range(len(z.x)):
            self.assertAlmostEqual(z.x[i], [-0.5,1][i])







