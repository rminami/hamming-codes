#!/usr/bin/env python3

from hammingclasses import HammingEncoder
from hammingclasses import HammingChecker

from random import randint
import numpy as np


def rand_array(size):
    arr = np.empty(size, dtype=np.int)
    for i in range(size):
        arr[i] = randint(0, 1)
    return arr

def main():

    size = 4
    encoder = HammingEncoder(size)
    checker = HammingChecker(size)

    word = rand_array(size)
    coded = encoder.encode(word)

    checker.check_print(coded)      # No bits should be corrupted yet
    # TODO bit 6 is detected as corrupted when word = [1 0 1 1]

    print(str(word) + " has been encoded into: " + str(coded))

    for i in range(7):
        coded[i] = (coded[i] + 1) % 2   # Flip a bit
        print("Bit " + str(i) + " has been flipped: " + str(coded) + " -> corrects to: " + str(checker.correct(coded.copy())))
        coded[i] = (coded[i] + 1) % 2   # Flip it back

    # checker.check_print(coded)        # Checker should detect corrupted bit


# Main launcher
if __name__ == '__main__':
    main()
