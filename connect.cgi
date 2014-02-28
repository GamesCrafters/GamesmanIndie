#!/usr/bin/env python

# Written by Kyle Zentner. Feb 28, 2014

from __future__ import print_function

import sys
import cgi
import json
import re
import os.path
import math


def main():
    env = cgi.parse()
    try:
        width = int(env['width'][0])
        height = int(env['height'][0])
        board = env['board'][0]
        user = env['user'][0]
    except KeyError as e:
        return_error('Missing parameter {0}'.format(e))
        return
    # Remove ""
    board = board[1:-1]
    if check_board(board, width, height) and check_user(user):
        res = response(user, board, width, height)
        return_response(res)


def response(user, board, width, height):
    succ = successors(board, width, height)
    filename = db_name(user, width, height)
    values = []
    hashes = []
    with open(filename) as f:
        for s in succ:
            hsh = hash_brd(s, width, height)
            hashes.append(hsh)
            values.append(get_value(f, hsh))
    res = []
    for s, v, h in zip(succ, values, hashes):
        res.append({'board': s, 'value': v, 'hash': h})
    return res


def db_name(user, width, height):
    path = '~{0}/public_html/connect{1}x{2}.txt'.format(user, width, height)
    return os.path.expanduser(path)


def successors(brd, width, height):
    columns = get_columns(brd, width, height)
    to_move = turn(brd)
    out = []
    for i, col in enumerate(columns):
        if ' ' not in col:
            continue
        new_col = move_column(to_move, col)
        new_brd = ''.join(columns[:i] + [new_col] + columns[i+1:])
        assert len(new_brd) == len(brd)
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
    len_bits = int(math.ceil(math.log(height, 2)))
    out = 0
    for i, col in enumerate(columns):
        length = len(col.strip())
        out |= length
        out |= (to_bits(col) << len_bits)
        out = out << (length + len_bits)
    return out


def to_bits(column):
    out = 0
    for i, c in enumerate(column):
        if c == 'x':
            out |= 0x1 << len(column) - i - 1
    return out


def return_error(msg):
    json.dump({'status': 'error', 'reason': msg}, sys.stdout, indent=2)


def return_response(msg):
    json.dump({'status': 'ok', 'response': msg}, sys.stdout, indent=2)


def get_columns(brd, width, height):
    return [brd[i:i+height] for i in range(0, width * height, width)]


def move_column(turn, column):
    last_space = index_of_last(column, ' ')
    out = column[:last_space] + turn + column[last_space+1:]
    assert len(out) == len(column)
    return out


def index_of_last(string, char):
    out = len(string) - string[::-1].find(char) - 1
    assert string[out] == char
    assert string[out + 1:].find(char) == -1
    return out


def get_value(fd, hsh):
    fd.seek(2 * hsh)
    return fd.read(1)


def check_board(brd, width, height):
    match = re.match('[ xo]{%d}' % width * height, brd)
    if not match or match.string != brd:
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

db = []

def store(brd, width, height, res):
    hsh = hash_brd(brd, width, height)
    if len(db) < hsh:
        db.extend([None] * (1 + hsh - len(db)))
    db[hsh] = res
    return res

def solve(brd, width, height):
    cols = get_columns(brd, width, height)
    for c in cols:
        if 'xxx' in c:
            return store(brd, width, height, 'x')
        elif 'ooo' in c:
            return store(brd, width, height, 'o')
    rows = get_rows(brd, width, height)
    for r in rows:
        if 'xxx' in r:
            return store(brd, width, height, 'x')
        elif 'ooo' in r:
            return store(brd, width, height, 'o')
    diags = get_diagonals(brd, width, height)
    for d in diags:
        if 'xxx' in d:
            return store(brd, width, height, 'x')
        elif 'ooo' in d:
            return store(brd, width, height, 'o')
    
    children = []
    for s in successors(brd, width, height):
        children.append(solve(s, width, height))

    if turn(brd) == 'o' and 'o' in children:
        return store(brd, width, height, 'o')
    elif turn(brd) == 'x' and 'x' in children:
        return store(brd, width, height, 'x')

def to_line(v):
    if v == 'o':
        return 'W\n'
    elif v == 'x':
        return 'L\n'
    else:
        return 'T\n'

def save_db(filename):
    with open(filename, 'w') as f:
        for v in db:
            f.write(to_line(v))

print()
try:
    #solve(' ' * 16, 4, 4)
    #save_db('connect4x4.txt')
    main()
except Exception as e:
    return_error('Exception: {0}'.format(e))
