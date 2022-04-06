import torch
from simulator import Simulator
from HashPIM import *
from Cryptodome.Hash import SHA3_256
import random


device = torch.device('cpu')


def fromBitsToHex(bit_array):
    chars = []
    for b in range(len(bit_array) // 8):
        byte = bit_array[b*8:(b+1)*8]
        byte = byte[::-1]
        chars.append("{:02x}".format(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def testHashPIM():
    """
    Tests the HashPIM algorithm
    """

    # The parameters for the test
    row = 1024
    kr = 14
    col = 1024
    kc = 27
    b = 1600
    r = 1088
    c = b - r
    w = 64
    m = 72
    n = 37
    digest = 256


    sim = Simulator([m] * kr + [row - m * kr], [n] * kc + [col - n * kc], device=device)

    print(f'HashPIM: SHA3-256')
    print(f'Parameters: row={row}, col={col}, m={m}, n={n}, w={w} b={b}, digest={digest}')

    # Construct random bit array (limited to r-4 size)
    message_len = random.randrange(0, r-4, 8)
    message = torch.rand(size=(message_len, ), device=device) < 0.5

    padding1 = torch.tensor([0, 1])
    padding2 = torch.zeros(size=((-2-message_len)%r, ), dtype=torch.int, device=device)
    padding2[0] = 1
    padding2[-1] = 1
    padding3 = torch.zeros(size=(c, ), dtype=torch.int, device=device)

    message_padded = torch.cat((message, padding1, padding2, padding3), 0)


    # Store the vectors in the memory
    for j in range(b // w):
        for i in range(w):
            sim.memory[i][j] = message_padded[i+w*j]

    # Run the HashPIM algorithm
    HashPIM(sim, m, n)

    messege_in_bytes = [sum(b*2**x for b,x in zip(byte,range(8))) for byte in zip(*([iter(message)]*8))]
    messege_in_bytes = [int(byte) for byte in messege_in_bytes]
    messege_in_bytes = bytearray(messege_in_bytes)

    hash = (SHA3_256.new(messege_in_bytes)).hexdigest()

    output = [0] * digest

    for j in range(digest // w):
        for i in range(w):
            output[i+w*j] = int(sim.memory[i][j])

    
    output = fromBitsToHex(output)

    assert(output == hash)

    print(f'Success with {sim.latency} cycles and {sim.energy} energy\n')
    print(f'Hash: {output}\n')



if __name__ == "__main__":
    testHashPIM()
