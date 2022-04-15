import torch
import random
from simulator import Simulator
from HashPIM import *
from Cryptodome.Hash import SHA3_224, SHA3_256, SHA3_384, SHA3_512


device = torch.device('cpu')



def testHashPIM(r: int, digest: int):
    """
    Tests the HashPIM algorithm
    :param r: the SHA-3 rate = {1152,1088,832,576}
    :param digest: the SHA-3 hash value size = {224,256,384,512}



    Simulator parameters:
    :param row: the number of memristive rows in the crossbar array e.g., 512, 1024
    :param col: the number of memristive columns in the crossbar array e.g., 512, 1024
    :param r_u: the number of SHA-3 units vertically in the crossbar array (optimal value: floor((row-log(w)-1)/m))
    :param c_u: the number of SHA-3 units horizontally in the crossbar array (optimal value: floor((col-Rnd-1)/n))
    """

    row = 1024
    col = 1024
    r_u = 14
    c_u = 27

    # Total number of SHA-3 units in a crossbar array
    N_u = r_u * c_u


    """
    SHA-3 constants:
    :param b: the Keccak-f internal state size
    :param w: the Keccak-f lane size
    :param Rnd: Keccak-f total rounds
    """

    b = 1600
    w = 64
    Rnd = 24


    """
    HashPIM constants:
    :param m: the number of rows in each SHA-3 unit
    :param n: the number of columns in each SHA-3 unit
    """

    m = 72
    n = 37


    hash_param = ((1152,224),(1088,256),(832,384),(576,512))
    

    if ((r, digest) not in hash_param):
        print("Error! allowed only: (r, digest)={(1152,224),(1088,256),(832,384),(576,512)}\n")
        quit()

    print(f'HashPIM: SHA3-{digest}')
    print(f'Parameters: rows={row}, columns={col}, SHA-3 Units={N_u}, r={r}, hash value size={digest}\n')


    sim = Simulator([m] * r_u + [row - m * r_u], [n] * c_u + [col - n * c_u], device=device)

    message = torch.zeros(size=(r_u, c_u, b), dtype=torch.int, device=device)
    message_padded = torch.zeros(size=(r_u, c_u, b), dtype=torch.int, device=device)

    hash_value = [[0 for i in range(c_u)] for j in range(r_u)]


    for i in range(r_u):
        for j in range(c_u):
            # Construct random bit array (limited to r-4 size, and to bytes for compatability with Cryptodome)
            message_len = random.randrange(0, r-4, 8)
            message[i][j][:message_len] = torch.rand(size=(message_len, ), device=device) < 0.5

            # Padding rule
            message_padded[i][j][:message_len] = message[i][j][:message_len]
            message_padded[i][j][message_len+1] = 1
            message_padded[i][j][message_len+2] = 1
            message_padded[i][j][r-1] = 1

            message_in_bytes = bytearray(sum(bit*(2**k) for bit,k in zip(byte,range(8))) for byte in zip(*([iter(message[i][j][:message_len])]*8)))

            if digest == 224:
                hash_value[i][j] = SHA3_224.new(message_in_bytes).hexdigest()

            elif digest == 256:
                hash_value[i][j] = SHA3_256.new(message_in_bytes).hexdigest()

            elif digest == 384:
                hash_value[i][j] = SHA3_384.new(message_in_bytes).hexdigest()

            elif digest == 512:
                hash_value[i][j] = SHA3_512.new(message_in_bytes).hexdigest()


    # Store the vectors in the memory
    for r_i in range(r_u):
        for c_i in range(c_u):       
            for i in range(w):
                for j in range(b // w):
                    sim.memory[i+r_i*m][j+c_i*n] = message_padded[r_i][c_i][i+j*w]


    # Run the HashPIM algorithm
    HashPIM(sim, m, n)


    out_in_bits = [0] * digest
    output = [[0 for i in range(c_u)] for j in range(r_u)]


    for r_i in range(r_u):
        for c_i in range(c_u):
            cnt = 0
            for j in range((digest // w) + 1):       
                for i in range(w):
                    cnt += 1
                    if cnt > digest:
                        break
                
                    out_in_bits[i+w*j] = int(sim.memory[i+r_i*m][j+c_i*n])

            out_in_bytes = bytearray(sum(bit*(2**k) for bit,k in zip(byte,range(8))) for byte in zip(*([iter(out_in_bits)]*8)))
            output[r_i][c_i] = "".join(["%02x" % it for it in out_in_bytes])


    for i in range(r_i):
        for j in range(c_i):
            assert(output[i][j] == hash_value[i][j])


    print(f'Success with total {sim.latency} cycles and {sim.energy} gates\n')
    print('Results (1 round):')
    print(f'Single Unit: {sim.latency//Rnd} cycles and {sim.energy//(N_u*Rnd)} gates')
    print(f'Single XB ({N_u} Units): {sim.latency//Rnd} cycles and {sim.energy//Rnd} gates\n')
