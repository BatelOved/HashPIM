from TestHashPIM import *

def testHashPIM_SHA3_512():
    """
    Tests the HashPIM algorithm for SHA3-512
    """

    r = 576
    digest = 512

    testHashPIM(r, digest)


if __name__ == "__main__":
    testHashPIM_SHA3_512()
    