#!/usr/bin/env python3

import unittest

from hammingclasses import HammingEncoder, HammingChecker, random_word
from basictests import corrupt_one_bit, corrupt_two_bits


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

        # set to print string of any length
        self.maxDiff = None


    # ---- Verifies that tests correctly identify uncorrupted codewords ---- #

    def test_no_corruption_7(self):
        # r = 7, n = 120
        word = random_word(120)
        codeword = self.encoder7.encode(word)
        self.assertEqual(codeword, self.checker7.correct(codeword))


    def test_no_corruption_8(self):
        # r = 8, n = 247
        word = random_word(247)
        codeword = self.encoder8.encode(word)
        self.assertEqual(codeword, self.checker8.correct(codeword))


    # ---- Verifies that one corrupted bit can be successfully corrected ---- #

    def test_corrupt_one_bit_7(self):
        # r = 7, n = 120
        word = random_word(120)
        codeword = self.encoder7.encode(word)
        corrupted = corrupt_one_bit(codeword)
        self.assertEqual(codeword, self.checker7.correct(corrupted))


    def test_corrupt_one_bit_8(self):
        # r = 8, n = 247
        word = random_word(247)
        codeword = self.encoder8.encode(word)
        corrupted = corrupt_one_bit(codeword)
        self.assertEqual(codeword, self.checker8.correct(corrupted))


    # ---- Verifies that correction fails when two bits are corrupted ---- #

    def test_corrupt_two_bits_7(self):
        # r = 7, n = 120
        word = random_word(120)
        codeword = self.encoder7.encode(word)
        corrupted = corrupt_two_bits(codeword)
        self.assertNotEqual(codeword, self.checker7.correct(corrupted))


    def test_corrupt_two_bits_8(self):
        # r = 8, n = 247
        word = random_word(247)
        codeword = self.encoder8.encode(word)
        corrupted = corrupt_two_bits(codeword)
        self.assertNotEqual(codeword, self.checker8.correct(corrupted))


if __name__ == '__main__':
    unittest.main()