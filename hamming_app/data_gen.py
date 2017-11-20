#!/usr/bin/env python3
import numpy as np

from hammingclasses import HammingEncoder, HammingChecker, \
    str_to_arr, arr_to_str, add_noise, random_word


def main():
    # tests will be conducted against 5 values of r, 10 values of p
    # total number of tests conducted will be no_of_tests * 50
    no_of_tests = 1000

    # header line
    print('r,p,success_rate')

    for r in range(2, 7):
        n = 2 ** r - 1
        encoder = HammingEncoder(r)
        checker = HammingChecker(r)

        p = 0.01
        while p <= 0.201:      

            no_of_successes = 0
            for _ in range(no_of_tests):
                word = random_word(n - r)
                codeword = encoder.encode(word)
                corrupted, bits_corrupted = add_noise(codeword, p)
                corrected = checker.correct(corrupted)
                if codeword == corrected:
                    no_of_successes += 1

            success_rate = '{0:.4f}'.format(no_of_successes / no_of_tests)

            print('%d,%s,%s' % (r, '{0:.2f}'.format(p), success_rate))

            p += 0.01


if __name__ == '__main__':
    main()
