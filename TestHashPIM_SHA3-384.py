from TestHashPIM import *

def testHashPIM_SHA3_384():
    """
    Tests the HashPIM algorithm for SHA3-384
    """

    r = 832
    digest = 384

    testHashPIM(r, digest)


if __name__ == "__main__":
    testHashPIM_SHA3_384()
    