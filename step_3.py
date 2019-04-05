from cqc.pythonLib import CQCConnection, qubit

def step_3(theta_A):
    """Alice sends her basis information theta_A to Bob.""" # Classical information
    with CQCConnection("Alice") as Alice:
        Alice.sendClassical("Bob",theta_A)

    with CQCConnection("Bob") as Bob:
        theta = Bob.recvClassical()
        print(list(theta))
