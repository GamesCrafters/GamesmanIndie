from game_blockis import *

mem = {}

counter = 0

def Solve(position):
    global counter

    hpos = Hash(position)

    # check if position has been memoized
    if hpos in mem:
        return mem[hpos]

    counter += 1
    if counter % 100000 == 0:
        print(counter)

    # ending position
    moves = GenerateMoves(position)
    if not moves:
        mem[hpos] = ("lose", 0)
        return mem[hpos]

    children = [Solve(DoMove(position, m)) for m in moves]

    # winning position
    minRemote = -1
    for c in children:
        if c[0] == "lose" and (minRemote == -1 or c[1] < minRemote):
            minRemote = c[1]
    if minRemote != -1:
        mem[hpos] = ("win", minRemote+1)
        return mem[hpos]

    # tying position
    minRemote = -1
    for c in children:
        if c[0] == "tie" and (minRemote == -1 or c[1] < minRemote):
            minRemote = c[1]
    if minRemote != -1:
        mem[hpos] = ("tie", minRemote+1)
        return mem[hpos]

    # losing position
    mem[hpos] = ("lose", max(c[1] for c in children)+1)
    return mem[hpos]
