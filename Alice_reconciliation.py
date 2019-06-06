from cqc.pythonLib import CQCConnection
import reedsolo

def Alice_reconciliation(x_0, x_1, m, n):
    """
    Perform Alice's part of reconciliation for 1-2 ROT protocol, using RS codes.

    Input arguments:
    x_0           -- list of length n consisting of bits
    x_1           -- list of length n consisting of bits
    m             -- integer, length of input lists x_0 and x_1
    n             -- integer, length of input lists x_0 and x_1

    A message is printed when Alice is finished. There is no output.

    NOTE: the number of errors that can be corrected is <= (m-n/2)
    """
    # Error handling.
    if len(x_0) != len(x_1):
        raise Exception("Inputs x_0 and x_1 must be of the same length.")
    if n != len(x_0):
        raise Exception("Input n must be the same length as x_0 and x_1.")

    # Initialise code.
    rs = reedsolo.RSCodec(m-n)

    enc_0 = rs.encode(x_0)
    enc_1 = rs.encode(x_1)
    red_0 = enc_0[n:]
    red_1 = enc_1[n:]

    # Send red_0 and red_1 to Bob.
    with CQCConnection("Alice") as Alice:
        Alice.sendClassical("Bob",red_0)
        Alice.sendClassical("Bob",red_1)

    print("Alice is finished.")
    return
