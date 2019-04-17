from cqc.pythonLib import CQCConnection
from Bob_ROT import Bob_ROT


#Now works for n = 20, l <= 20
def Bob_OT(c,l,n):
    """
    Return Alice's input list corresponding to choice bit c, obtained from 1-2 OT.

    Input arguments:
    c -- integer 0 or 1, Bob's choice bit
    l -- integer (<= 20), length of output
    n -- integer (<= 20)

    Output:
    list of length l
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
