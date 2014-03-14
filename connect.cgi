#!/usr/bin/env python

# Written by Kyle Zentner. Feb 28, 2014

from __future__ import print_function

import cgi
import json
import math
import os
import os.path
import re
import sys
import traceback


def main():
    env = cgi.parse()
    try:
        width = int(env['width'][0])
        height = int(env['height'][0])
        win = int(env['win'][0])
        board = env['board'][0]
        user = env['user'][0]
    except KeyError as e:
        return_error('Missing parameter {0}'.format(e))
        return
    # Remove ""
    board = board[1:-1]
    if check_board(board, width, height) and check_user(user):
        res = response(user, board, width, height, win)
        return_response(res)


def response(user, board, width, height, win):
    succ = successors(board, width, height)
    filename = db_name(user, width, height, win)
    values = []
    hashes = []
    with open(filename) as f:
        for s in succ:
            hsh = hash_brd(s, width, height)
            hashes.append(hsh)
            values.append(get_value(f, hsh, s, width, height))
    res = []
    for s, v, h in zip(succ, values, hashes):
        res.append({'board': s, 'value': v, 'hash': h})
    return res


def db_name(user, width, height, win):
    path = ('~{0}/public_html/' +
            '{2}x{3}_connect{1}.txt').format(user, win, width, height)
    return os.path.expanduser(path)


def successors(brd, width, height):
    columns = get_columns(brd, width, height)
    #assert len(brd) == width * height
    #assert len(''.join(columns)) == len(brd)
    to_move = turn(brd)
    out = []
    for i, col in enumerate(columns):
        if ' ' not in col:
            continue
        new_col = move_column(to_move, col)
        new_brd = ''.join(columns[:i] + [new_col] + columns[i+1:])
        #assert len(new_brd) == len(brd)
        out.append(new_brd)
    return out


def turn(brd):
    # Default to 'o''s turn ('o' goes first).
    if brd.count('o') > brd.count('x'):
        return 'x'
    else:
        return 'o'


def hash_brd(brd, width, height):
    columns = get_columns(brd, width, height)
    bits_per_column = height + 1
    out = 0
    for i, col in enumerate(columns):
        out |= to_bits(col) << (i * bits_per_column)
    return out


def to_bits(column):
    column = column.strip()
    out = 0
    out |= 0x1 << len(column)
    for i, c in enumerate(column):
        if c == 'x':
            out |= 0x1 << len(column) - i - 1
    #print('"{0:>4}" => {1:>5}'.format(column, bin(out)[2:]))
    return out


def return_error(msg):
    json.dump({'status': 'error', 'reason': msg}, sys.stdout, indent=2)


def return_response(msg):
    json.dump({'status': 'ok', 'response': msg}, sys.stdout, indent=2)


def get_columns(brd, width, height):
    return [brd[i:i+height] for i in range(0, width * height, height)]


def move_column(turn, column):
    last_space = index_of_last(column, ' ')
    out = column[:last_space] + turn + column[last_space+1:]
    #assert len(out) == len(column)
    return out


def index_of_last(string, char):
    out = len(string) - string[::-1].find(char) - 1
    #assert string[out] == char
    #assert string[out + 1:].find(char) == -1
    return out

NAIVE_STORE = True


def get_value(fd, hsh, brd, width, height):
    if NAIVE_STORE:
        # Reverse board
        brd = brd[::-1]
        # Swap players and capitalize
        brd = brd.replace('o', 'X')
        brd = brd.replace('x', 'O')
        fd.seek(0, os.SEEK_SET)
        lines = fd.xreadlines()
        for line in lines:
            if brd in line:
                num = int(line.split()[-1])
                return get_value_from_naive_num(brd, num)
        return 'U'
    else:
        fd.seek(2 * hsh)
        return fd.read(1)


def get_value_from_naive_num(brd, num):
    vals = {
        0: 'U',
        1: 'W' if turn(brd) == 'o' else 'L',
        2: 'W' if turn(brd) == 'x' else 'L',
        3: 'T'
        }
    return vals[num & 0b11]


def check_board(brd, width, height):
    match = re.match('[ xo]{%d}' % width * height, brd)
    if not match or match.string != brd or len(brd) != width * height:
        return_error('board format incorrect.')
        return False
    return True


def check_user(user):
    match = re.match('[eecs]{2}[0-9]{1,3}[-][A-z]{2,}|[A-z]*', user)
    if not match or match.string != user:
        return_error('user format incorrect.')
        return False
    return True


def get_rows(brd, width, height):
    return [brd[i::width] for i in range(0, height)]


def get_p_diags(brd, width, height):
    return [brd[i::width + 1] for i in range(0, height)]


def get_n_diags(brd, width, height):
    return [brd[i::width - 1] for i in range(0, height)]


def get_diagonals(brd, width, height):
    return get_p_diags(brd, width, height) + get_n_diags(brd, width, height)


db = {}


def db_set(brd, width, height, res):
    hsh = hash_brd(brd, width, height)
    db[hsh] = res
    return res


def db_get(brd, width, height):
    hsh = hash_brd(brd, width, height)
    try:
        return db[hsh]
    except KeyError:
        return None


def solve(brd, width, height, win):
    res = db_get(brd, width, height)
    if res is not None:
        return res
    cols = get_columns(brd, width, height)
    winx = 'x' * win
    wino = 'o' * win
    for c in cols:
        if winx in c:
            return db_set(brd, width, height, 'x')
        elif wino in c:
            return db_set(brd, width, height, 'o')
    rows = get_rows(brd, width, height)
    for r in rows:
        if winx in r:
            return db_set(brd, width, height, 'x')
        elif wino in r:
            return db_set(brd, width, height, 'o')
    diags = get_diagonals(brd, width, height)
    for d in diags:
        if winx in d:
            return db_set(brd, width, height, 'x')
        elif wino in d:
            return db_set(brd, width, height, 'o')

    children = []
    for s in successors(brd, width, height):
        children.append(solve(s, width, height, win))

    if turn(brd) == 'o':
        if 'o' in children:
            return db_set(brd, width, height, 'o')
        elif None in children:
            return None
        else:
            return db_set(brd, width, height, 'x')
    if turn(brd) == 'x':
        if 'x' in children:
            return db_set(brd, width, height, 'x')
        elif None in children:
            return None
        else:
            return db_set(brd, width, height, 'o')


def to_line(v):
    if v == 'o':
        return 'W\n'
    elif v == 'x':
        return 'L\n'
    else:
        return 'T\n'


# --- => 0
# --o => 1
# --x => 2
# -oo => 3
# -ox => 4
# -xo => 5
# -xx => 6
# ooo => 7
# oox => 8
# oxo => 9
# oxx => 10
# xoo => 11
# xox => 12
# xxo => 13
# xxx => 14


# --- => 01 => 0001
# --o => 02 => 0010
# --x => 03 => 0011
# -oo => 04 => 0100
# -ox => 05 => 0101
# -xo => 06 => 0110
# -xx => 07 => 0111
# ooo => 08 => 1000
# oox => 09 => 1001
# oxo => 10 => 1010
# oxx => 11 => 1011
# xoo => 12 => 1100
# xox => 13 => 1101
# xxo => 14 => 1110
# xxx => 15 => 1111


def save_db(filename):
    with open(filename, 'w') as f:
        i = 0
        #while i not in db:
        for k, v in sorted(db.iteritems()):
            while i != k:
                f.write(to_line(None))
                i += 1
            f.write(to_line(v))
        #for v in db:
            #f.write(to_line(v))


def solve_game(width, height, win):
    solve(' ' * width * height, width, height, win)
    save_db('{1}x{2}_connect{0}.txt'.format(win, width, height))


#solve_game(4, 5, 4)
#solve_game(3, 3, 3)

#to_bits('    ')
#to_bits('   o')
#to_bits('   x')
#to_bits('  oo')
#to_bits('  ox')
#to_bits('  xx')
#to_bits(' ooo')
#to_bits(' oox')
#to_bits(' oxo')
#to_bits(' oxx')
#to_bits(' xoo')
#to_bits(' xox')
#to_bits(' xxo')
#to_bits(' xxx')
#to_bits('oooo')
#to_bits('ooox')
#to_bits('ooxo')
#to_bits('ooxx')
#to_bits('oxoo')
#to_bits('oxox')
#to_bits('oxxx')
#to_bits('xooo')
#to_bits('xoox')
#to_bits('xoxo')
#to_bits('xoxx')
#to_bits('xxoo')
#to_bits('xxox')
#to_bits('xxxo')
#to_bits('xxxx')

print()
try:
    main()
except Exception as e:
    return_error('Exception: {0}, {1}'.format(e, traceback.format_exc()))
