#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Kevin
#
# Created:     24/06/2013
# Copyright:   (c) Kevin 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#!/usr/bin/env python

import random
from random import shuffle, choice, randint

class Position(object):
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C

    def toList(self):
        return [self.A, self.B, self.C]

    def sort(self):
        return sorted(toList(self))

    def equals(self, other):
        return sort(self) == sort(other);

class SortedPosition(Position):
    def __init__(self, A, B, C):
        self.A = min(A, B, C)
        self.B = sorted([A, B, C])[1]
        self.C = max(A, B, C)

    def toList(self):
        return (self.A, self.B, self.C)

    def sort(self):
        return toList(self)

    def equals(self, other):
        return self.A == other.A and self.B == other.B and self.C == other.C

class Position4(object):
    def __init__(self, A, B, C, D):
        self.A = A
        self.B = B
        self.C = C
        self.D = D

    def toList(self):
        return [self.A, self.B, self.C, self.D]

    def sort(self):
        return sorted(toList(self))

    def equals(self, other):
        return sort(self) == sort(other);

class SortedPosition4(Position4):
    def __init__(self, A, B, C, D):
        self.A = min(A, B, C, D)
        self.B = sorted([A, B, C, D])[1]
        self.C = sorted([A, B, C, D])[2]
        self.C = max(A, B, C, D)

    def toList(self):
        return (self.A, self.B, self.C, self.D)

    def sort(self):
        return toList(self)

    def equals(self, other):
        return self.A == other.A and self.B == other.B and self.C == other.C and self.D == other.D

def generateWinners(): #all positions are sorted
    PPositions = [Position(1,1,1).sort()]
    for k in range(101):
        PPositions.append(Position(0,k,k).sort())
        PPositions.append(Position(0,2*k,2*k+1).sort())
        PPositions.append(Position(2*k-1,2*k,2*k).sort())
        PPositions.append(Position(k,2*k+1,2*k+1).sort())
    for x in range(1,101):
        for y in range (x+1,101):
            PPositions.append(Position(x,y,x+y+1).sort())
    return PPositions

def primitive(posn):
    return posn.A < 2 and posn.B < 2 and posn.C < 2

def gameplay():
    pileA = random.randint(1,101)
    pileB = random.randint(1,101)
    pileC = random.randint(1,101)
    PPositions = generateWinners()
    print ('This is a game of 3-pile Nim.')
    print ('You may take any number of counters you like from any one pile.')
    print ('However, before each turn, your opponent must block one move from a certain pile.')
    print ('The first player to have no legal moves left loses.')
    print ('Pile A has ' + str(pileA) + ' counters.')
    print ('Pile B has ' + str(pileB) + ' counters.')
    print ('Pile C has ' + str(pileC) + ' counters.')
    numberOfMoves = 0
    while not primitive(Position(pileA, pileB, pileC)):
        current = Position(pileA, pileB, pileC)
        span = generateMoves(current)
        blockable = []
        for x in range(pileA + 1):
            for y in range (pileB + 1):
                for z in range (pileC + 1):
                    if Position(x, y, z).toList() in span and Position(x, y, z).sort() in PPositions and (Position(x, y, z).toList() not in blockable):
                        blockable.append(Position(x, y, z).toList())
        if len(blockable) == 0:
            random.shuffle(span)
            blockTarget = span[0]
            span.remove(blockTarget)
            inputPosition = choice(span)
        elif len(blockable) == 1:
            blockTarget = blockable[0]
            span.remove(blockTarget)
            inputPosition = choice(span)
        else:
            random.shuffle(blockable)
            blockTarget = blockable[0]
            blockable.remove(blockTarget)
            inputPosition = choice(blockable)
        pileA = inputPosition[0]
        pileB = inputPosition[1]
        pileC = inputPosition[2]
        numberOfMoves += 1
        print ('After ' + str(numberOfMoves) + ' moves, the position ' + str(blockTarget) + ' was blocked.')
        print ('Pile A has ' + str(pileA) + ' counters.')
        print ('Pile B has ' + str(pileB) + ' counters.')
        print ('Pile C has ' + str(pileC) + ' counters.')
    print ('The game is over.')
    if numberOfMoves % 2 == 1:
        print ('Player 1 has won.')
    else:
        print ('Player 2 has won.')

def generateMoves(position): #not sorted, piles distinguishable
    pileA, pileB, pileC = position.A, position.B, position.C
    span = []
    for k in reversed(range(0, pileA)):
        span.append(Position(k, pileB, pileC).toList())
    if pileB != pileA:
        for k in reversed(range(0, pileB)):
            span.append(Position(pileA, k, pileC).toList())
    if pileC != pileA and pileC != pileB:
        for k in reversed(range(0, pileC)):
            span.append(Position(pileA, pileB, k).toList())
    return span

grundycache = {}
miserecache = {}

def grundy(position): #need tuples for dict keys
    lst = position.toList()
    ordered = SortedPosition(lst[0], lst[1], lst[2]).toList()
    if ordered in grundycache:
        return grundycache[ordered] 
    cache = generateMoves(position)
    if not cache:
        grundycache[ordered] = 0
        return 0
    values = []
    for x in cache:
        values.append(grundy(Position(x[0], x[1], x[2])))
    grundycache[ordered] = mex(values, 2)
    return grundycache[ordered]

def misere_grundy(position): #need tuples for dict keys
    lst = position.toList()
    ordered = SortedPosition(lst[0], lst[1], lst[2]).toList()
    miserecache[SortedPosition(0,0,0)] = float("inf")
    if ordered in miserecache:
        return miserecache[ordered] 
    cache = generateMoves(position)
    try:
        while True:
            cache.remove([0,0,0])
    except:
        pass
    if not cache:
        miserecache[ordered] = 0
        return 0
    values = []
    for x in cache:
        values.append(misere_grundy(Position(x[0], x[1], x[2])))
    miserecache[ordered] = mex(values, 2)
    return miserecache[ordered]

def mex(vals, count = 1):
    result = 0
    while vals.count(result) >= count:
        result += 1
    return result

def generateWinnersGeneral():
    PPositions = [Position(0, 0, 0).toList()]
    for x in range(101):
        for y in range (x, 101):
            for z in range (x + y, 101):
                if grundy(Position(x, y, z)) == 0:
                    PPositions += [Position(x, y, z).toList()]
    return PPositions
