function Board(x, y) {
    this._board = [];
    this._width = x;
    this._height = y;
    this._valid_moves = [];
    for(var i = 0; i < this._width; i++) {
	this._board.push([]);
	this._valid_moves.push(i);
    }
    this._connections = {
	R: { h: {}, v: {}, d1: {}, d2: {} },
	B: { h: {}, v: {}, d1: {}, d2: {} }
    };
    this._win = { R: false, B: false };
    var pos;
    for(var i = 0; i < this._width; i++) {
	for(var j = 0; j < this._height; j++) {
	    pos = [i, j];
	    this._connections.R.h[pos] = 0;
	    this._connections.R.v[pos] = 0;
	    this._connections.R.d1[pos] = 0;
	    this._connections.R.d2[pos] = 0;
	    this._connections.B.h[pos] = 0;
	    this._connections.B.v[pos] = 0;
	    this._connections.B.d1[pos] = 0;
	    this._connections.B.d2[pos] = 0;
	}
    }
    this._move_history = [];
    this._getOtherColor = function(color) {
	return color === "R" ? "B" : "R";
    };

    var next_fns = {
	n:  function(pos, i) { return [pos[0], pos[1]+i]; },
	s:  function(pos, i) { return [pos[0], pos[1]-i]; },
	e:  function(pos, i) { return [pos[0]+i, pos[1]]; },
	w:  function(pos, i) { return [pos[0]-i, pos[1]]; },
	ne: function(pos, i) { return [pos[0]+i, pos[1]+i]; },
	se: function(pos, i) { return [pos[0]+i, pos[1]-i]; },
	sw: function(pos, i) { return [pos[0]-i, pos[1]-i]; },
	nw: function(pos, i) { return [pos[0]-i, pos[1]+i]; }
    }
    var orientations = {
	n:  "v",
	s:  "v",
	e:  "h",
	w:  "h",
	ne: "d1",
	sw: "d1",
	nw: "d2",
	se: "d2"
    }
    var directions = ["n", "s", "e", "w", "ne", "sw", "nw", "se"];
    this._addConnections = function(pos, color) {
	var connections = this._connections[color];
	var x = pos[0], y = pos[1], i;
	var cur_pos;
	var positions_to_set;
	var o = "";
	var value, d;
	connections.h[pos] = 1;
	connections.v[pos] = 1;
	connections.d1[pos] = 1;
	connections.d2[pos] = 1;
	for(var j = 0; j < directions.length; j++) {
	    d = directions[j];
	    for(i = 1; i <= 3; i++) {
		cur_pos = next_fns[d](pos, i);
		if(o != orientations[d]) { 
		    positions_to_set = [pos]; 
		    value = 1;
		}
		o = orientations[d];
		if(this._isValidPos(cur_pos) && connections[o][cur_pos] != 0) {
		    value++;
		    positions_to_set.push(cur_pos);
		} else {
		    break;
		}
	    }
	    if(value >= 4) { this._win[color] = true; }
	    for(var k = 0; k < positions_to_set.length; k++) {
		connections[o][positions_to_set[k]] = value;
	    }
	}
    };
    this._removeConnections = function(pos, color) {
	var connections = this._connections[color];
	var x = pos[0], y = pos[1], i;
	var value_remove;
	var value;
	var positions_to_set;
	var o, i, cur_pos, d;
	this._win[color] = false;
	for(var j = 0; j < directions.length; j++) {
	    value = 0;
	    d = directions[j];
	    o = orientations[d];
	    value_remove = connections[o][pos];
	    positions_to_set = [];
	    for(i = 1; i <= 3; i++) {
		cur_pos = next_fns[d](pos, i);
		if(this._isValidPos(cur_pos) && connections[o][cur_pos] === value_remove) {
		    value++;
		    positions_to_set.push(cur_pos);
		} else {
		    break;
		}
	    }
	    if(value >= 4) { this._win[color] = true; }
	    for(var k = 0; k < positions_to_set.length; k++) {
		connections[o][positions_to_set[k]] = value;
	    }
	} 
	connections.h[pos] = 0;
	connections.v[pos] = 0;
	connections.d1[pos] = 0;
	connections.d2[pos] = 0;
    };
    this._isValidPos = function(pos) {
	var x = pos[0], y = pos[1];
	return x >= 0 && x < this._width &&
	       y >= 0 && y < this._height &&
	       this._board[x][y] != undefined;
    };
}

Board.prototype.currentColor = function() {
    return this._current_color;
}

Board.prototype.makeMove = function(column, color) {
    var pos = [column, this._board[column].length];
    this._board[column].push(color);
    if(this._board[column].length === this._height) {
	this._valid_moves.splice(column, 1);
    }
    this._move_history.push({color: color, column: column});
    this._addConnections(pos, color);
};
Board.prototype.undoLastMove = function() {
    var last_move = this._move_history.pop();
    var col = this._board[last_move.column];
    var pos = [last_move.column, col.length-1];
    if(col.length == this._height) {
	this._valid_moves.push(last_move.column);
	this._valid_moves.sort();
    }
    this._removeConnections(pos, last_move.color);
    col.pop();
};

Board.prototype.evaluate = function(color) {};

Board.prototype.isWin = function(color) {
    return this._win[color];
};
Board.prototype.isLoss = function(color) {
    return this.isWin(this._getOtherColor(color));
};
Board.prototype.isTie = function(color) {
    return !this.isWin(color) && !this.isLoss(color) &&
           this._valid_moves.length == 0;
};
Board.prototype.isDraw = Board.prototype.isTie;
Board.prototype.validMoves = function() {
    return this._valid_moves;
};
Board.prototype.toString = function() {
    var str = "_";
    var board = this._board;
    for(var i = 0; i < this._width-1; i++) {
	str += " _";
    }
    str += " \n";
    for(var j = this._height-1; j >= 0; j--) {
	for(var i = 0; i < this._width; i++) {
	    if (board[i][j] === "R") {
		str += "|R";
	    } else if(board[i][j] === "B") {
		str += "|B";
	    } else {
		str += "|_";
	    }
	}
	str += "|\n";
    }
    return str;
};

/***********************************UNIT TESTS*********************************/

function runBoardTests() {
    var passed = 0;
    var results = loadAndRunTests();
    for(var i = 0; i < results.length; i++) {
	if(results[i].answer != results[i].expected) {
	    console.log(results[i].name + " failed.");
	    console.log("Expected: " + results[i].expected);
	    console.log("Got: " + results[i].answer);
	    console.log("Board:\n " + results[i].board_str);
	} else {
	    console.log(results[i].name + " passed.");
	    passed++;
	}
    }
    console.log(passed + "/" + results.length + " passed.");
}

function loadAndRunTests() {
    var data = loadTestData();
    var results = [];
    var result;
    for(var i = 0; i < data.names.length; i++) {
	result = {
	    name: data.names[i],
	    expected: data.expected[i],
	    board_str: data.board_strs[i]
	};
	result.answer = data.funcs[i].apply(data.objs[i], data.args[i]);
	results.push(result);
    }
    return results;
}

function loadTestData() {
    var board_data = loadBoards();
    var board_eq = function(s1, s2) {
	return s1 === s2;
    }
    var test_data = {
	names: [
	    "rvwin_init",
	    "rhwin_init",
	    "rd1win_init",
	    "rvwin",
	    "rhwin",
	    "rd1win"
	],
	expected: [
	    true,
	    true,
	    true,
	    true,
	    true,
	    true
	],
	funcs: [
	    board_eq,
	    board_eq,
	    board_eq,
	    board_data[0].board.isWin,
	    board_data[1].board.isWin,
	    board_data[2].board.isWin
	],
	args: [
	    [board_data[0].board.toString(), board_data[0].str],
	    [board_data[1].board.toString(), board_data[1].str],
	    [board_data[2].board.toString(), board_data[2].str],
	    ["R"],
	    ["R"],
	    ["R"]
	],
	objs: [
	    null,
	    null,
	    null,
	    board_data[0].board,
	    board_data[1].board,
	    board_data[2].board
	],
	board_strs: []
    };
    for(var i = 0; i < board_data.length; i++) {
	test_data.board_strs.push(board_data[i].board.toString());
    }
    return test_data;
}

function loadBoards() {
    var board_data = [];

    var rvwin4 = new Board(6, 6);
    var rhwin4 = new Board(6, 6);
    var rd1win4 = new Board(6, 6);

    rvwin4.makeMove(1, "R");
    rvwin4.makeMove(2, "B");
    rvwin4.makeMove(3, "R");
    rvwin4.makeMove(2, "B");
    rvwin4.makeMove(3, "R");
    rvwin4.makeMove(4, "B");
    rvwin4.makeMove(3, "R");
    rvwin4.makeMove(4, "B");
    rvwin4.makeMove(3, "R");
    var rvwin4_data = {
	board: rvwin4,
	str: "_ _ _ _ _ _ \n|_|_|_|_|_|_|\n|_|_|_|_|_|_|\n|_|_|_|R|_|_|\n|_|_|_|R|_|_|\n|_|_|B|R|B|_|\n|_|R|B|R|B|_|\n"
    };
    board_data.push(rvwin4_data);

    rhwin4.makeMove(1, "R");
    rhwin4.makeMove(2, "B");
    rhwin4.makeMove(2, "R");
    rhwin4.makeMove(4, "B");
    rhwin4.makeMove(3, "R");
    rhwin4.makeMove(5, "B");
    rhwin4.makeMove(3, "R");
    rhwin4.makeMove(0, "B");
    rhwin4.makeMove(4, "R");
    rhwin4.makeMove(0, "B");
    rhwin4.makeMove(5, "R");
    var rhwin4_data = {
	board: rhwin4,
	str: "_ _ _ _ _ _ \n|_|_|_|_|_|_|\n|_|_|_|_|_|_|\n|_|_|_|_|_|_|\n|_|_|_|_|_|_|\n|B|_|R|R|R|R|\n|B|R|B|R|B|B|\n"
    };
    board_data.push(rhwin4_data);

    rd1win4.makeMove(1, "R");
    rd1win4.makeMove(2, "B");
    rd1win4.makeMove(4, "R");
    rd1win4.makeMove(3, "B");
    rd1win4.makeMove(5, "R");
    rd1win4.makeMove(3, "B");
    rd1win4.makeMove(2, "R");
    rd1win4.makeMove(4, "B");
    rd1win4.makeMove(3, "R");
    rd1win4.makeMove(4, "B");
    rd1win4.makeMove(4, "R");
    var rd1win4_data = {
	board: rd1win4,
	str: "_ _ _ _ _ _ \n|_|_|_|_|_|_|\n|_|_|_|_|_|_|\n|_|_|_|_|R|_|\n|_|_|_|R|B|_|\n|_|_|R|B|B|_|\n|_|R|B|B|R|R|\n"
    };
    board_data.push(rd1win4_data);
     
    board_data.push(rvwin4_data);
    board_data.push(rhwin4_data);
    board_data.push(rd1win4_data);

    return board_data;
}

/** rvwin4
 *          _ _ _ _ _ _ 
 *         |_|_|_|_|_|_|
 *         |_|_|_|_|_|_|
 *         |_|_|_|R|_|_|
 *         |_|_|_|R|_|_|
 *         |_|_|B|R|B|_|
 *         |_|R|B|R|B|_|
 */
/** rhwin4 
 *          _ _ _ _ _ _
 *         |_|_|_|_|_|_|
 *         |_|_|_|_|_|_|
 *         |_|_|_|_|_|_|
 *         |_|_|_|_|_|_|
 *         |B|_|R|R|R|R|
 *         |B|R|B|R|B|B|
 */
/** rd1win4 
 *          _ _ _ _ _ _
 *         |_|_|_|_|_|_|
 *         |_|_|_|_|_|_|
 *         |_|_|_|_|R|_|
 *         |_|_|_|R|B|_|
 *         |_|_|R|B|B|_|
 *         |_|R|B|B|R|R|
 */
