from TestHashPIM import *

def testHashPIM_SHA3_224():
    """
    Tests the HashPIM algorithm for SHA3-224
    """

    r = 1152
    digest = 224

    testHashPIM(r, digest)


if __name__ == "__main__":
    testHashPIM_SHA3_224()
    