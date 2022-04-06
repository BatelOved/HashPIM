from simulator import Simulator, ParallelOperation, Operation, GateType, GateDirection


def XOR(sim: Simulator, a: int, b: int, c: int, gateDirection: GateDirection, mask=None):
    """
    Performs a row/col-parallel XOR on numbers stored in indices a and b, storing the result in b.
    :param sim: the simulation environment
    :param a: the intra-partition index of the first number
    :param b: the intra-partition index of the second number
    :param c: the intra-partition index of the output
    :param gateDirection: the direction of the gate (e.g., IN_ROW)
    :param mask: the row/col mask
    """

    if (gateDirection == gateDirection.IN_ROW):
        sim.perform(ParallelOperation([Operation(GateType.OR, GateDirection.IN_ROW,
            [sim.relToAbsCol(j, a), sim.relToAbsCol(j, b)], [sim.relToAbsCol(j, c)], mask) for j in range(sim.kc)]))

        sim.perform(ParallelOperation([Operation(GateType.NAND, GateDirection.IN_ROW,
            [sim.relToAbsCol(j, a), sim.relToAbsCol(j, b)], [sim.relToAbsCol(j, c)], mask) for j in range(sim.kc)]))

    else:
        sim.perform(ParallelOperation([Operation(GateType.OR, GateDirection.IN_COLUMN,
            [sim.relToAbsRow(j, a), sim.relToAbsRow(j, b)], [sim.relToAbsRow(j, c)], mask) for j in range(sim.kr)]))

        sim.perform(ParallelOperation([Operation(GateType.NAND, GateDirection.IN_COLUMN,
            [sim.relToAbsRow(j, a), sim.relToAbsRow(j, b)], [sim.relToAbsRow(j, c)], mask) for j in range(sim.kr)]))


def OR(sim: Simulator, a: int, b: int, c: int, gateDirection: GateDirection, mask=None):
    """
    Performs a row/col-parallel OR on numbers stored in indices a and b, storing the result in b.
    :param sim: the simulation environment
    :param a: the intra-partition index of the first number
    :param b: the intra-partition index of the second number
    :param c: the intra-partition index of the output
    :param gateDirection: the direction of the gate (e.g., IN_ROW)
    :param mask: the row/col mask
    """

    if (gateDirection == gateDirection.IN_ROW):
        sim.perform(ParallelOperation([Operation(GateType.OR, GateDirection.IN_ROW,
            [sim.relToAbsCol(j, a), sim.relToAbsCol(j, b)], [sim.relToAbsCol(j, c)], mask) for j in range(sim.kc)]))

    else:
        sim.perform(ParallelOperation([Operation(GateType.OR, GateDirection.IN_COLUMN,
            [sim.relToAbsRow(j, a), sim.relToAbsRow(j, b)], [sim.relToAbsRow(j, c)], mask) for j in range(sim.kr)]))


def NOR(sim: Simulator, a: int, b: int, c: int, gateDirection: GateDirection, mask=None):
    """
    Performs a row/col-parallel NOR on numbers stored in indices a and b, storing the result in b.
    :param sim: the simulation environment
    :param a: the intra-partition index of the first number
    :param b: the intra-partition index of the second number
    :param c: the intra-partition index of the output
    :param gateDirection: the direction of the gate (e.g., IN_ROW)
    :param mask: the row/col mask
    """

    if (gateDirection == gateDirection.IN_ROW):
        sim.perform(ParallelOperation([Operation(GateType.NOR, GateDirection.IN_ROW,
            [sim.relToAbsCol(j, a), sim.relToAbsCol(j, b)], [sim.relToAbsCol(j, c)], mask) for j in range(sim.kc)]))

    else:
        sim.perform(ParallelOperation([Operation(GateType.NOR, GateDirection.IN_COLUMN,
            [sim.relToAbsRow(j, a), sim.relToAbsRow(j, b)], [sim.relToAbsRow(j, c)], mask) for j in range(sim.kr)]))


def NOT(sim: Simulator, a: int, c: int, gateDirection: GateDirection, mask=None):
    """
    Performs a row/col-parallel NOT on numbers stored in indices a, storing the result in c.
    :param sim: the simulation environment
    :param a: the intra-partition index of the first number
    :param c: the intra-partition index of the output
    :param gateDirection: the direction of the gate (e.g., IN_ROW)
    :param mask: the row/col mask
    """

    if (gateDirection == gateDirection.IN_ROW):
        sim.perform(ParallelOperation([Operation(GateType.NOT, GateDirection.IN_ROW,
            [sim.relToAbsCol(j, a)], [sim.relToAbsCol(j, c)], mask) for j in range(sim.kc)]))

    else:
        sim.perform(ParallelOperation([Operation(GateType.NOT, GateDirection.IN_COLUMN,
            [sim.relToAbsRow(j, a)], [sim.relToAbsRow(j, c)], mask) for j in range(sim.kr)]))


def MUX2(sim: Simulator, a: int, b: int, sel: int, selN: int, c: int, intermediates: list, gateDirection: GateDirection, mask=None):
    """
    Performs a row/col-parallel MUX on numbers stored in indices a, b and sel, storing the result in c.
    :param sim: the simulation environment
    :param a: the intra-partition index of the first number
    :param b: the intra-partition index of the second number
    :param sel: the intra-partition index of the selector
    :param sel: the intra-partition index of the ~selector
    :param c: the intra-partition index of the output
    :param intermediates: the intermediates used (2 are needed)
    :param gateDirection: the direction of the gate (e.g., IN_ROW)
    :param mask: the row/col mask
    """

    if (gateDirection == gateDirection.IN_ROW):
        sim.perform(ParallelOperation([Operation(GateType.NOR, GateDirection.IN_ROW,
            [sim.relToAbsCol(j, a), sim.relToAbsCol(j, sel)], [sim.relToAbsCol(j, intermediates[0])], mask) for j in range(sim.kc)]))

        sim.perform(ParallelOperation([Operation(GateType.NOR, GateDirection.IN_ROW,
            [sim.relToAbsCol(j, b), sim.relToAbsCol(j, selN)], [sim.relToAbsCol(j, intermediates[1])], mask) for j in range(sim.kc)]))

        sim.perform(ParallelOperation([Operation(GateType.NOR, GateDirection.IN_ROW,
            [sim.relToAbsCol(j, intermediates[0]), sim.relToAbsCol(j, intermediates[1])], [sim.relToAbsCol(j, c)], mask) for j in range(sim.kc)]))

    else:
        sim.perform(ParallelOperation([Operation(GateType.NOR, GateDirection.IN_COLUMN,
            [sim.relToAbsRow(j, a), sim.relToAbsRow(j, sel)], [sim.relToAbsRow(j, intermediates[0])], mask) for j in range(sim.kr)]))

        sim.perform(ParallelOperation([Operation(GateType.NOR, GateDirection.IN_COLUMN,
            [sim.relToAbsRow(j, b), sim.relToAbsRow(j, selN)], [sim.relToAbsRow(j, intermediates[1])], mask) for j in range(sim.kr)]))

        sim.perform(ParallelOperation([Operation(GateType.NOR, GateDirection.IN_COLUMN,
            [sim.relToAbsRow(j, intermediates[0]), sim.relToAbsRow(j, intermediates[1])], [sim.relToAbsRow(j, c)], mask) for j in range(sim.kr)]))


def INIT0(sim: Simulator, a: list, gateDirection: GateDirection, mask=None):
    """
    Performs a row/col-parallel INIT0 storing the result in a.
    :param sim: the simulation environment
    :param a: the intra-partition index of the output
    :param gateDirection: the direction of the gate (e.g., IN_ROW)
    :param mask: the row/col mask
    """

    if (gateDirection == gateDirection.IN_ROW):
        sim.perform(ParallelOperation([Operation(GateType.INIT0, GateDirection.IN_ROW, [],
            sum([[sim.relToAbsCol(j, i) for i in a] for j in range(sim.kc)], []), mask)]))

    else:
        sim.perform(ParallelOperation([Operation(GateType.INIT0, GateDirection.IN_COLUMN, [],
            sum([[sim.relToAbsRow(j, i) for i in a] for j in range(sim.kr)], []), mask)]))


def INIT1(sim: Simulator, a: list, gateDirection: GateDirection, mask=None):
    """
    Performs a row/col-parallel INIT1 storing the result in a.
    :param sim: the simulation environment
    :param a: the intra-partition index of the output
    :param gateDirection: the direction of the gate (e.g., IN_ROW)
    :param mask: the row/col mask
    """

    if (gateDirection == gateDirection.IN_ROW):
        sim.perform(ParallelOperation([Operation(GateType.INIT1, GateDirection.IN_ROW, [],
            sum([[sim.relToAbsCol(j, i) for i in a] for j in range(sim.kc)], []), mask)]))

    else:
        sim.perform(ParallelOperation([Operation(GateType.INIT1, GateDirection.IN_COLUMN, [],
            sum([[sim.relToAbsRow(j, i) for i in a] for j in range(sim.kr)], []), mask)]))
