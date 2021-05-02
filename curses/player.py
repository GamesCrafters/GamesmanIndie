import curses
import argparse
from os import path
from sys import exit

import uwapi
import ui_default as ui

parser = argparse.ArgumentParser()
parser.add_argument('game')
parser.add_argument('-v', '-variant', dest='variant', default='regular')
args = vars(parser.parse_args())

game = args['game']
variant = args['variant']
if path.exists(f'ui_{game}.py'):
    exec(f'import ui_{game} as ui')

w = curses.initscr()
curses.start_color()
w.keypad(True)
curses.mousemask(1)

w_height, w_width = w.getmaxyx()

def draw_position(pos_str, offset=(0,0)):
    """Draws a given position string `pos_str` with offset `offset`."""
    lines = pos_str.split('\n')
    for i in range(len(lines)):
        w.addstr(offset[0] + i, offset[1], lines[i])

coord_move = {}
moves = {}
def draw_move(move, move_str, offset=(0,0)):
    """Draws a given move string `move_str` with offset `offset`, then adds `move` to the `coord_move` dictionary
    for each coordinate drawn."""
    lines = move_str.split('\n')
    for i in range(len(lines)):
        w.addstr(offset[0] + i, offset[1], lines[i])
        for j in range(len(lines[i])):
            coord_move[(offset[0] + i, offset[1] + j)] = move

# get starting position
pos = uwapi.get_start_position(game, variant)

# game loop
ch = None
while ch != ord('q'):
    # click input
    if ch == curses.KEY_MOUSE:
        _, mx, my, _, _ = curses.getmouse()

        # check if any move string is clicked
        if (my, mx) in coord_move:
            move = coord_move[(my, mx)]
            pos = moves[move]['position']
        else:
            ch = w.getch()
            continue

    w.erase()

    # get and draw position string
    draw_position(*ui.position_string(pos))

    # get list of possible next moves from UWAPI
    response = uwapi.get_position(game, variant, pos)
    moves = response['response']['moves']
    moves = {move['move']: move for move in moves}

    # get and draw move strings
    coord_move = {}
    index = 0
    for move in moves:
        draw_move(move, *ui.move_string(move, pos, index))
        index += 1

    w.addstr(0, w_width - 7, '[Q]uit')

    w.move(w_height - 1, 0)

    w.refresh()

    ch = w.getch()
