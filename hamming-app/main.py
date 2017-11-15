#!/usr/bin/env python3

from hammingclasses import HammingEncoder
from hammingclasses import HammingChecker

from random import randint
import numpy as np



def main():

    r = 3
    encoder = HammingEncoder(r)
    checker = HammingChecker(r)

    word = '1010'
    coded = encoder.encode(word)

    checker.check_print(coded)      # No bits should be corrupted yet
    # TODO bit 6 is detected as corrupted when word = [1 0 1 1]

    print(str(word) + " has been encoded into: " + str(coded))

    for i in range(7):
        coded = flip_bit(coded, i) 
        print("Bit " + str(i) + " has been flipped: " + coded + " -> corrects to: " + arr_to_str(checker.correct(coded)))
        coded = flip_bit(coded, i)

    # checker.check_print(coded)        # Checker should detect corrupted bit

def flip_bit(str, i):
    arr = str_to_arr(str)
    arr[i] = (arr[i] + 1) % 2
    return arr_to_str(arr)

# Converts strings to arrays and back

def str_to_arr(s):
    '''Converts a string of 0s and 1s to a numpy array'''
    arr = np.empty(len(s), dtype=np.int)
    for i in range(len(s)):
        if s[i] == '0' or s[i] == '1':
            arr[i] = int(s[i])
        else:
            raise ValueError('Please enter a binary number.')
    return arr


def arr_to_str(arr):
    '''Converts a numpy array to a string. Does not validate input value.'''
    s = ""
    for el in arr:
        s += str(el)
    return s

# Main launcher
if __name__ == '__main__':
    main()
