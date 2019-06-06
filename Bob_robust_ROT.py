from numpy import matrix, random
from cqc.pythonLib import CQCConnection
import reedsolo

def Bob_robust_ROT(c, l, n=20, m=30):
    """
    Perform robust 1-2 ROT for Bob and return string s_c of length l without revealing c.

    Input arguments:
    c              -- integer 0 or 1, Bob's choice bit c
    l              -- integer, length of output lists (must be smaller than n)
    n              -- integer, length of y_B (default 20 < m)
    m              -- integer, length of RS encoded lists (default 30)

    Output:
    s_c            -- list of l bits corresponding to list s_c returned by Alice

    Encoding and decoding is handled via reedsolo.
    NOTE: We can correct up to (m-n)/2 errors with RS encoding/decoding.
    """
    # Error handling.
    if c != 0 and c!= 1:
        raise Exception("Input argument c must be either 0 or 1.")
    if l > n:
        raise Exception("Input argument l cannot be greater than n.")
    if n > m:
        raise Exception("Input argument n cannot be greater than m.")

    # (Step 2)
    # Bob randomly picks y_B in {0,1}^n.
    y_B = [random.randint(2) for i in range(n)]

    with CQCConnection("Bob") as Bob:
        # (Step 3)
        # Bob measures the ith incoming qubit in basis corresponding to y_B[i]
        # and obtains outcome x_B, a list of length n.
        x_B = []
        for i in range(n):
            q = Bob.recvQubit()
            if y_B[i] == 1:
                q.H()
            m = q.measure()
            x_B.append(m)

        #Wait.

        # (Step 4)
        # Bob receives y_A from Alice.
        basisinfo = Bob.recvClassical()
        y_A = list(basisinfo)

        # (Step 5)
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

        # (Step 6)
        # Bob receives f_0, f_1 from Alice.
        # Here, f_i is a list of l lists of size n.
        f_0 = []
        for i in range(l):
            data0 = Bob.recvClassical()
            f_0.append(list(data0))
        f_1 = []
        for i in range(l):
            data1 = Bob.recvClassical()
            f_1.append(list(data1))

        # (Step 7)
        # Bob constructs x_c = x_B|I_c.
        x_c = []
        for i in I_c:
            x_c.append(x_B[i])
        for i in range(len(x_B) - len(I_c)):
            x_c.append(0)

        # Bob receives red_0 and red_1 from Alice.
        red_0 = Bob.recvClassical()
        print("Bob received red_0.")
        red_1 = Bob.recvClassical()
        print("Bob received red_1.")

        # Initialise f_c and red_c.
        if c ==0:
            f_c = f_0
            red_c = red_0
        else:
            f_c = f_1
            red_c = red_1

        # Information reconciliation part:
        # Bob corrects errors on x_B|I_c and output estimated s_c_hat.
        # Initialise RS code.
        rs = reedsolo.RSCodec(m-n)
        # Bob corrects errors.
        enc_B = x_c + list(red_c)
        x_cor = rs.decode(enc_B)
        x_cor = list(x_cor)

        # Translate x_c into a numpy nx1 matrix.
        x_cor = matrix(x_cor).transpose()
        # Bob computes s_c_hat = f_c(x_cor).
        s_c_hat = f_c*x_cor % 2
        s_c_hat = [s_c_hat[i,0] for i in range(len(s_c_hat))]

    print("Bob outputs s_c_hat.")

    return s_c_hat
