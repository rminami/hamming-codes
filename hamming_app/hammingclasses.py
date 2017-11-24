#!/usr/bin/env python3

import numpy as np
import re
import random

# ---- Hamming code classes --- #

# This code assumes that words and codewords are encoded as row vectors.
# Thus, word w is encoded into codeword c with w.G and c is decoded with c.H.

# ---- Hamming encoder class --- #

class HammingEncoder(object):
    """Takes a source message and adds Hamming parity-check bits"""

    def __init__(self, r):
        """Constructs a Hamming encoder"""
        self.r = r
        self.n = 2 ** self.r - 1
        self.genmatrix = self.__make_genmatrix()

        
    def __make_genmatrix(self):
        """Creates the generator matrix for the Hamming code"""
        genmatrix = np.zeros((self.n - self.r, self.n), dtype=np.uint) # k x n

        p_set = set([2 ** i - 1 for i in range(self.r)])
        d_set = set(range(self.n)) - p_set

        # fills in parity bit columns of the generator matrix
        for p_item in p_set:
            for d_index, d_item in enumerate(d_set):
                if (p_item + 1) & (d_item + 1) != 0:
                    genmatrix[d_index][p_item] = 1

        # fills in data bit columns of the generator matrix
        for d_index, d_item in enumerate(d_set):
            genmatrix[d_index][d_item] = 1

        return genmatrix


    def encode(self, word):
        """Constructs a codeword with parity bits given a word of an appropriate length.
           Assumes that the input is a string of 0s and 1s"""
        if len(word) != (self.n - self.r):
            raise ValueError("Wrong word length")

        return arr_to_str(np.dot(str_to_arr(word), self.genmatrix) % 2)


# ---- Hamming checker class --- #

class HammingChecker(object):
    """Reads a codeword and checks if the word bits and the parity bits match up"""

    def __init__(self, r):
        """Constructs a Hamming parity-checker"""
        self.r = r
        self.n = 2 ** self.r - 1
        self.checkmatrix = self.__make_checkmatrix()


    def __make_checkmatrix(self):
        """Creates the parity-check matrix for the Hamming code"""
        p_set = set([2 ** i - 1 for i in range(self.r)])
        d_set = set(range(self.n)) - p_set

        checkmatrix = np.zeros((self.n, self.r), dtype=np.uint) # n x r

        # filling in parity bit rows of the parity check matrix
        for d_item in d_set:
            for index in range(self.r):
                checkmatrix[d_item, index] = int(((d_item + 1) >> index) & 1)
     
        # filling in data bit rows of the parity check matrix
        for p_index, p_item in enumerate(p_set):
            checkmatrix[p_item][p_index] = 1  
        
        return checkmatrix


    def get_matching_row(self, row):
        """Searches for a row in the parity-check matrix and returns its index.
           Returns -1 if not found."""
        try:
            return np.where(np.all(self.checkmatrix == row, axis=1))[0][0]
        except IndexError:
            return -1


    def check(self, codeword):
        """Checks if a codeword's word bits and parity bits match up."""
        if len(codeword) != (self.n):
            raise ValueError("Codeword is the wrong length.")

        return self.get_matching_row(np.dot(str_to_arr(codeword), self.checkmatrix) % 2)


    def correct(self, codeword):
        """Tries to correct the corrupted bit."""
        if len(codeword) != (self.n):
            raise ValueError("Codeword is the wrong length.")

        cw_arr = str_to_arr(codeword)
        res = self.get_matching_row(np.dot(cw_arr, self.checkmatrix) % 2)

        # Everything seems to be working here -- problem with check matrix?
        
        # np.set_printoptions(threshold=np.nan)
        # print(self.checkmatrix)
        # print(np.dot(cw_arr, self.checkmatrix) % 2)
        
        if res != -1:
            cw_arr[res] = (cw_arr[res] + 1) % 2
            return arr_to_str(cw_arr)
        else:
            return codeword


# ---- Conversion utilities --- #

def str_to_arr(s):
    """Converts binary string to numpy array"""
    if not re.fullmatch(r'(0|1)*', s):
        raise ValueError('Input must be in binary.')
    return np.array([int(d) for d in s], dtype=np.uint)


def arr_to_str(arr):
    """Converts numpy array to string"""
    return re.sub(r'\[|\]|\s+', '', np.array_str(arr))


# ---- Helper functions --- #

def random_word(len):
    """Returns random binary word at the given length"""
    return ''.join([random.choice(('0', '1')) for _ in range(len)])


def add_noise(s, p):
    """Adds noise to transmissions"""
    arr = str_to_arr(s)
    count = 0
    for i in range(len(arr)):
        r = random.random()
        if (r < p):
            arr[i] = (arr[i] + 1) % 2
            count += 1
    return arr_to_str(arr), count

