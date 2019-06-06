from cqc.pythonLib import CQCConnection
import reedsolo
import reeds



def Bob2_rec(B,m,n):
    rs = reedsolo.RSCodec(m-n) #init_tables(0x11d)
    enc_B = rs.encode(B)
#    print(enc_B)
    with CQCConnection("Bob") as Bob:
        alice = Bob.recvClassical()
        print(alice)

    enc_B[n:] = alice
#    print(enc_B)
    cor_B = rs.decode(enc_B)
    return cor_B


def Bob_rec(B,m,n):
    rs = reeds.init_tables(0x11d)
    enc_B = reeds.rs_encode_msg(B,m-n)
#    print(enc_B)
    with CQCConnection("Bob") as Bob:
        alice = Bob.recvClassical()
        print(alice)

    enc_B[n:] = alice
#    print(enc_B)
    cor_B = reeds.rs_correct_msg(enc_B,m-n)[0]
    return cor_B, rs


def Bob_reconciliation(B,m,n,alice):
    rs = reeds.init_tables(0x11d)
    enc_B = reeds.rs_encode_msg(B,m-n)
    print(enc_B)
    enc_B[n:] = alice
    print(enc_B)
    cor_B = reeds.rs_correct_msg(enc_B,m-n)[0]
    print(list(cor_B))
    print(cor_B)



def Bob2_reconciliation(B,m,n,alice):
    rs = reedsolo.RSCodec(m-n)
    enc_B = rs.encode(B)
    enc_B[n:] = alice
    A_hat = rs.decode(enc_B)
    print(list(enc_B))
    print(A_hat)
