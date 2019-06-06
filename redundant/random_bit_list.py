#This file contains function random_bit_list(n)

from random import randint

def random_bit_list(n):
    """
    Return a random list of length n consisting of 0s and/or 1s.

    Argument:
    n -- length of the list
    """
    list = []
    for i in range(n):
        list.append(randint(0,1))

    return list
