from random import randint
from cqc.pythonLib import CQCConnection, qubit


n = 20 # Note: n > 20 gives an error


def main():
    """
    Send n BB84 states from Alice to Bob. Print list of outcomes when measuring in + basis.

    Input argument:
    n -- integer <= 20, number of BB84 states that will be sent

    Create n BB84 states (i.e. create n qubits and randomly decide per qubit to apply X
    and/or H. Then send the qubits from Alice to Bob. Bob measures the qubits in the
    computational basis (the + basis).
    Print a list containing the measurement outcomes.
    """
    with CQCConnection("Alice") as Alice:
        for i in range(n):
            q = qubit(Alice)
            x = randint(0,1)
            if x == 1: q.X()
            h = randint(0,1)
            if h == 1: q.H()
            Alice.sendQubit(q,"Bob")

    list = []
    with CQCConnection("Bob") as Bob:
        for i in range(n):              # Check if need for loop
            q = Bob.recvQubit()
            m = q.measure()
            list.append(m)

    print() # Print on new line
    print("Bob's measurement outcomes: ",list)


main()
