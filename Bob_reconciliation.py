from cqc.pythonLib import CQCConnection
import reedsolo

def Bob_reconciliation(c, x_c, m, n):
    """
    Perform Bob's part of reconciliation for 1-2 ROT protocol, using RS codes.

    Input arguments:
    c             -- integer, Bob's choice bit
    x_c           -- list of length n consisting of bits
    m             -- integer, length of input lists x_0 and x_1
    n             -- integer, length of input lists x_0 and x_1

    Output argument:
    x_cor         -- list of length n, corrected version of x_c

    NOTE: the number of errors that can be corrected is <= (m-n/2)
    """
    # Error handling.
    if c != 0 and c!= 1:
        raise Exception("Input c must be either 0 or 1.")
    if n != len(x_c):
        raise Exception("Input n must be the same length as x_c.")

    # Initialise code.
    rs = reedsolo.RSCodec(m-n)

    # Receive red_0 and red_1 from Alice.
    with CQCConnection("Bob") as Bob:
        red_0 = Bob.recvClassical()
        red_1 = Bob.recvClassical()

    if c == 0:
        red_c = red_0
    else:
        red_c = red_1

    # Error correction.
    enc_B = x_c + list(red_c)
    x_cor = rs.decode(enc_B)

    return list(x_cor)
