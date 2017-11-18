#!/usr/bin/env python3

import unittest
import numpy as np
import random

from hammingclasses import HammingEncoder
from hammingclasses import HammingChecker


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
        self.r = 3
        self.k = 2 ** self.r - self.r - 1
        self.encoder = HammingEncoder(self.r)
        self.checker = HammingChecker(self.r)

    def test_no_corruption(self):
        for i in range(2, 7):
            self.r = i
            self.k = 2 ** self.r - self.r - 1
            self.encoder = HammingEncoder(self.r)
            self.checker = HammingChecker(self.r)

            word = ''.join([random.choice(('0', '1')) for _ in range(self.k)])
            coded = self.encoder.encode(word)
            self.assertEqual(self.checker.check(coded), -1)


    def test_corrupt_one_bit(self):

        word = ''.join([random.choice(('0', '1')) for _ in range(self.k)])
        coded = self.encoder.encode(word)

        



    # @repeat(10)
    # def test_no_corruption_random(self):
    #     word = rand_array(self.size)
    #     coded = self.encoder.encode(word)
    #     self.assertEqual(self.checker.check(coded), -1)


if __name__ == '__main__':
    unittest.main()