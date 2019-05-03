import unittest
import interval

class TestSum(unittest.TestCase):
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


