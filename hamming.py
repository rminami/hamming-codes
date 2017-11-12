#!/usr/bin/env python3

import numpy as np


# ---- Hamming code classes --- #

# This code assumes that words and codewords are encoded as row vectors.
# Thus, word w is encoded into codeword c with w.G and c is decoded with c.H.


# Takes a source message and adds Hamming parity-check bits
class HammingEncoder(object):

    # Creates the generator matrix for the Hamming code, given its size
    def init_genmatrix(self, size):
        parmatrix = init_paritymatrix(size)
        genmatrix = np.identity(size, dtype=np.int)

        # Parity bits are set as bits 1, 2, 4, 8, ... (= index 0, 1, 3, 7, ...)
        for i in range(len(parmatrix)):
            genmatrix = insert_col(genmatrix, parmatrix[:, i:i+1], 2**i-1)
        return genmatrix


    # Constructs a Hamming encoder
    def __init__(self, size):
        self.size = size
        self.genmatrix = self.init_genmatrix(size)


    # Constructs a codeword with parity bits given a word of an appropriate length
    def encode(self, word_arr):
        if len(word_arr) != self.size:
            raise ValueError("Word must be of length " + str(self.size))
        return np.dot(word_arr, self.genmatrix) % 2



# Reads a codeword and checks if the word bits and the parity bits match up
class HammingChecker(object):

    # Creates the parity-check matrix for the Hamming code, given its size
    def init_checkmatrix(self, size):
        parmatrix = init_paritymatrix(size)
        checkmatrix = np.identity(size-1, dtype=np.int)

        # Parity bits are set as bits 1, 2, 4, 8, ... (= index 0, 1, 3, 7, ...)
        for i in range(len(parmatrix)):
            checkmatrix = insert_row(checkmatrix, parmatrix[i:i+1], 2**i-1)
        return checkmatrix


    # Constructs a Hamming parity-checker
    def __init__(self, size):
        self.size = size
        self.checkmatrix = self.init_checkmatrix(size)


    # Searches for a row in the parity-check matrix and returns its index.
    # Returns -1 if not found.
    def get_matching_row(self, row):
        try:
            return np.where(np.all(self.checkmatrix == row, axis=1))[0][0]
        except IndexError:
            return -1

    # Checks if a codeword's word bits and parity bits match up
    def check(self, codeword_arr):
        if len(codeword_arr) != len(self.checkmatrix):
            raise ValueError("Codeword is the wrong length.")

        return self.get_matching_row(np.dot(codeword_arr, self.checkmatrix) % 2)

    # Prints the relevant message for the parity-check result.
    def check_print(self, codeword_arr):
        try:
            res = self.check(codeword_arr)
            if res != -1:
                print("Bit %d has been corrupted." % res)
            else:
                print("No bits have been corrupted.")
        except ValueError as err:
            print(err)

    # Tries to correct the corrupted bit
    def correct(self, codeword_arr):
        try:
            res = self.check(codeword_arr)
            if res != -1:
                codeword_arr[res] = (codeword_arr[res] + 1) % 2
            return codeword_arr
                
        except ValueError as err:
            print(err)



# ---- Matrix utilities --- #

# Various matrix operations that are needed for the Hamming encoder and checker.


# Generates the parity-check portion of both the generator and parity-check matrices.
def init_paritymatrix(size):
    return ((np.fliplr(np.identity(size, dtype=np.int)) + 1) % 2)[:, 1:]


# Inserts a column into a matrix at the given index.
def insert_col(mat, col, index):
    return np.hstack((mat[:, :index], col, mat[:, index:]))


# Inserts a row into a matrix at the given index.
def insert_row(mat, row, index):
    return np.vstack((mat[:index, ], row, mat[index:, ]))
