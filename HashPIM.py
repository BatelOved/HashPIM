from Utilities import *
from math import ceil, log2



def HashPIM(sim: Simulator, m: int, n: int):
    """
    Performs the HashPIM algorithm of SHA-3.
    :param sim: the simulation environment
    :param m: the number of rows in each partition
    :param n: the number of columns in each partition
    """

    b = 1600
    w = 64
    Rnd = 24

    RC = [0]*Rnd
    RC[0]  = 0x0000000000000001
    RC[1]  = 0x0000000000008082
    RC[2]  = 0x800000000000808A
    RC[3]  = 0x8000000080008000
    RC[4]  = 0x000000000000808B
    RC[5]  = 0x0000000080000001
    RC[6]  = 0x8000000080008081
    RC[7]  = 0x8000000000008009
    RC[8]  = 0x000000000000008A
    RC[9]  = 0x0000000000000088
    RC[10] = 0x0000000080008009
    RC[11] = 0x000000008000000A
    RC[12] = 0x000000008000808B
    RC[13] = 0x800000000000008B
    RC[14] = 0x8000000000008089
    RC[15] = 0x8000000000008003
    RC[16] = 0x8000000000008002
    RC[17] = 0x8000000000000080
    RC[18] = 0x000000000000800A
    RC[19] = 0x800000008000000A
    RC[20] = 0x8000000080008081
    RC[21] = 0x8000000000008080
    RC[22] = 0x0000000080000001
    RC[23] = 0x8000000080008008

    ROT = [0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14]

    sim.kc = sim.kc - 1
    sim.kr = sim.kr - 1

    for j in range(w):
        for ir in range(Rnd):
            for rp in range(sim.kr):
                sim.memory[sim.relToAbsRow(rp, j), sim.col_partition_starts[sim.kc] + ir] = int(format((RC[ir]),'064b')[w-j-1])

    for j in range(b // w):
        for cp in range(sim.kc):
            for i in range(ceil(log2(w))):
                sim.memory[sim.row_partition_starts[sim.kr] + i, sim.relToAbsCol(cp, j)] = int(format((ROT[j]),'06b')[ceil(log2(w))-i-1])

    sim.perform(ParallelOperation([Operation(GateType.INIT0, GateDirection.IN_ROW, [], [sim.c-1], 
            sum([[j + sim.row_partition_starts[rp] for j in range(w)] for rp in range(sim.kr)], []))]))

    sim.perform(ParallelOperation([Operation(GateType.INIT0, GateDirection.IN_COLUMN, [], [sim.r-1], 
            sum([[j + sim.col_partition_starts[cp] for j in range(b // w)] for cp in range(sim.kc)], []))]))

    for ir in range(Rnd):
        HashPIM_f(sim, m, n, ir, Rnd, w, b)



def HashPIM_f(sim: Simulator, m: int, n: int, ir: int, Rnd: int, w: int, b: int):
    """
    Performs the HashPIM algorithm of SHA-3.
    :param sim: the simulation environment
    :param m: the number of rows in each partition
    :param n: the number of columns in each partition
    :param ir: the Keccak-f round
    """
    
    x = 5
    y = 5


    rc = list(range(sim.col_partition_starts[sim.kc], sim.col_partition_starts[sim.kc] + Rnd))
    rot = list(range(sim.row_partition_starts[sim.kr], sim.row_partition_starts[sim.kr] + ceil(log2(w))))

    col_intermediates = list(range(b // w, n))
    row_intermediates = list(range(w, m))

    col_mask  = sum([[j + sim.row_partition_starts[rp] for j in range(w)] for rp in range(sim.kr)], [])
    row_mask1 = sum([[j + sim.col_partition_starts[cp] for j in range(b // w)] for cp in range(sim.kc)], [])
    row_mask2 = sum([[j + col_intermediates[5] + sim.col_partition_starts[cp] for j in range(5)] for cp in range(sim.kc)], [])


    ## THETA Step

    A = [[i + 5 * j for j in range(y)] for i in range(x)]

    # Intermediate initialization
    INIT1(sim, col_intermediates, GateDirection.IN_ROW, col_mask)
    INIT1(sim, row_intermediates, GateDirection.IN_COLUMN, row_mask1)

    # C[x] = A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4]
    C = col_intermediates[0:x]
    C_r = col_intermediates[x:2*x]
    
    for i in range(x):
        XOR(sim, A[i][0], A[i][1], col_intermediates[5], GateDirection.IN_ROW, col_mask)
        XOR(sim, A[i][2], A[i][3], col_intermediates[6], GateDirection.IN_ROW, col_mask)
        XOR(sim, A[i][4], col_intermediates[5], col_intermediates[7], GateDirection.IN_ROW, col_mask)
        XOR(sim, col_intermediates[6], col_intermediates[7], C[i], GateDirection.IN_ROW, col_mask)
        INIT1(sim, col_intermediates[5:8], GateDirection.IN_ROW, col_mask)

    INIT0(sim, [col_intermediates[10]], GateDirection.IN_ROW, col_mask)
    INIT1(sim, C_r, GateDirection.IN_ROW, col_mask)

    # Copy C[x]
    for i in range(x):
        OR(sim, C[i], col_intermediates[10], C_r[i], GateDirection.IN_ROW, col_mask)

    INIT0(sim, [row_intermediates[1]], GateDirection.IN_COLUMN, row_mask2)
    INIT1(sim, [row_intermediates[0]], GateDirection.IN_COLUMN, row_mask2)

    # Rotation C[x] <<< 1
    for i in range(w):
        OR(sim, row_intermediates[0] - i - 1, row_intermediates[1], row_intermediates[0] - i, GateDirection.IN_COLUMN, row_mask2)
        INIT1(sim, [row_intermediates[0] - i - 1], GateDirection.IN_COLUMN, row_mask2)

    OR(sim, row_intermediates[0], row_intermediates[1], row_intermediates[0] - w, GateDirection.IN_COLUMN, row_mask2) 
    
    # D[x] = C[x-1] ^ C_r[x+1]
    for i in range(x):
        INIT1(sim, [col_intermediates[10]], GateDirection.IN_ROW, col_mask)
        XOR(sim, C[(i-1)%x], C_r[(i+1)%x], col_intermediates[10], GateDirection.IN_ROW, col_mask)
        INIT0(sim, [C[(i-1)%x]], GateDirection.IN_ROW, col_mask)

        # A[x][y] = A[x][y] ^ D[x]
        for j in range(y):
            INIT1(sim, [col_intermediates[11]], GateDirection.IN_ROW, col_mask)
            XOR(sim, A[i][j], col_intermediates[10], col_intermediates[11], GateDirection.IN_ROW, col_mask)
            INIT1(sim, [A[i][j]], GateDirection.IN_ROW, col_mask)
            OR(sim, C[(i-1)%x], col_intermediates[11], A[i][j], GateDirection.IN_ROW, col_mask)


    ## Rho Step

    INIT0(sim, [row_intermediates[0]], GateDirection.IN_COLUMN, row_mask1)

    for i in range(ceil(log2(w))):
        INIT1(sim, row_intermediates[1:5], GateDirection.IN_COLUMN, row_mask1)
        for rp in range(sim.kr):
            sim.perform(ParallelOperation([Operation(GateType.OR, GateDirection.IN_COLUMN,
                            [rot[i], sim.r-1], [sim.relToAbsRow(rp, row_intermediates[1])], row_mask1)]))
            
        NOT(sim, row_intermediates[1], row_intermediates[2], GateDirection.IN_COLUMN, row_mask1)

        d1 = sim.row_partition_starts[0]
        d0 = (d1 + 2 ** i) % w

        INIT1(sim, [row_intermediates[4]], GateDirection.IN_COLUMN, row_mask1)
        OR(sim, d1, row_intermediates[0], row_intermediates[4], GateDirection.IN_COLUMN, row_mask1)

        is_rot = [False]*w

        for j in range(w):
            if is_rot[d0] is True:
                d0 += 1
                d1 += 1
                INIT1(sim, row_intermediates[3:5], GateDirection.IN_COLUMN, row_mask1)
                OR(sim, d1, row_intermediates[0], row_intermediates[4], GateDirection.IN_COLUMN, row_mask1)
            
            INIT1(sim, row_intermediates[5:7], GateDirection.IN_COLUMN, row_mask1)

            if (j % 2 == 0):
                INIT1(sim, [row_intermediates[3]], GateDirection.IN_COLUMN, row_mask1)
                OR(sim, d0, row_intermediates[0], row_intermediates[3], GateDirection.IN_COLUMN, row_mask1)
                INIT1(sim, [d0], GateDirection.IN_COLUMN, row_mask1)
                MUX2(sim, row_intermediates[3], row_intermediates[4], row_intermediates[1], row_intermediates[2], 
                    d0, row_intermediates[5:7], GateDirection.IN_COLUMN, row_mask1)

            else:
                INIT1(sim, [row_intermediates[4]], GateDirection.IN_COLUMN, row_mask1)
                OR(sim, d0, row_intermediates[0], row_intermediates[4], GateDirection.IN_COLUMN, row_mask1)
                INIT1(sim, [d0], GateDirection.IN_COLUMN, row_mask1)
                MUX2(sim, row_intermediates[4], row_intermediates[3], row_intermediates[1], row_intermediates[2], 
                    d0, row_intermediates[5:7], GateDirection.IN_COLUMN, row_mask1)

            is_rot[d0] = True

            d1 = (d1 + 2 ** i) % w
            d0 = (d0 + 2 ** i) % w


    ## Pi Step

    INIT0(sim, [col_intermediates[-1]], GateDirection.IN_ROW, col_mask)
    INIT1(sim, col_intermediates[:-1], GateDirection.IN_ROW, col_mask)
    
    temp_i = 0
    curr_x = 1
    curr_y = 0

    OR(sim, A[curr_x][curr_y], col_intermediates[-1], col_intermediates[temp_i], GateDirection.IN_ROW, col_mask)

    for i in range(b // w - 1):
        if temp_i >= len(col_intermediates) - 2:
            INIT1(sim, [col_intermediates[0]], GateDirection.IN_ROW, col_mask)
            OR(sim, col_intermediates[temp_i], col_intermediates[-1], col_intermediates[0], GateDirection.IN_ROW, col_mask)
            INIT1(sim, col_intermediates[1:-1], GateDirection.IN_ROW, col_mask)
            temp_i = 0
              
        next_x = curr_y
        next_y = (2*curr_x+3*curr_y) % x
                

        OR(sim, A[next_x][next_y], col_intermediates[-1], col_intermediates[temp_i + 1], GateDirection.IN_ROW, col_mask)
        INIT1(sim, [A[next_x][next_y]], GateDirection.IN_ROW, col_mask)
        OR(sim, col_intermediates[temp_i], col_intermediates[-1], A[next_x][next_y], GateDirection.IN_ROW, col_mask)

        curr_x = next_x
        curr_y = next_y
        temp_i += 1


    ## Chi Step

    for j in range(y):
        INIT1(sim, col_intermediates[:-1], GateDirection.IN_ROW, col_mask)
        temp_i = 0

        for i in range(x):
            NOT(sim, A[i][j], col_intermediates[temp_i], GateDirection.IN_ROW, col_mask)
            temp_i += 1
        
        for i in range(x):
            NOR(sim, A[(i+1) % x][j], col_intermediates[(i+2) % x], col_intermediates[temp_i], GateDirection.IN_ROW, col_mask)
            temp_i += 1

        INIT1(sim, col_intermediates[:x], GateDirection.IN_ROW, col_mask)

        for i in range(x):
            XOR(sim, A[i][j], col_intermediates[x + i], col_intermediates[i], GateDirection.IN_ROW, col_mask)

        INIT1(sim, [A[0][j], A[1][j], A[2][j], A[3][j], A[4][j]], GateDirection.IN_ROW, col_mask)

        for i in range(x):
            OR(sim, col_intermediates[i], col_intermediates[-1], A[i][j], GateDirection.IN_ROW, col_mask)


    ## Iota Step

    # A[0][0] = A[0][0] ^ RC[i]
    INIT1(sim, col_intermediates[:2], GateDirection.IN_ROW, col_mask)
    
    for cp in range(sim.kc):
        sim.perform(ParallelOperation([Operation(GateType.OR, GateDirection.IN_ROW,
                    [rc[ir], sim.c-1], [sim.relToAbsCol(cp, col_intermediates[0])], col_mask)]))
    XOR(sim, A[0][0], col_intermediates[0], col_intermediates[1], GateDirection.IN_ROW, col_mask)
    INIT1(sim, [A[0][0]], GateDirection.IN_ROW, col_mask)
    OR(sim, col_intermediates[1], col_intermediates[-1], A[0][0], GateDirection.IN_ROW, col_mask)
