from time import sleep
from numpy import matrix, random
from cqc.pythonLib import CQCConnection, qubit
import reeds

reeds.init_tables(0x11d)

def Alice_robust_ROT(l, n=20, m=30, waiting_time=2): # adapt default values
    """
    Perform robust 1-2 ROT for Alice and return two random strings of length l.

    Input arguments:
    l            -- integer, length of output lists (must be smaller than n)
    n            -- integer, length of x_A and y_A (default 20 < m)
    m            -- integer, length of RS encoded lists (default 30)
    waiting_time -- integer, number of seconds that Alice and Bob wait after
                    step 3 during the protocol (default 2)

    Output:
    s_0          -- list of l bits
    s_1          -- list of l bits

    Encoding is handled via reedsolo.
    NOTE: We can correct up to (m-n)/2 errors with RS encoding/decoding.
    """
    # Error handling.
    if l > n:
        raise Exception("Input argument l cannot be greater than n.")
    if n > m:
        raise Exception("Input argument n cannot be greater than m.")

    # (Step 1)
    # Alice randomlys picks x_A and y_B in {0,1}^n.
    x_A = [random.randint(2) for i in range(n)]
    y_A = [random.randint(2) for i in range(n)]

    with CQCConnection("Alice") as Alice:
        # (Step 3)
        # Alice sends each send x_A[i] encoded in basis y_A[i] to Bob.
        for i in range(n):
            q = qubit(Alice)
            if x_A[i] == 1:
                q.X()
            if y_A[i] == 1:
                q.H()
            Alice.sendQubit(q, "Bob")
 #           # Wait 1 second before sending next qubit
 #           sleep(1)
 #           print("Time slot t = {}.".format(i))
        print("Alice has sent {} (random) qubits to Bob.".format(n))

        # Wait.
        print("Both parties wait {} seconds.".format(waiting_time))
        sleep(waiting_time)

        # (Step 4)
        # Alice sends y_A to Bob.
    #with CQCConnection("Alice") as Alice:
        Alice.sendClassical("Bob", y_A)
        print("Alice has sent y_A to Bob.")

        # (Step 5)
        # Alice receives I_0 and I_1 from Bob.
        data0 = Alice.recvClassical()
        I_0 = list(data0)
        data1 = Alice.recvClassical()
        I_1 = list(data1)

        # (Step 6)
        # Alice randomly picks two two-universal (lxn) hash functions
        # f_0, f_1 and sends them to Bob.
        f_0 = [[random.randint(2) for i in range(n)] for j in range(l)]
        f_1 = [[random.randint(2) for i in range(n)] for j in range(l)]
        for i in range(l):
            Alice.sendClassical("Bob", f_0[i])
        print("Alice has sent f_0.")
#        Alice.recvClassical()
        for i in range(l):
            Alice.sendClassical("Bob", f_1[i])
        print("Alice has sent f_1.")
#        Alice.recvClassical()

        # Alice constructs x_0 = x_A|I_0 and x_1 = x_A|I_1.
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

        # Information reconciliation part:
        # Alice sends red_0 and red_1 to Bob.
        # Initialise RS code.
#        rs = reedsolo.RSCodec(m-n)
        # Alice encodes x_0 and x_1 and forms red_0, red_0 consisting
        # of the last (m-n) "redundancy" bits of the encoded lists.
        enc_0 = reeds.rs_encode_msg(x_0,m-n)
        enc_1 = reeds.rs_encode_msg(x_1,m-n)
        red_0 = enc_0[n:] # n is length of x_0 and x_1
        red_1 = enc_1[n:]
        Alice.sendClassical("Bob", red_0)
        print("Alice has sent red_0 = {}.".format(red_0))
#        Alice.recvClassical()
        print("Alice recv 1")
        Alice.sendClassical("Bob", red_1)
        print("Alice")
        Alice.recvClassical()
        print("Alice recv 2")
        # Translate x_0 and x_1 into a numpy nx1 matrix for computation.
        x_0 = matrix(x_0).transpose()
        x_1 = matrix(x_1).transpose()
        # Alice computes s_0 = f_0(x_0) and s_1 = f_1(x_1).
        s_0 = f_0*x_0 % 2
        s_0 = [s_0[i,0] for i in range(len(s_0))]
        s_1 = f_1*x_1 % 2
        s_1 = [s_1[i,0] for i in range(len(s_1))]

        Alice.recvClassical()
    print("Alice outputs s_0 and s_1.")

    return s_0, s_1
