import unittest
from genetic_algorithm.utils import *


class TestUtils(unittest.TestCase):

    def test_create_path(self):
        names = ["{}".format(i) for i in range(10)]
        path = generate_path(names, 5)
        self.assertTrue(len(path) == 5)
        self.assertTrue(len(set(path)) == 5)
        self.assertTrue(set(path).issubset(set(names)))

