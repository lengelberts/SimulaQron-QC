from random import randint
from cqc.pythonLib import CQCConnection, qubit


def step_1_and_2(n):
    """
    Send n (random) qubits from Alice to Bob and measure each in the + or x basis.

    Input:
    n -- number of qubits
    Output:
    list of n bits (i.e. integers 0 or 1) representing the measurement outcomes

    Initialise a CQCConnection for Alice. Send one of the four BB84 states, randomly
    chosen, to Bob. Repeat this process n times.
    Initialise a CQCConnection for Bob. Receive all n qubits. For each qubit, randomly
    decide to convert to Hadamard basis or stick to the computational basis.
    Measure each qubit in the corresponding basis. Return a list of measurement outcomes.
    """
    x_A = []
    h_A = []
    with CQCConnection("Alice") as Alice:
        for i in range(n):
            q = qubit(Alice)
            x = randint(0,1)
            x_A.append(x)
            h = randint(0,1)
            h_A.append(h)
            if x == 1: q.X()
            if h == 1: q.H()
            Alice.sendQubit(q,"Bob")
        #print("x_A = ",x_A)
        #print("h_A = ",h_A)

    x_B = []
    h_B = []
    with CQCConnection("Bob") as Bob:
        for i in range(n):
            h = randint(0,1)
            h_B.append(h)
            q = Bob.recvQubit()
            if h == 1: q.H()
            m = q.measure()
            x_B.append(m)
        #print("h_B = ",h_B)
        #print("x_B = ",x_B)

    return x_B

