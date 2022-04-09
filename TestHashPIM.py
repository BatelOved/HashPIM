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
    w = 64
    m = 72
    n = 37
    Rnd = 24
    r_u = 14
    c_u = 27
    N_u = r_u * c_u
    digest = 256


    print(f'HashPIM: SHA3-256')
    print(f'Parameters: rows={row}, columns={col}, SHA-3 units={N_u}, w={w}, b={b}, digest={digest}')


    sim = Simulator([m] * kr + [row - m * kr], [n] * kc + [col - n * kc], device=device)

    message = torch.zeros(size=(r_u, c_u, b), dtype=torch.int, device=device)
    message_padded = torch.zeros(size=(r_u, c_u, b), dtype=torch.int, device=device)

    hash_value = [[0 for i in range(c_u)] for j in range(r_u)]


    for i in range(r_u):
        for j in range(c_u):
            # Construct random bit array (limited to r-4 size)
            message_len = random.randrange(0, r-4, 8)
            message[i][j][:message_len] = torch.rand(size=(message_len, ), device=device) < 0.5

            # Padding rule
            message_padded[i][j][:message_len] = message[i][j][:message_len]
            message_padded[i][j][message_len+1] = 1
            message_padded[i][j][message_len+2] = 1
            message_padded[i][j][r-1] = 1

            message_in_bytes = [sum(b*2**x for b,x in zip(byte,range(8))) for byte in zip(*([iter(message[i][j][:message_len])]*8))]
            message_in_bytes = [int(byte) for byte in message_in_bytes]
            message_in_bytes = bytearray(message_in_bytes)

            hash_value[i][j] = (SHA3_256.new(message_in_bytes)).hexdigest()


    # Store the vectors in the memory
    for r_i in range(r_u):
        for c_i in range(c_u):       
            for i in range(w):
                for j in range(b // w):
                    sim.memory[i+r_i*m][j+c_i*n] = message_padded[r_i][c_i][i+j*w]


    # Run the HashPIM algorithm
    HashPIM(sim, m, n)


    output = [[0 for i in range(c_u)] for j in range(r_u)]
    temp = [0] * digest

    for r_i in range(r_u):
        for c_i in range(c_u):       
            for i in range(w):
                for j in range(digest // w):
                    temp[i+w*j] = int(sim.memory[i+r_i*m][j+c_i*n])
                    output[r_i][c_i] = fromBitsToHex(temp)


    for i in range(r_i):
        for j in range(c_i):
            assert(output[i][j] == hash_value[i][j])


    print(f'Success with {sim.latency} cycles and {sim.energy} energy\n')
    print(f'Single SHA-3 unit 1 round evaluation: {sim.latency//Rnd} cycles and {sim.energy//(N_u*Rnd)} energy\n')



if __name__ == "__main__":
    testHashPIM()
