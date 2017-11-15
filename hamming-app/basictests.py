import unittest
import numpy as np
from random import randint

from hammingclasses import HammingEncoder
from hammingclasses import HammingChecker
from main import rand_array


# ---- Repeat decorator --- #

# This decorator allows a single test to be run multiple times
# Useful for when a random input value is generated with each test

def repeat(times):
    def repeatHelper(f):
        def callHelper(*args):
            for i in range(0, times):
                f(*args)
        return callHelper
    return repeatHelper


# ---- Unit test class --- #


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.size = 4
        self.encoder = HammingEncoder(self.size)
        self.checker = HammingChecker(self.size)

    def test_no_corruption(self):
        word = np.array([1, 0, 0, 1])
        coded = self.encoder.encode(word)
        self.assertEqual(self.checker.check(coded), -1)


    def test_corrupt_one_bit(self):

        word = np.array([1, 0, 0, 1])
        coded = self.encoder.encode(word)

        corrupted = coded.copy()
        corrupted[4] = (corrupted[4] + 1) % 2

        self.assertTrue(np.array_equal(self.checker.correct(corrupted), coded))



    # @repeat(10)
    # def test_no_corruption_random(self):
    #     word = rand_array(self.size)
    #     coded = self.encoder.encode(word)
    #     self.assertEqual(self.checker.check(coded), -1)


if __name__ == '__main__':
    unittest.main()