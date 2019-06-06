from cqc.pythonLib import CQCConnection
from Alice_ROT import Alice_ROT

def Alice_OT(m0, m1, l, n=100, waiting_time=2):
    """
    Perform 1-2 OT for Alice, without revealing Alice's other input list to Bob.

    Input arguments:
    m0           -- list of length l consisting of 0s and 1s
    m1           -- list of length l consisting of 0s and 1s
    l            -- integer, length of input lists (must be smaller than n)
    n            -- integer, length of n for ROT (default 100)
    waiting_time -- integer, number of seconds that Alice and Bob wait after
                    step 2 during the protocol for 1-2 ROT (default 2)

    There is no output.
    """
    # Error handling.
    if l > n:
        raise Exception("Input argument l cannot be greater than n.")

    # (Step 1)
    # Alice runs 1-2 ROT.
    s0,s1 = Alice_ROT(l, n, waiting_time)

    # (Step 2)
    # Alice sends (m0 XOR s0) and (m1 XOR s1) to Bob.
    xor_0 = []
    xor_1 = []
    for i in range(l):
        xor_0.append((m0[i] + s0[i]) %2)
        xor_1.append((m1[i] + s1[i]) %2)
    with CQCConnection("Alice") as Alice:
        Alice.sendClassical("Bob", xor_0)
        Alice.sendClassical("Bob", xor_1)

    print("Alice is finished.")
