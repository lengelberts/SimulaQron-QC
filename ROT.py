from time import sleep
from numpy import matrix
from numpy.random import randint
from cqc.pythonLib import CQCConnection, qubit


# ROT does not yet achieve classical communication, nor time handling is implemented yet.
def ROT(c,l,n):
    """
    Run the protocol for 1-2 ROT between Alice and Bob.

    Arguments:
    c -- integer 0 or 1, choice bit for Bob
    l -- integer <= l, length of the resulting strings s_0, s_1, and s_c
    n -- integer <= 20, length of x_A, theta_A, x_B, theta_B

    Print when communication between Alice and Bob occurs.
    At the end, print the resulting output strings (s_0 and s_1 for Alice; s_c for Bob).
    If Bob's string is not equal to the corresponding string of Alice, print an error.

    Raise an error if the input arguments are not the integers as indicated.
    """

    #Check if input arguments are valid. Otherwise, return an error.
    if n > 20:
        raise Exception("Input argument n must not be greater than 20.")
    if c != 0 and c != 1:
        raise Exception("Input argument c must be either 0 or 1.")
    if l > n: 					# Note: l must be way smaller, so adapt!
        raise Exception("Input argument l cannot be greater than n.")
    if n > 20:
        raise Exception("Input argument n must not be greater than 20.")

    #Step 1.
    #Alice randomly picks x_A and theta_B in {0,1}^n.
    x_A = [randint(2) for i in range(n)] 	# Or: x_A = random_bit_list(n)
    theta_A = [randint(2) for i in range(n)] 	# Or: theta_A = random_bit_list(n)
    #Set time to t = 0.
    
    #Alice sends n qubits to Bob, where qubit i is
    #H^{theta_A[i]}X^{x_A[i]}|0>.
    with CQCConnection("Alice") as Alice:
        for i in range(n):
            q = qubit(Alice)
            if x_A[i] == 1:
                q.X()
            if theta_A[i] == 1:
                q.H()
            Alice.sendQubit(q,"Bob")
    print("Alice sends {} (random) qubits to Bob.".format(n))


    #Step 2.
    #Bob randomly picks theta_B in {0,1}^n.
    theta_B = [randint(2) for i in range(n)] 	# Or: theta_B = random_bit_list(n)
    #Bob measures the ith received qubit in basis theta_B[i] for
    #each i, and obtains x_B (list of length n, containing 0s and 1s).
    x_B = []
    with CQCConnection("Bob") as Bob:
        for i in range(n):
            q = Bob.recvQubit()
            if theta_B[i] == 1:
                q.H()
            m = q.measure()
            x_B.append(m)


    #Wait time.
    waiting_time = 2 # Seconds
    print("Both parties wait {} seconds.".format(waiting_time))
    sleep(waiting_time)


    #Step 3.
    #Alice sends theta_A to Bob.
    
    print("Alice sends her basis information to Bob.")


    #Step 4.
    #Bob, given his choice bit c, forms the sets I_c and I_cbar.
    I_c = []
    I_cbar = []
    for i in range(n):
        if theta_A[i] == theta_B[i]:
            I_c.append(i)
        else:
            I_cbar.append(i)
    #Form I_0 and I_1.
    if c == 0:
        I_0 = I_c
        I_1 = I_cbar
    else:
        I_0 = I_cbar
        I_1 = I_c
    #Bob sends I_0 and I_1 to Alice.
    
    print("Bob sends I_0 and I_1 to Alice.")


    #Step 5.
    #Alice randomly picks two two-universal hash functions f_0, f_1.
    f_0 = randint(2,size=(l,n))
    f_1 = randint(2,size=(l,n))
    #Alice sends f_0, f_1 to Bob.
    
    print("Alice sends f_0 and f_1 to Bob.")
    #Construct X_0 = x_A|I_0 and X_1 = x_A|I_1.
    X_0 = []
    for i in I_0:
        X_0.append(x_A[i]) 			# Not i - 1!
    for i in range(len(x_A) - len(I_0)):
        X_0.append(0)
    X_1 = []
    for i in I_1:
        X_1.append(x_A[i]) 			# Not i - 1!
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
    print("Alice outputs s_0 = ",s_0)
    print("Alice outputs s_1 = ",s_1)


    #Step 6.
    #Construct X_c = x_B|I_c.
    X_c = []
    for i in I_c:
        X_c.append(x_B[i])			# Not i - 1!
    for i in range(len(x_B) - len(I_c)):
        X_c.append(0)
    #Translate X_c into a numpy nx1 matrix.
    X_c = matrix(X_c).transpose()
    #Bob outputs s_c = f_c(X_c).
    if c == 0:
        f_c = f_0
    else:
        f_c = f_1
    s_c = f_c*X_c % 2
    s_c = [s_c[i,0] for i in range(len(s_c))]
    print("Bob outputs s_c = ",s_c)

    #Check if s_c is correct. Otherwise, return an error message.
    if c == 0:
        if not s_c == s_0:
            print("Error! Bob's string does not correspond to Alice's.")
    elif c == 1:
        if not s_c == s_1:
            print("Error! Bob's string does not correspond to Alice's.")
