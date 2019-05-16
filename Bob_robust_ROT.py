from numpy import matrix
from numpy.random import randint
from cqc.pythonLib import CQCConnection, qubit

def Bob_robust_ROT(c, l, n=20, H):
    """
    Return string s_c from Alice, obtained from 1-2 ROT.

    Input arguments:
    c -- integer 0 or 1, Bob's choice bit c
    l -- integer, length of output lists (<= n)
    n -- integer, length of y_B (default 20)
    H -- (n-k)xn matrix, parity-check matrix used for reconciliation

    Output:
    s_c -- list of l bits corresponding to the string s_i that Alice outputs for i = c
    """
    #Step 2. Randomly pick y_B in {0,1}^n.
    y_B = [randint(2) for i in range(n)]

    with CQCConnection("Bob") as Bob:
        #Step 3 (part Bob). At time t = i, for each i in [n], measure the incoming
        #qubit in basis y_B[i]. Save outcomes in a list x_B (of length n).
        x_B = []
        for i in range(n):
            if (i+1)%20 == 0:
                data = Bob.recvClassical()
                print("Bob received {} qubits.".format(i+1))
            q = Bob.recvQubit()
            if y_B[i] == 1:
                q.H()
            m = q.measure()
            x_B.append(m)

        #Wait time.

        #Step 4 (part Bob). Receive y_A from Alice.
        basisinfo = Bob.recvClassical()
        y_A = list(basisinfo)

        #Step 5 (part Bob). Form the sets I_c and I_cbar. Send I_0 and I_1 to Alice.
        I_c = []
        I_cbar = []
        for i in range(n):
            if y_A[i] == y_B[i]:
                I_c.append(i)
            else:
                I_cbar.append(i)
        if c == 0:
            I_0 = I_c
            I_1 = I_cbar
        else:
            I_0 = I_cbar
            I_1 = I_c
        Bob.sendClassical("Alice",I_0)
        print("Alice has received I_0.")
        Bob.sendClassical("Alice",I_1)
        print("Alice has received I_1.")

        #Step 6 (part Bob). Receive f_0, f_1, z_0, z_1 from Alice,
        #where f_i is a list of l lists each containing n elements
        #and z_i is the syndrome computed by Alice (for i in [0,1]).
        f_0 = []
        for i in range(l):
            data0 = Bob.recvClassical()
            f_0.append(list(data0))
        f_1 = []
        for i in range(l):
            data1 = Bob.recvClassical()
            f_1.append(list(data1))
        syn0 = Bob.recvClassical()
        z_0 = list(syn0)
        syn1 = Bob.recvClassical()
        z_1 = list(syn1)

        #Step 7. Correct errors on x_B|I_c and output estimated s_c_hat.
        #Construct X_c = x_B|I_c.
        X_c = []
        for i in I_c:
            X_c.append(x_B[i])
        for i in range(len(x_B) - len(I_c)):
            X_c.append(0)
        #Translate X_c into a numpy nx1 matrix.
        X_c = matrix(X_c).transpose()
        #Initialise f_c and z_c.
        if c ==0:
            f_c = f_0
            z_c = z_0
        else:
            f_c = f_1
            z_c = z_1
        #Correct errors.
        X_cor = decoding(X_c,z_c,H)
        #Output s_c_hat = f_c(X_cor).
        s_c_hat = f_c*X_cor % 2
        s_c_hat = [s_c_hat[i,0] for i in range(len(s_c_hat))]

    print("Bob outputs his estimation for s_c.")

    return s_c_hat



def decoding(X_c, z_c, H):
    """
    Use z_c and H to correct the errors on X_c and return corrected list.

    Input arguments:
    X_c -- list of length n, Bob's x_B|I_c (!= x_A|I_c in case of noise)
    z_c -- list of length k, syndrome of Alice's x_A|I_c
    H   -- (n-k)xn matrix, parity-check matrix on which Alice and Bob agreed

    Output:
    X_cor -- corrected list of same length as X_c
    """
    X_cor = 

    return X_cor

