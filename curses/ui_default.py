offset = (0, 0)

def position_string(pos):
    args = pos.split('_')
    type = args[0]

    if type == 'R':
        _, player, rows, cols, board = args[:5]
        rows, cols = int(rows), int(cols)
        board = board.replace('-', ' ')

        board_str = '┌' + '───┬' * (cols - 1) + '───┐\n'
        for r in range(rows):
            board_str += '│'
            for c in range(cols):
                board_str += ' ' + board[r * cols + c] + ' ' + '│'
            if r < rows - 1:
                board_str += '\n├' + '───┼' * (cols - 1) + '───┤\n'
            else:
                board_str += '\n└' + '───┴' * (cols - 1) + '───┘\n'

        return board_str, offset
    else:
        return pos, offset

def comp(a, b):
    return 0 if a < b else 2 if a > b else 1

def move_string(move, pos, index=None):
    move_args = move.split('_')
    type = move_args[0]

    if type == 'A':
        pos_args = pos.split('_')
        rows, cols = int(pos_args[2]), int(pos_args[3])

        piece, index = move_args[1], int(move_args[2])
        row, col = index // cols, index % cols
        return ' . ', (1 + row * 2 + offset[0], 1 + col * 4 + offset[1])

    if type == 'M':
        pos_args = pos.split('_')
        rows, cols = int(pos_args[2]), int(pos_args[3])

        start, end = int(move_args[1]), int(move_args[2])
        srow, scol = start // cols, start % cols
        erow, ecol = end // cols, end % cols

        out_offset = (1 + srow * 2 + [-1, 0, 1][comp(erow, srow)] + offset[0],
                      2 + scol * 4 + [-2, 0, 2][comp(ecol, scol)] + offset[1])

        return [['↖', '↑', '↗'], ['←', '', '→'], ['↙', '↓', '↘']][comp(erow, srow)][comp(ecol, scol)], out_offset

    return move, (offset[0] + 2 + index, 0)
