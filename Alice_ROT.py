from time import sleep
from numpy import matrix
from numpy.random import randint
from cqc.pythonLib import CQCConnection, qubit

def Alice_ROT(l, n=20, waiting_time=2):
    """
    Return two random strings of length l, obtained from 1-2 ROT.

    Input argument:
    l            -- integer, length of output lists (<= n)
    n            -- integer, length of x_A and y_A (default 20)
    waiting_time -- integer, amount of seconds that Alice and Bob wait before
                    Alice sends her basis string y_A (default 2)

    Output:
    s_0 -- list of l bits
    s_1 -- list of l bits
    """
    #Step 1. Alice randomly picks x_A and y_B in {0,1}^n.
    x_A = [randint(2) for i in range(n)]
    y_A = [randint(2) for i in range(n)]

    with CQCConnection("Alice") as Alice:
        #Step 1. (Continue) Send n qubits (BB84 states) to Bob.
        for i in range(n):
            if (i+1)%20 == 0:
                Alice.sendClassical("Bob",0)
                print("Alice informs Bob she has sent {} qubits.".format(i+1))
            q = qubit(Alice)
            if x_A[i] == 1:
                q.X()
            if y_A[i] == 1:
                q.H()
            Alice.sendQubit(q,"Bob")
        print("Alice has sent {} (random) qubits to Bob.".format(n))

        #Wait time.
        print("Both parties wait {} seconds.".format(waiting_time))
        sleep(waiting_time)

        #Step 3. Alice sends y_A to Bob.
        Alice.sendClassical("Bob", y_A)
        print("Bob has received y_A.")

        #Step 4. Alice receives I_0 and I_1 from Bob.
        data0 = Alice.recvClassical()
        I_0 = list(data0)
        data1 = Alice.recvClassical()
        I_1 = list(data1)

        #Step 5. Alice randomly picks two two-universal (lxn) hash functions f_0, f_1 and
        #sends them to Bob.
        f_0 = [[randint(2) for i in range(n)] for j in range(l)] # randint(2,size=(l,n))
        f_1 = [[randint(2) for i in range(n)] for j in range(l)] # randint(2,size=(l,n))
        for i in range(l):
            Alice.sendClassical("Bob",f_0[i])
        print("Bob has received f_0.")
        for i in range(l):
            Alice.sendClassical("Bob",f_1[i])       # Need to do separately!
        print("Bob has received f_1.")
        #Construct X_0 = x_A|I_0 and X_1 = x_A|I_1.
        X_0 = []
        for i in I_0:
            X_0.append(x_A[i])
        for i in range(len(x_A) - len(I_0)):
            X_0.append(0)
        X_1 = []
        for i in I_1:
            X_1.append(x_A[i])
        for i in range(len(x_A) - len(I_1)):
            X_1.append(0)
        #Translate X_0 and X_1 into a numpy nx1 matrix.
        X_0 = matrix(X_0).transpose()
        X_1 = matrix(X_1).transpose()
        #Alice outputs s_0 = f_0(X_0) and s_1 = f_1(X_1).
        s_0 = f_0*X_0 % 2
        s_0 = [s_0[i,0] for i in range(len(s_0))]
        s_1 = f_1*X_1 % 2
        s_1 = [s_1[i,0] for i in range(len(s_1))]

    print("Alice outputs s_0 and s_1.")

    return s_0, s_1
