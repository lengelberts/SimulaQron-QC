from cqc.pythonLib import CQCConnection, qubit


def step_3_Alice(theta_A):
    """Alice sends her basis information theta_A to Bob.""" # Classical information
    with CQCConnection("Alice") as Alice:
        Alice.sendClassical("Bob",theta_A)
        print("Bob has received the classical information.") # Can also do without indent


def step_3_Bob():
    """Bob receives the basis information from Alice. Return basis information as a list."""
    with CQCConnection("Bob") as Bob:
        theta = Bob.recvClassical()
        return list(theta)
