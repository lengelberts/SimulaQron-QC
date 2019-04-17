from cqc.pythonLib import CQCConnection
from Alice_ROT import Alice_ROT


#Now works for n = 20, l <= 20
def Alice_OT(m0,m1,l,n):
    """
    Perform 1-2 OT for Alice's part, without revealing the other input list.

    Input arguments:
    m0 -- list of length l consisting of 0s and 1s
    m1 -- list of length l consisting of 0s and 1s
    l -- integer (<= 20), length of m0 and m1
    n -- integer (<= 20)

    There is no output.
    """
    s0,s1 = Alice_ROT(l,n)

    xor_0 = []
    xor_1 = []
    for i in range(l):
        xor_0.append((m0[i]+s0[i]) %2)
        xor_1.append((m1[i]+s1[i]) %2)

    with CQCConnection("Alice") as Alice:
        Alice.sendClassical("Bob",xor_0)
        Alice.sendClassical("Bob",xor_1)
    print("Bob has received xor_0 and xor_1.")
