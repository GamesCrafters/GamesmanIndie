from game_blockis import *
from solver import *

from curses import *
import random
import sys

cpu = '--cpu' in sys.argv
solve = '--solve' in sys.argv

w = initscr()
start_color()
w.keypad(True)

# initialize colors
init_pair(1, COLOR_RED, COLOR_RED)
init_pair(2, COLOR_BLUE, COLOR_BLUE)
init_color(15, 500, 0, 0)
init_pair(3, 15, 15)
init_pair(4, COLOR_MAGENTA, COLOR_MAGENTA)
init_color(16, 0, 0, 500)
init_pair(5, 16, 16)

w_height, w_width = w.getmaxyx()

CHAR_BLANK = '. '
CHAR_PIECE = '##'
def draw_position(pos):
    """Draws a given position."""
    w.addstr(1, 2, '╔' + '══'*W + '╗')
    for r in range(H):
        w.addch(r+2, 2, '║')
        for c in range(W):
            ch = CHAR_BLANK if pos.board[r][c] == 0 else CHAR_PIECE
            w.addstr(r+2, c*2+3, ch, color_pair(pos.board[r][c]))
        w.addch(r+2, W*2+3, '║')
    w.addstr(H+2, 2, '╚' + '══'*W + '╝')

def draw_piece(piece, r, c, color, ch='##'):
    """Draws a given piece."""
    for s in piece.rotations[0]:
        w.addstr(r + s[0], c + s[1]*2, ch, color_pair(color))

def draw_pieces(pos, turn=None, index=None):
    """Draws the set of pieces available for each player."""

    # p1 pieces
    r = H + 4
    c = 2
    selection = '  '
    for p in pos.p1_pieces:
        piece = PIECES[p]
        draw_piece(piece, r, c, 1, '11')
        piece_width = piece.sizes[0][1]
        if turn == 1 and pos.p1_pieces[index] == p:
            w.addstr(r + MAX_P1_HEIGHT, c, '^^'*piece_width)
        c += (piece_width + 1) * 2
    w.addstr(r + MAX_P1_HEIGHT, 0, selection)

    # p2 pieces
    r += MAX_P1_HEIGHT + 1
    c = 2
    dr = max(PIECES[p].sizes[0][0] for p in pos.p2_pieces)
    selection = '  '
    for p in pos.p2_pieces:
        piece = PIECES[p]
        draw_piece(piece, r, c, 2, '22')
        piece_width = piece.sizes[0][1]
        if turn == 2 and pos.p2_pieces[index] == p:
            w.addstr(r + MAX_P2_HEIGHT, c, '^^'*piece_width)
        c += (piece_width + 1) * 2
    w.addstr(r + MAX_P2_HEIGHT, 0, selection)

# dictionary used to determine overlap color
colors = {
    1: {
        0: 1,
        1: 3,
        2: 4
    },
    2: {
        0: 2,
        1: 4,
        2: 5
    }
}
def draw_place(pos, piece, turn, r, c, rotate, ch='##'):
    """Draw a piece that is currently being placed."""
    for s in piece.rotations[rotate]:
        w.addstr(2 + r + s[0], 3 + c*2 + s[1]*2, ch, color_pair(colors[turn][pos.board[r+s[0]][c+s[1]]]))

pos = Position()
MAX_P1_HEIGHT = max(PIECES[p].sizes[0][0] for p in pos.p1_pieces)
MAX_P2_HEIGHT = max(PIECES[p].sizes[0][0] for p in pos.p2_pieces)

mode = 'selecting'
select_piece = 0
place_r = place_c = place_rotate = 0

ch = None
while ch != ord('q'):
    w.erase()

    #w.addstr(15, 0, str(ch) + ' '*4) # debugging

    turn = pos.turn % 2 + 1
    pieces = pos.p1_pieces if turn == 1 else pos.p2_pieces

    # automate move if CPU mode
    if cpu and turn == 2 and mode != 'gameover':
        moves = GenerateMoves(pos)
        if solve: # if solve flag is checked, solve current position and pick best move
            Solve(pos)
            outcomes = [Solve(DoMove(pos, m)) for m in moves]
            best_move = max(moves, key=lambda m: {'win':0,'tie':1,'lose':2}[Solve(DoMove(pos, m))[0]])
            pos = DoMove(pos, best_move)
        else: # otherwise, pick random move
            random_move = moves[random.randint(0, len(moves)-1)]
            pos = DoMove(pos, random_move)

        if PrimitiveValue(pos) != 'not_primitive':
            mode = 'gameover'
    else:
        if mode == 'selecting': # selecting a piece to place
            if ch == KEY_LEFT:
                select_piece = max(0, select_piece - 1)
            elif ch == KEY_RIGHT:
                select_piece = min(len(pieces) - 1, select_piece + 1)
            elif ch == ord(' '):
                mode = 'placing'
                place_r = place_c = place_rotate = 0
        elif mode == 'placing': # selecting where to place the piece
            size = PIECES[pieces[select_piece]].sizes[place_rotate]
            if ch == KEY_LEFT:
                place_c = max(0, place_c - 1)
            elif ch == KEY_RIGHT:
                place_c = min(W - size[1], place_c + 1)
            elif ch == KEY_UP:
                place_r = max(0, place_r - 1)
            elif ch == KEY_DOWN:
                place_r = min(H - size[0], place_r + 1)
            elif ch == ord('r'): # rotate
                place_rotate = (place_rotate + 1) % len(PIECES[pieces[select_piece]].rotations)
                place_r = place_c = 0
            elif ch == ord(' '): # place
                move = (select_piece, place_rotate, place_r, place_c)
                if CanDoMove(pos, move):
                    pos = DoMove(pos, move)
                    select_piece = 0
                    place_r = place_c = place_rotate = 0
                    mode = 'selecting'
                if PrimitiveValue(pos) != 'not_primitive':
                    mode = 'gameover'
            elif ch == 27: #esc
                mode = 'selecting'
        elif mode == 'gameover': # game is over
            if ch == 27: #esc
                pos = Position()
                select_piece = 0
                place_r = place_c = place_rotate = 0
                mode = 'selecting'

    draw_position(pos)

    turn = pos.turn % 2 + 1
    draw_pieces(pos, turn, select_piece)

    if mode == 'placing':
        draw_place(pos, PIECES[pieces[select_piece]], turn, place_r, place_c, place_rotate)

    if mode == 'gameover':
        w.addstr(2, W*2+5, f'P{turn%2+1} WINS!')
    else:
        w.addstr(2, W*2+5, f'P{turn}\'s turn')

    instructions = {
        'selecting': 'Press LEFT and RIGHT to change piece, SPACE to select',
        'placing': 'Press arrow keys to move piece, R to rotate piece, SPACE to place, ESC to go back',
        'gameover': 'Press ESC to restart'
    }
    w.addstr(w_height - 2, 0, instructions[mode])

    w.addstr(0, w_width-7, '[Q]uit')

    # move cursor
    w.move(w_height - 1, 0)

    w.refresh()
    if turn == 1 or mode == 'gameover' or not cpu: ch = w.getch()