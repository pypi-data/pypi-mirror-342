import unittest
import math
from lazar.core.array import LazarArray
from lazar.core.math import exp, sin

class TestMathFunctions(unittest.TestCase):
    def setUp(self):
        self.arr = LazarArray([0, math.pi/2, math.pi])
    
    def test_exp(self):
        result = exp(self.arr)
        self.assertAlmostEqual(result[0], 1.0, places=4)
    
    def test_sin(self):
        result = sin(self.arr)
        self.assertAlmostEqual(result[1], 1.0, places=4)
        self.assertAlmostEqual(result[2], 0.0, places=4)

if __name__ == '__main__':
    unittest.main()
