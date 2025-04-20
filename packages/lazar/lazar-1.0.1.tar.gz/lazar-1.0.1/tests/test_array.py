import unittest
from lazar.core.array import LazarArray

class TestLazarArray(unittest.TestCase):
    def setUp(self):
        self.arr1 = LazarArray([1, 2, 3])
        self.arr2 = LazarArray([4, 5, 6])
    
    def test_addition(self):
        result = self.arr1 + self.arr2
        self.assertEqual(list(result), [5, 7, 9])
    
    def test_dot_product(self):
        result = self.arr1.dot(self.arr2)
        self.assertEqual(result, 32)
    
    def test_reshape(self):
        arr = LazarArray([1, 2, 3, 4])
        reshaped = arr.reshape((2, 2))
        self.assertEqual(reshaped.shape, (2, 2))
    
    def test_indexing(self):
        self.assertEqual(self.arr1[1], 2)
        self.assertEqual(list(self.arr1[1:3]), [2, 3])

if __name__ == '__main__':
    unittest.main()
