import numpy as np

size = 4

def str_to_arr(s):
    arr = np.empty(len(s), dtype=np.int)
    for i in range(len(s)):
        if s[i] == '0' or s[i] == '1':
            arr[i] = int(s[i])
        else:
            raise ValueError('Please enter a binary number.')
    return arr


def arr_to_str(arr):
    s = ""
    for el in arr:
        # This function does not validate
        s += str(el)
    return s

def corrupt(arr, error_rate):
    # implement later
    return arr

