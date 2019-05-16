from cqc.pythonLib import CQCConnection
from Bob_ROT import Bob_ROT


def Bob_OT(c, l, n=20):
    """
    Return Alice's input list corresponding to choice bit c, obtained from 1-2 OT.

    Input arguments:
    c -- integer 0 or 1, Bob's choice bit
    l -- integer, length of output lists (<= n)
    n -- integer, length of n for ROT (default 20)

    Output:
    m_c -- list of l bits corresponding to list m_i that Alice inputs for i = c
    """
    s_c = Bob_ROT(c,l,n)

    with CQCConnection("Bob") as Bob:
        data0 = Bob.recvClassical()
        xor_0 = list(data0)
        data1 = Bob.recvClassical()
        xor_1 = list(data1)

    if c == 0:
        xor_c = xor_0 # Can neglect the other
    else:
        xor_c = xor_1

    m_c = []
    for i in range(l):
        m_c.append((s_c[i]+xor_c[i]) %2)

    return m_c
