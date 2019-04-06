from cqc.pythonLib import CQCConnection
from Bob_ROT import Bob_ROT


#Now works for n = 20
def Bob_OT(c):
    """
    Return Alice's input list corresponding to choice bit c, obtained from 1-2 OT.

    Input argument:
    c -- integer 0 or 1, Bob's choice bit
    Output:
    list of length n
    """
    s_c = Bob_ROT(c)

    with CQCConnection("Bob") as Bob:
        data0 = Bob.recvClassical()
        xor_0 = list(data0)
        data1 = Bob.recvClassical()
        xor_1 = list(data1)

    if c == 0:
        xor_c = xor_0 # Can neglect the other
    else:
        xor_c = xor_1

    n = len(s_c)
    m_c = []
    for i in range(n):
        m_c.append((s_c[i]+xor_c[i]) %2)

    return m_c
