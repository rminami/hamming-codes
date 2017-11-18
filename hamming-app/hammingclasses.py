#!/usr/bin/env python3

import numpy as np
from random import random

# ---- Hamming code classes --- #

# This code assumes that words and codewords are encoded as row vectors.
# Thus, word w is encoded into codeword c with w.G and c is decoded with c.H.

# ---- Hamming encoder class --- #

class HammingEncoder(object):
    """Takes a source message and adds Hamming parity-check bits"""

    def init_genmatrix(self):
        """Creates the generator matrix for the Hamming code, given its size"""
        parmatrix = init_paritymatrix(self.k)
        genmatrix = np.identity(self.k, dtype=np.int)

        # Parity bits are set as bits 1, 2, 4, 8, ... (= index 0, 1, 3, 7, ...)
        for i in range(len(parmatrix)):
            genmatrix = insert_col(genmatrix, parmatrix[:, i:i+1], 2**i-1)
        return genmatrix


    def __init__(self, r):
        """Constructs a Hamming encoder"""
        self.n = 2 ** r - 1
        self.k = self.n - r
        self.genmatrix = self.init_genmatrix()


    def encode(self, word):
        """Constructs a codeword with parity bits given a word of an appropriate length.
           Assumes that the input is a string of 0s and 1s"""
        if len(word) != self.k:
            raise ValueError("Word must be of length " + str(self.k))

        return arr_to_str(np.dot(str_to_arr(word), self.genmatrix) % 2)


# ---- Hamming encoder class --- #

class HammingChecker(object):
    """Reads a codeword and checks if the word bits and the parity bits match up"""

    def init_checkmatrix(self):
        """Creates the parity-check matrix for the Hamming code, given its size"""
        parmatrix = init_paritymatrix(self.k)
        checkmatrix = np.identity(self.k-1, dtype=np.int)

        # Parity bits are set as bits 1, 2, 4, 8, ... (= index 0, 1, 3, 7, ...)
        for i in range(len(parmatrix)):
            checkmatrix = insert_row(checkmatrix, parmatrix[i:i+1], 2**i-1)
        return checkmatrix


    def __init__(self, r):
        """Constructs a Hamming parity-checker"""
        self.n = 2 ** r - 1
        self.k = self.n - r
        self.checkmatrix = self.init_checkmatrix()


    def get_matching_row(self, row):
        """Searches for a row in the parity-check matrix and returns its index.
           Returns -1 if not found."""
        try:
            return np.where(np.all(self.checkmatrix == row, axis=1))[0][0]
        except IndexError:
            return -1


    def check(self, codeword):
        """Checks if a codeword's word bits and parity bits match up"""
        if len(codeword) != len(self.checkmatrix):
            raise ValueError("Codeword is the wrong length.")

        return self.get_matching_row(np.dot(str_to_arr(codeword), self.checkmatrix) % 2)


    def check_print(self, codeword):
        """Prints the relevant message for the parity-check result."""
        try:
            res = self.check(codeword)
            if res != -1:
                print("Bit %d has been corrupted." % res)
            else:
                print("No bits have been corrupted.")
        except ValueError as err:
            print(err)


    def correct(self, codeword):
        """Tries to correct the corrupted bit"""
        try:
            res = self.check(codeword)
            if res != -1:
                cw_arr = str_to_arr(codeword)
                cw_arr[res] = (cw_arr[res] + 1) % 2
                return arr_to_str(cw_arr)
            else:
                return codeword
                
        except ValueError as err:
            print(err)


# ---- Matrix utilities --- #

# Various matrix operations that are needed for the Hamming encoder and checker.


def init_paritymatrix(size):
    """Generates the parity-check portion of both the generator and parity-check matrices."""
    return ((np.fliplr(np.identity(size, dtype=np.int)) + 1) % 2)[:, 1:]


def insert_col(mat, col, index):
    """Inserts a column into a matrix at the given index."""
    return np.hstack((mat[:, :index], col, mat[:, index:]))


def insert_row(mat, row, index):
    """Inserts a row into a matrix at the given index."""
    return np.vstack((mat[:index, ], row, mat[index:, ]))


# ---- Conversion utilities --- #

# Converts strings to arrays and back

def str_to_arr(s):
    """Converts a string of 0s and 1s to a numpy array"""
    arr = np.empty(len(s), dtype=np.int)
    for i in range(len(s)):
        if s[i] == '0' or s[i] == '1':
            arr[i] = int(s[i])
        else:
            raise ValueError('Please enter a binary number.')
    return arr


def arr_to_str(arr):
    """Converts a numpy array to a string. Does not validate input value."""
    s = ""
    for el in arr:
        s += str(el)
    return s


# ---- Helper functions --- #

# Adds noise to transmissions

def add_noise(s, p):
    arr = str_to_arr(s)
    count = 0
    for i in range(len(arr)):
        r = random()
        if (r < p):
            arr[i] = (arr[i] + 1) % 2
            count += 1
    return arr_to_str(arr), count
