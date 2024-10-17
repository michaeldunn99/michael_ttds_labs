import unittest
import numpy as np
from proximity import proximity

class TestProximity(unittest.TestCase):

    def test_proximity_basic(self):
        list_0 = [1, 3, 5]
        list_1 = [2, 4, 6]
        min_proximity, positions = proximity(list_0, list_1)
        self.assertEqual(min_proximity, 1)
        self.assertIn(positions, [(1, 2), (3, 4), (5, 6)])

    def test_proximity_with_large_numbers(self):
        list_0 = [1000, 2000, 3000]
        list_1 = [1500, 2500, 3500]
        min_proximity, positions = proximity(list_0, list_1)
        self.assertEqual(min_proximity, 500)
        self.assertIn(positions, [(1000, 1500), (2000, 1500), (3000, 3500)])

    def test_proximity_with_mixed_signs(self):
        list_0 = [1, 3, 5]
        list_1 = [2, 4, 6]
        min_proximity, positions = proximity(list_0, list_1)
        self.assertEqual(min_proximity, 1)
        self.assertIn(positions, [(1, 2), (3, 4), (5, 6)])

    def test_proximity_with_single_element_lists(self):
        list_0 = [1]
        list_1 = [2]
        min_proximity, positions = proximity(list_0, list_1)
        self.assertEqual(min_proximity, 1)
        self.assertIn(positions, [(1, 2)])

if __name__ == '__main__':
    unittest.main()
