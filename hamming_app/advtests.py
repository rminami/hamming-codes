#!/usr/bin/env python3

import unittest
import random

from hammingclasses import HammingEncoder
from hammingclasses import HammingChecker

from hammingclasses import str_to_arr
from hammingclasses import arr_to_str


# ---- Unit test class --- #

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        """Sets up Hamming encoders and checkers for parameters 7 and 8"""

        # for r = 7
        self.encoder7 = HammingEncoder(7)
        self.checker7 = HammingChecker(7)

        # for r = 8
        self.encoder8 = HammingEncoder(8)
        self.checker8 = HammingChecker(8)


    # ---- Verifies that tests correctly identify uncorrupted codewords ---- #

    def test_no_corruption_7(self):
        # r = 7, n = 120
        word = ''.join([random.choice(('0', '1')) for _ in range(120)])
        codeword = self.encoder7.encode(word)
        self.assertEqual(codeword, self.checker7.correct(codeword))


    def test_no_corruption_8(self):
        # r = 8, n = 247
        word = ''.join([random.choice(('0', '1')) for _ in range(247)])
        codeword = self.encoder8.encode(word)
        self.assertEqual(codeword, self.checker8.correct(codeword))


    # ---- Verifies that one corrupted bit can be successfully corrected ---- #



    # ---- Verifies that correction fails when two bits are corrupted ---- #




# ---- Helper function for unit tests ---- #

def corrupt_one_bit(codeword):
    """Flips a random bit in the codeword given"""
    cw_arr = str_to_arr(codeword)
    c_index = random.randint(0, len(codeword) - 1)
    cw_arr[c_index] = (cw_arr[c_index] + 1) % 2

    return arr_to_str(cw_arr)


def corrupt_two_bits(codeword):
    """Flips two random bits in the codeword given"""
    cw_arr = str_to_arr(codeword)

    # procedure ensures that the same bit is not flipped twice
    c_index1 = random.randint(0, len(codeword) - 1)
    c_index2 = (c_index1 + random.randint(1, len(codeword) - 1)) % len(codeword)

    cw_arr[c_index1] = (cw_arr[c_index1] + 1) % 2
    cw_arr[c_index2] = (cw_arr[c_index2] + 1) % 2

    return arr_to_str(cw_arr)


if __name__ == '__main__':
    unittest.main()