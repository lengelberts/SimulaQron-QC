from cqc.pythonLib import CQCConnection
import reedsolo
import reeds



def Alice2_rec(A,m,n):
    rs = reedsolo.RSCodec(m-n) #reeds.init_tables(0x11d)
    enc_A = rs.encode(A)
    print(enc_A)
    red_A = enc_A[n:]
    with CQCConnection("Alice") as Alice:
        Alice.sendClassical("Bob",red_A)
    print("Alice sends red_A = {}".format(red_A))



def Alice_rec(A,m,n):
    rs = reeds.init_tables(0x11d)
    enc_A = reeds.rs_encode_msg(A,m-n)
    print(enc_A)
    red_A = enc_A[n:]
    with CQCConnection("Alice") as Alice:
        Alice.sendClassical("Bob",red_A)
    print("Alice sends red_A = {}".format(red_A))
    return rs



def Alice_reconciliation(A,m,n):
    rs = reeds.init_tables(0x11d)
    enc_A = reeds.rs_encode_msg(A,m-n)
    print(enc_A)
    red_A = enc_A[n:]
    print("Alice sends red_A = {}".format(red_A))
    print(enc_A)



def Alice2_reconciliation(A,m,n):
    rs = reedsolo.RSCodec(m-n)
    enc_A = rs.encode(A)
    red_A = enc_A[n:]
    print("Alice sends red_A = {}".format(red_A))
    #with ... send
    # note must do x and x
