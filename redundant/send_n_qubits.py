from cqc.pythonLib import CQCConnection, qubit
from numpy.random import randint


def send_n_qubits_Alice(n):
    """
    Send n BB84 states from Alice to Bob.

    Input argument:
    n -- integer, number of BB84 states that will be sent

    Create n BB84 states (i.e. create n qubits and randomly decide per qubit to apply X
    and/or H. Then send the qubits from Alice to Bob.

    NOTE: The qubits are sent in phases of 20 qubits to prevent inavailability qubits.
    To let this happen, after every 20 iterations, Alice sends a classical message to Bob.
    The user is notified by a print message.
    """
    with CQCConnection("Alice") as Alice:
        for i in range(n):
            if (i+1)%20 == 0:
                Alice.sendClassical("Bob",0)
                print("Alice informs Bob she has sent {} qubits.".format(i+1))
            q = qubit(Alice)
            x = randint(2)
            if x == 1: q.X()
            h = randint(2)
            if h == 1: q.H()
            Alice.sendQubit(q,"Bob")

    #print() # Print on new line
    print("Alice has sent n={} qubits to Bob".format(n))


def recv_n_qubits_Bob(n): # Try without n
    """
    Receive n BB84 states from Alice. Print list of outcomes when measuring in + basis.

    Input argument:
    n -- integer, number of BB84 states that will be received

    Receive the n qubits (each is one of BB84 states) from Alice.
    Measure the qubits in the computational basis (the + basis).
    Print a list containing the measurement outcomes.

    NOTE: The qubits are received in phases of 20 qubits to prevent inavailability qubits.
    To let this happen, after every 20 iterations, Bob receives a classical message from
    Alice. The user is notified by a print message.
    """
    list = []
    with CQCConnection("Bob") as Bob:
        for i in range(n):
            if (i+1)%20 == 0:
                data = Bob.recvClassical()
                print("Bob received {} qubits.".format(i+1))
            q = Bob.recvQubit()
            m = q.measure()
            list.append(m)

    print() # Print on new line
    print("Bob's measurement outcomes: ",list)
