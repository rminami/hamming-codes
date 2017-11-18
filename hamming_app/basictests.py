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
        """Sets up Hamming encoders and checkers for parameters 2 to 5"""

        # for r = 2
        self.encoder2 = HammingEncoder(2)
        self.checker2 = HammingChecker(2)

        # for r = 3
        self.encoder3 = HammingEncoder(3)
        self.checker3 = HammingChecker(3)

        # for r = 4
        self.encoder4 = HammingEncoder(4)
        self.checker4 = HammingChecker(4)

        # for r = 5
        self.encoder5 = HammingEncoder(5)
        self.checker5 = HammingChecker(5)


    # ---- Verifies that tests correctly identify uncorrupted codewords ---- #

    def test_no_corruption_2(self):
        # r = 2, n = 1
        word = ''.join([random.choice(('0', '1')) for _ in range(1)])
        codeword = self.encoder2.encode(word)
        self.assertEqual(codeword, self.checker2.correct(codeword))


    def test_no_corruption_3(self):
        # r = 3, n = 4
        word = ''.join([random.choice(('0', '1')) for _ in range(4)])
        codeword = self.encoder3.encode(word)
        self.assertEqual(codeword, self.checker3.correct(codeword))


    def test_no_corruption_4(self):
        # r = 4, n = 11
        word = ''.join([random.choice(('0', '1')) for _ in range(11)])
        codeword = self.encoder4.encode(word)
        self.assertEqual(codeword, self.checker4.correct(codeword))


    def test_no_corruption_5(self):
        # r = 5, n = 26
        word = ''.join([random.choice(('0', '1')) for _ in range(26)])
        codeword = self.encoder5.encode(word)
        self.assertEqual(codeword, self.checker5.correct(codeword))


    # ---- Verifies that one corrupted bit can be successfully corrected ---- #

    def test_corrupt_one_bit_2(self):
        # r = 2, n = 1
        word = ''.join([random.choice(('0', '1')) for _ in range(1)])
        codeword = self.encoder2.encode(word)
        corrupted = corrupt_one_bit(codeword)
        self.assertEqual(codeword, self.checker2.correct(corrupted))


    def test_corrupt_one_bit_3(self):
        # r = 3, n = 4
        word = ''.join([random.choice(('0', '1')) for _ in range(4)])
        codeword = self.encoder3.encode(word)
        corrupted = corrupt_one_bit(codeword)
        self.assertEqual(codeword, self.checker3.correct(corrupted))


    def test_corrupt_one_bit_4(self):
        # r = 4, n = 11
        word = ''.join([random.choice(('0', '1')) for _ in range(11)])
        codeword = self.encoder4.encode(word)
        corrupted = corrupt_one_bit(codeword)
        self.assertEqual(codeword, self.checker4.correct(corrupted))


    def test_corrupt_one_bit_5(self):
        # r = 5, n = 26
        word = ''.join([random.choice(('0', '1')) for _ in range(26)])
        codeword = self.encoder5.encode(word)
        corrupted = corrupt_one_bit(codeword)
        self.assertEqual(codeword, self.checker5.correct(corrupted))


    # ---- Verifies that correction fails when two bits are corrupted ---- #

    def test_corrupt_two_bits_2(self):
        # r = 2, n = 1
        word = ''.join([random.choice(('0', '1')) for _ in range(1)])
        codeword = self.encoder2.encode(word)
        corrupted = corrupt_two_bits(codeword)
        self.assertNotEqual(codeword, self.checker2.correct(corrupted))


    def test_corrupt_two_bits_3(self):
        # r = 3, n = 4
        word = ''.join([random.choice(('0', '1')) for _ in range(4)])
        codeword = self.encoder3.encode(word)
        corrupted = corrupt_two_bits(codeword)
        self.assertNotEqual(codeword, self.checker3.correct(corrupted))


    def test_corrupt_two_bits_4(self):
        # r = 4, n = 11
        word = ''.join([random.choice(('0', '1')) for _ in range(11)])
        codeword = self.encoder4.encode(word)
        corrupted = corrupt_two_bits(codeword)
        self.assertNotEqual(codeword, self.checker4.correct(corrupted))


    def test_corrupt_two_bits_5(self):
        # r = 5, n = 26
        word = ''.join([random.choice(('0', '1')) for _ in range(26)])
        codeword = self.encoder5.encode(word)
        corrupted = corrupt_two_bits(codeword)
        self.assertNotEqual(codeword, self.checker5.correct(corrupted))


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