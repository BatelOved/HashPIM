from TestHashPIM import *

def testHashPIM_SHA3_256():
    """
    Tests the HashPIM algorithm for SHA3-256
    """

    r = 1088
    digest = 256

    testHashPIM(r, digest)
    

if __name__ == "__main__":
    testHashPIM_SHA3_256()
    