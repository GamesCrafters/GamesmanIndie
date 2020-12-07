class Piece:
    def __init__(self, squares):
        self.rotations = []
        while squares not in self.rotations:
            self.rotations.append(squares)
            squares = self.rotate(squares)

        self.sizes = []
        for rot in self.rotations:
            self.sizes.append((max(s[0] for s in rot) + 1, max(s[1] for s in rot) + 1))

    def rotate(self, squares):
        """Rotate 90 degrees clockwise."""
        adj_x = min(s[1] for s in squares)
        adj_y = min(-s[0] for s in squares)

        new_squares = []
        for s in squares:
            new_squares.append((s[1] - adj_x, -s[0] - adj_y))

        return new_squares

    def __str__(self):
        out = ''
        for r in range(5):
            for rot in self.rotations:
                for c in range(5):
                    out += ('#' if (r,c) in rot else ' ')
            out += '\n'

        return out

TETRIS = [
    Piece([(0,0),(0,1),(0,2),(0,3)]),
    Piece([(0,0),(1,0),(1,1),(1,2)]),
    Piece([(0,2),(1,0),(1,1),(1,2)]),
    Piece([(0,0),(0,1),(1,0),(1,1)]),
    Piece([(0,1),(0,2),(1,0),(1,1)]),
    Piece([(0,1),(1,0),(1,1),(1,2)]),
    Piece([(0,0),(0,1),(1,1),(1,2)])
]

# Game constants
# --------------
W = 4
H = 5
ADJACENCY = False # do new pieces need to connect with old pieces?
P1_START = (0, 0)
P2_START = (H - 1, W - 1)
SINGLE_USE = False # can pieces only be used once?
PIECES = [Piece([(1,0),(1,1),(0,0)])]
# W = 7
# H = 7
# ADJACENCY = False # do new pieces need to connect with old pieces?
# P1_START = (0, 0)
# P2_START = (H - 1, W - 1)
# SINGLE_USE = True # can pieces only be used once?
# PIECES = TETRIS
# W = 14
# H = 14
# ADJACENCY = True # do new pieces need to connect with old pieces?
# P1_START = (0, 0)
# P2_START = (H - 1, W - 1)
# SINGLE_USE = True # can pieces only be used once?
# PIECES = TETRIS
# --------------

class Position:
    def __init__(self):
        self.board = [[0]*W for _ in range(H)]
        self.p1_pieces = [i for i in range(len(PIECES))]
        self.p2_pieces = [i for i in range(len(PIECES))]
        self.turn = 0

    def copy(self):
        pos = Position()
        for r in range(H):
            for c in range(W):
                pos.board[r][c] = self.board[r][c]
        pos.p1_pieces = self.p1_pieces[:]
        pos.p2_pieces = self.p2_pieces[:]
        pos.turn = self.turn
        return pos

def Hash(pos):
    return str(pos.board) + str(pos.p1_pieces) + str(pos.p2_pieces) + str(pos.turn)

# move - (piece index, rotation index, row, column)
def DoMove(pos, move):
    newpos = pos.copy()

    arr = newpos.p1_pieces if pos.turn % 2 == 0 else newpos.p2_pieces
    player = pos.turn % 2 + 1
    rot = PIECES[arr[move[0]]].rotations[move[1]]

    for s in rot:
        newpos.board[move[2] + s[0]][move[3] + s[1]] = player

    if SINGLE_USE:
        arr.pop(move[0])

    newpos.turn += 1
    return newpos

def CanDoMove(pos, move):
    arr = pos.p1_pieces if pos.turn % 2 == 0 else pos.p2_pieces
    player = pos.turn % 2 + 1
    rot = PIECES[arr[move[0]]].rotations[move[1]]
    r, c = move[2], move[3]

    overlap = False
    adjacent = False
    for s in rot:
        if pos.board[s[0] + r][s[1] + c] != 0:
            overlap = True
            break
        if ADJACENCY:
            if pos.turn == 0:
                adjacent = ((s[0] + r, s[1] + c) == P1_START)
            elif pos.turn == 1:
                adjacent = ((s[0] + r, s[1] + c) == P2_START)
            else:
                for d in [-1, 1]:
                    if 0 <= s[0] + r + d < H:
                        if pos.board[s[0] + r + d][s[1] + c] == player:
                            adjacent = True
                            break
                    if 0 <= s[1] + c + d < W:
                        if pos.board[s[0] + r][s[1] + c + d] == player:
                            adjacent = True
                            break

    return not overlap and (adjacent or not ADJACENCY)

def GenerateMoves(pos):
    moves = []

    arr = pos.p1_pieces if pos.turn % 2 == 0 else pos.p2_pieces
    player = pos.turn % 2 + 1

    for pi in range(len(arr)):
        p = PIECES[arr[pi]]
        for ri in range(len(p.rotations)):
            rot = p.rotations[ri]
            for r in range(H + 1 - p.sizes[ri][0]):
                for c in range(W + 1 - p.sizes[ri][1]):
                    overlap = False
                    adjacent = False
                    for s in rot:
                        if pos.board[s[0] + r][s[1] + c] != 0:
                            overlap = True
                            break
                        if ADJACENCY:
                            if pos.turn == 0:
                                adjacent = ((s[0] + r, s[1] + c) == P1_START)
                            elif pos.turn == 1:
                                adjacent = ((s[0] + r, s[1] + c) == P2_START)
                            else:
                                for d in [-1, 1]:
                                    if 0 <= s[0] + r + d < H:
                                        if pos.board[s[0] + r + d][s[1] + c] == player:
                                            adjacent = True
                                            break
                                    if 0 <= s[1] + c + d < W:
                                        if pos.board[s[0] + r][s[1] + c + d] == player:
                                            adjacent = True
                                            break

                    if not overlap and (adjacent or not ADJACENCY):
                        moves.append([pi, ri, r, c])

    return moves

def PrimitiveValue(pos):
    if not GenerateMoves(pos):
        return "lose"
    return "not_primitive"
