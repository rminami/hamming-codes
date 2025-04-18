#!/usr/bin/env python3

import unittest
import random

from .hammingclasses import HammingEncoder, HammingChecker, \
    str_to_arr, arr_to_str, random_word


# ---- Unit test class --- #

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        """Sets up Hamming encoders and checkers for parameters 2 to 6"""

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

        # for r = 6
        self.encoder6 = HammingEncoder(6)
        self.checker6 = HammingChecker(6)


    # ---- Verifies that tests correctly identify uncorrupted codewords ---- #

    def test_no_corruption_2(self):
        # r = 2, n = 1
        word = random_word(1)
        codeword = self.encoder2.encode(word)
        self.assertEqual(codeword, self.checker2.correct(codeword))


    def test_no_corruption_3(self):
        # r = 3, n = 4
        word = random_word(4)
        codeword = self.encoder3.encode(word)
        self.assertEqual(codeword, self.checker3.correct(codeword))


    def test_no_corruption_4(self):
        # r = 4, n = 11
        word = random_word(11)
        codeword = self.encoder4.encode(word)
        self.assertEqual(codeword, self.checker4.correct(codeword))


    def test_no_corruption_5(self):
        # r = 5, n = 26
        word = random_word(26)
        codeword = self.encoder5.encode(word)
        self.assertEqual(codeword, self.checker5.correct(codeword))


    def test_no_corruption_6(self):
        # r = 6, n = 57
        word = random_word(57)
        codeword = self.encoder6.encode(word)
        self.assertEqual(codeword, self.checker6.correct(codeword))


    # ---- Verifies that one corrupted bit can be successfully corrected ---- #

    def test_corrupt_one_bit_2(self):
        # r = 2, n = 1
        word = random_word(1)
        codeword = self.encoder2.encode(word)
        corrupted = corrupt_one_bit(codeword)
        self.assertEqual(codeword, self.checker2.correct(corrupted))


    def test_corrupt_one_bit_3(self):
        # r = 3, n = 4
        word = random_word(4)
        codeword = self.encoder3.encode(word)
        corrupted = corrupt_one_bit(codeword)
        self.assertEqual(codeword, self.checker3.correct(corrupted))


    def test_corrupt_one_bit_4(self):
        # r = 4, n = 11
        word = random_word(11)
        codeword = self.encoder4.encode(word)
        corrupted = corrupt_one_bit(codeword)
        self.assertEqual(codeword, self.checker4.correct(corrupted))


    def test_corrupt_one_bit_5(self):
        # r = 5, n = 26
        word = random_word(26)
        codeword = self.encoder5.encode(word)
        corrupted = corrupt_one_bit(codeword)
        self.assertEqual(codeword, self.checker5.correct(corrupted))


    def test_corrupt_one_bit_6(self):
        # r = 6, n = 57
        word = random_word(57)
        codeword = self.encoder6.encode(word)
        corrupted = corrupt_one_bit(codeword)
        self.assertEqual(codeword, self.checker6.correct(corrupted))


    # ---- Verifies that correction fails when two bits are corrupted ---- #

    def test_corrupt_two_bits_2(self):
        # r = 2, n = 1
        word = random_word(1)
        codeword = self.encoder2.encode(word)
        corrupted = corrupt_two_bits(codeword)
        self.assertNotEqual(codeword, self.checker2.correct(corrupted))


    def test_corrupt_two_bits_3(self):
        # r = 3, n = 4
        word = random_word(4)
        codeword = self.encoder3.encode(word)
        corrupted = corrupt_two_bits(codeword)
        self.assertNotEqual(codeword, self.checker3.correct(corrupted))


    def test_corrupt_two_bits_4(self):
        # r = 4, n = 11
        word = random_word(11)
        codeword = self.encoder4.encode(word)
        corrupted = corrupt_two_bits(codeword)
        self.assertNotEqual(codeword, self.checker4.correct(corrupted))


    def test_corrupt_two_bits_5(self):
        # r = 5, n = 26
        word = random_word(26)
        codeword = self.encoder5.encode(word)
        corrupted = corrupt_two_bits(codeword)
        self.assertNotEqual(codeword, self.checker5.correct(corrupted))


    def test_corrupt_two_bits_6(self):
        # r = 6, n = 57
        word = random_word(57)
        codeword = self.encoder6.encode(word)
        corrupted = corrupt_two_bits(codeword)
        self.assertNotEqual(codeword, self.checker6.correct(corrupted))


# ---- Helper function for unit tests ---- #

def random_word(len):
    """Returns random binary word at the given length"""
    return ''.join([random.choice(('0', '1')) for _ in range(len)])


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