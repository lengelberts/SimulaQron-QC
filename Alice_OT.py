from cqc.pythonLib import CQCConnection
from Alice_ROT import Alice_ROT


#Now works for n = 20
def Alice_OT(m0,m1):
    """
    Perform 1-2 OT for Alice's part, without revealing the other input list.

    Input argument:
    m0 -- list of length n consisting of 0s and 1s
    m1 -- list of length n consisting of 0s and 1s

    There is no output.
    """
    s0,s1 = Alice_ROT()

    n = len(s0)
    xor_0 = []
    xor_1 = []
    for i in range(n):
        xor_0.append((m0[i]+s0[i]) %2)
        xor_1.append((m1[i]+s1[i]) %2)

    with CQCConnection("Alice") as Alice:
        Alice.sendClassical("Bob",xor_0)
        Alice.sendClassical("Bob",xor_1)
    print("Bob has received xor_0 and xor_1.")
