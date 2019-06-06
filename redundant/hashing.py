from numpy import matrix


def extended_sublist(x,I):
    """
    Return the elements of x whose index is in I and pad with 0s to obtain same length as x.

    Input argument:
    x -- list of integers 0s and 1s (length n)
    I -- list of non-decreasing integers i, where 0 <= i < n
    Output:
    list of length n
    """
    n = len(x)
    list = []
    for i in I:
        list.append(x[i])
    for i in range(len(x)-len(I)):
        list.append(0)
    return list


def compute_output_list(f,x):
    """
    Return result of matrix multiplication f*(x^T) as a list.

    Input arguments:
    f -- (Python) matrix of size nxn of integers 0s and 1s
    x -- (Python) list of length n of integers 0s and 1s
    Output:
    list of length n of integers 0s and 1s
    """
    list = []
    x_transpose = matrix(x).transpose() # Used numpy
    list = f*x_transpose % 2            # Used numpy
    list = [list[i,0] for i in range(len(list))]
    return list
