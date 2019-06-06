from time import sleep
from numpy import matrix, random
from cqc.pythonLib import CQCConnection, qubit

def Alice_ROT(l, n=100, waiting_time=2):
    """
    Perform 1-2 ROT for Alice and return two random lists of length l.

    Input arguments:
    l            -- integer, length of output lists (must be smaller than n)
    n            -- integer, length of initial x_A and y_A (default 100)
    waiting_time -- integer, number of seconds that Alice and Bob wait after
                    step 2 during the protocol (default 2)

    Output:
    s_0          -- list of l bits
    s_1          -- list of l bits
    """
    # Error handling.
    if l > n:
        raise Exception("Input argument l cannot be greater than n.")

    # (Step 1)
    # Alice randomly picks x_A and y_A in {0,1}^n.
    x_A = [random.randint(2) for i in range(n)]
    y_A = [random.randint(2) for i in range(n)]

    with CQCConnection("Alice") as Alice:
        # Alice sends n qubits (BB84 states) to Bob.
        for i in range(n):
            q = qubit(Alice)
            if x_A[i] == 1:
                q.X()
            if y_A[i] == 1:
                q.H()
            Alice.sendQubit(q, "Bob")
        print("Alice has sent {} qubits to Bob.".format(n))

        # Wait.
        print("Both parties wait {} seconds.".format(waiting_time))
        sleep(waiting_time)

        #(Step 3)
        # Alice sends y_A to Bob.
        Alice.sendClassical("Bob", y_A)
        print("Alice has sent y_A to Bob.")

        #(Step 4)
        # Alice receives I_0 and I_1 from Bob.
        data0 = Alice.recvClassical()
        I_0 = list(data0)
        data1 = Alice.recvClassical()
        I_1 = list(data1)

        # (Step 5)
        # Alice randomly picks two two-universal (lxn) hash functions
        # f_0, f_1 and sends them to Bob.
        f_0 = [[random.randint(2) for i in range(n)] for j in range(l)]
        f_1 = [[random.randint(2) for i in range(n)] for j in range(l)]
        for i in range(l):
            Alice.sendClassical("Bob", f_0[i])
        print("Alice has sent f_0.")
        for i in range(l):
            Alice.sendClassical("Bob", f_1[i])
        print("Alice has sent f_1.")
        # Construct x_0 = x_A|I_0 and x_1 = x_A|I_1.
        x_0 = []
        for i in I_0:
            x_0.append(x_A[i])
        for i in range(len(x_A) - len(I_0)):
            x_0.append(0)
        x_1 = []
        for i in I_1:
            x_1.append(x_A[i])
        for i in range(len(x_A) - len(I_1)):
            x_1.append(0)
        # Translate x_0 and x_1 into a numpy nx1 matrix for computation.
        x_0 = matrix(x_0).transpose()
        x_1 = matrix(x_1).transpose()
        # Alice computes s_0 = f_0(x_0) and s_1 = f_1(x_1).
        s_0 = f_0*x_0 % 2
        s_0 = [s_0[i,0] for i in range(len(s_0))]
        s_1 = f_1*x_1 % 2
        s_1 = [s_1[i,0] for i in range(len(s_1))]

    print("Alice outputs s_0 and s_1.")
    return s_0, s_1
