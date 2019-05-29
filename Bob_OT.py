from cqc.pythonLib import CQCConnection
from Bob_ROT import Bob_ROT

def Bob_OT(c, l, n=100):
    """
    Perform 1-2 OT for Bob and return Alice's input list m_c without revealing c.

    Input arguments:
    c            -- integer 0 or 1, Bob's choice bit c
    l            -- integer, length of output lists (must be smaller than n)
    n            -- integer, length of n for ROT (default 100)

    Output:
    m_c          -- list of l bits corresponding to Alice's input list m_c
    """
    # Error handling.
    if c != 0 and c != 1:
        raise Exception("Input argument c must be either 0 or 1.")
    if l > n:
        raise Exception("Input argument l cannot be greater than n.")

    # (Step 1)
    # Bob runs 1-2 ROT.
    s_c = Bob_ROT(c, l, n)

    # (Step 3)
    # Bob receives (m0 XOR s0) and (m1 XOR s1) from Alice.
    with CQCConnection("Bob") as Bob:
        data0 = Bob.recvClassical()
        xor_0 = list(data0)
        data1 = Bob.recvClassical()
        xor_1 = list(data1)

    # Bob computes m_c.
    if c == 0:
        xor_c = xor_0
    else:
        xor_c = xor_1
    m_c = []
    for i in range(l):
        m_c.append((s_c[i] + xor_c[i]) %2)

    print("Bob outputs m_c.")
    return m_c
