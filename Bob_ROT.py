from numpy import matrix, random
from cqc.pythonLib import CQCConnection

def Bob_ROT(c, l, n=100):
    """
    Perform 1-2 ROT for Bob and return list s_c of length l without revealing c.

    Input arguments:
    c            -- integer 0 or 1, Bob's choice bit c
    l            -- integer, length of output list (must be smaller than n)
    n            -- integer, length of initial y_B (default 100)

    Output:
    s_c          -- list of l bits corresponding to list s_c returned by Alice
    """
    # Error handling.
    if c != 0 and c != 1:
        raise Exception("Input argument c must be either 0 or 1.")
    if l > n:
        raise Exception("Input argument l cannot be greater than n.")

    # (Step 2)
    # Bob randomly picks y_B in {0,1}^n.
    y_B = [random.randint(2) for i in range(n)]

    with CQCConnection("Bob") as Bob:
        # Bob measures the ith received qubit in basis y_B[i]
        # and obtains outcome x_B, a list of length n.
        x_B = []
        for i in range(n):
            q = Bob.recvQubit()
            if y_B[i] == 1:
                q.H()
            m = q.measure()
            x_B.append(m)

        # Wait.

        # (Step 3)
        # Bob receives y_A from Alice.
        basisinfo = Bob.recvClassical()
        y_A = list(basisinfo)

        # (Step 4)
        # Bob forms the sets I_c and I_cbar.
        I_c = []
        I_cbar = []
        for i in range(n):
            if y_A[i] == y_B[i]:
                I_c.append(i)
            else:
                I_cbar.append(i)
        # Bob sends I_0 and I_1 to Alice.
        if c == 0:
            I_0 = I_c
            I_1 = I_cbar
        else:
            I_0 = I_cbar
            I_1 = I_c
        Bob.sendClassical("Alice", I_0)
        print("Bob has sent I_0.")
        Bob.sendClassical("Alice", I_1)
        print("Bob has sent I_1.")

        # (Step 5)
        # Bob receives f_0 and f_1 from Alice.
        # Here, f_i is a list of l lists of size n.
        f_0 = []
        for i in range(l):
            data0 = Bob.recvClassical()
            f_0.append(list(data0))
        f_1 = []
        for i in range(l):
            data1 = Bob.recvClassical()
            f_1.append(list(data1))

        # (Step 6)
        # Construct x_c = x_B|I_c.
        x_c = []
        for i in I_c:
            x_c.append(x_B[i])
        for i in range(len(x_B) - len(I_c)):
            x_c.append(0)
        # Translate x_c into a numpy nx1 matrix for computation.
        x_c = matrix(x_c).transpose()
        # Bob computes s_c = f_c(x_c).
        if c == 0:
            f_c = f_0
        else:
            f_c = f_1
        s_c = f_c*x_c % 2
        s_c = [s_c[i,0] for i in range(len(s_c))]

    print("Bob outputs s_c.")
    return s_c
