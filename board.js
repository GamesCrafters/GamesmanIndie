//constructor for Board
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

    //helper functions/objects below

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

/**
 * makeMove() will drop a piece of color "color" in column "column". This
 * does not enforce player turn order in any way, and will accept any color
 * or column number, even if invalid.
 */
Board.prototype.makeMove = function(column, color) {
    var pos = [column, this._board[column].length];
    this._board[column].push(color);
    if(this._board[column].length === this._height) {
	this._valid_moves.splice(this._valid_moves.indexOf(column), 1);
    }
    this._move_history.push({color: color, column: column});
    this._addConnections(pos, color);
};

/**
 * undoLastMove() undoes the last move and any changes it makes to the state
 * of _connections.
 */
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

/** IMPROVE ME!!
 * Given a color, evaluate() returns a positive or negative integer depending
 * on how "good" the current board is for that player.
 */
Board.prototype.evaluate = function(color) {};

/**
 * isWin() will return true if there is a connection of length 4 or higher for
 * the given color and false otherwise.
 */
Board.prototype.isWin = function(color) {
    return this._win[color];
};

/**
 * isLoss() will return true if there is a connection of length 4 or higher for
 * the other player and false otherwise.
 */
Board.prototype.isLoss = function(color) {
    return this.isWin(this._getOtherColor(color));
};


/** IMPROVE ME?
 * isTie() will return true if there are no wins present for either player and
 * there are no valid moves left.
 */
Board.prototype.isTie = function(color) {
    return !this.isWin(color) && !this.isLoss(color) &&
           this._valid_moves.length === 0;
};
Board.prototype.isDraw = Board.prototype.isTie;

/**
 * validMoves() returns an array of column numbers that have room for more
 * pieces.
 */
Board.prototype.validMoves = function() {
    return this._valid_moves;
};

/**
 * toString() returns a string representation of this Board for debugging purposes.
 */
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
	    "rd2win4_init",
	    "tie_init",
	    "rhwin7_init",
	    "rd1win6_init",
	    "rd2win5_init",
	    "rvwin",
	    "rhwin",
	    "rd1win4",
	    "rd2win4",
	    "tie",
	    "rhwin7",
	    "rd1win6",
	    "rd2win5"
	],
	expected: [
	    true,
	    true,
	    true,
	    true,
	    true,
	    true,
	    true,
	    true,
	    true,
	    true,
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
	    board_eq,
	    board_eq,
	    board_eq,
	    board_eq,
	    board_eq,
	    board_data[0].board.isWin,
	    board_data[1].board.isWin,
	    board_data[2].board.isWin,
	    board_data[3].board.isWin,
	    board_data[4].board.isTie,
	    board_data[5].board.isWin,
	    board_data[6].board.isWin,
	    board_data[7].board.isWin
	],
	args: [
	    [board_data[0].board.toString(), board_data[0].str],
	    [board_data[1].board.toString(), board_data[1].str],
	    [board_data[2].board.toString(), board_data[2].str],
	    [board_data[3].board.toString(), board_data[3].str],
	    [board_data[4].board.toString(), board_data[4].str],
	    [board_data[5].board.toString(), board_data[5].str],
	    [board_data[6].board.toString(), board_data[6].str],
	    [board_data[7].board.toString(), board_data[7].str],
	    ["R"],
	    ["R"],
	    ["R"],
	    ["R"],
	    ["B"],
	    ["R"],
	    ["R"],
	    ["R"]
	],
	objs: [
	    null,
	    null,
	    null,
	    null,
	    null,
	    null,
	    null,
	    null,
	    board_data[0].board,
	    board_data[1].board,
	    board_data[2].board,
	    board_data[3].board,
	    board_data[4].board,
	    board_data[5].board,
	    board_data[6].board,
	    board_data[7].board
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
    var rd2win4 = new Board(6, 6);
    var tie = new Board(6, 6);
    var rhwin7 = new Board(7, 7);
    var rd1win6 = new Board(6, 6);
    var rd2win5 = new Board(6, 6);

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
     
    rd2win4.makeMove(1, "R");
    rd2win4.makeMove(2, "B");
    rd2win4.makeMove(4, "R");
    rd2win4.makeMove(3, "B");
    rd2win4.makeMove(5, "R");
    rd2win4.makeMove(1, "B");
    rd2win4.makeMove(3, "R");
    rd2win4.makeMove(2, "B");
    rd2win4.makeMove(2, "R");
    rd2win4.makeMove(1, "B");
    rd2win4.makeMove(1, "R");
    var rd2win4_data = {
	board: rd2win4,
	str: "_ _ _ _ _ _ \n|_|_|_|_|_|_|\n|_|_|_|_|_|_|\n|_|R|_|_|_|_|\n|_|B|R|_|_|_|\n|_|B|B|R|_|_|\n|_|R|B|B|R|R|\n"
    };
    board_data.push(rd2win4_data);
    for(var times = 3; times > 0; times--) {
	for(var i = 0; i <= 4; i+=2) {
	    tie.makeMove(i+1, "R");
	    tie.makeMove(i, "B");
	}
    }
    for(var times = 3; times > 0; times--) {
	for(var i = 0; i <= 4; i+=2) {
	    tie.makeMove(i, "R");
	    tie.makeMove(i+1, "B");
	}
    }
    var tie_data = {
	board: tie,
	str: "_ _ _ _ _ _ \n|R|B|R|B|R|B|\n|R|B|R|B|R|B|\n|R|B|R|B|R|B|\n|B|R|B|R|B|R|\n|B|R|B|R|B|R|\n|B|R|B|R|B|R|\n"
    };
    board_data.push(tie_data);

    rhwin7.makeMove(0, "R");
    rhwin7.makeMove(0, "B");
    rhwin7.makeMove(1, "R");
    rhwin7.makeMove(1, "B");
    rhwin7.makeMove(2, "R");
    rhwin7.makeMove(2, "B");
    rhwin7.makeMove(4, "R");
    rhwin7.makeMove(4, "B");
    rhwin7.makeMove(5, "R");
    rhwin7.makeMove(5, "B");
    rhwin7.makeMove(6, "R");
    rhwin7.makeMove(6, "B");
    rhwin7.makeMove(3, "R");
    var rhwin7_data = {
	board: rhwin7,
	str: "_ _ _ _ _ _ _ \n|_|_|_|_|_|_|_|\n|_|_|_|_|_|_|_|\n|_|_|_|_|_|_|_|\n|_|_|_|_|_|_|_|\n|_|_|_|_|_|_|_|\n|B|B|B|_|B|B|B|\n|R|R|R|R|R|R|R|\n"
    };
    board_data.push(rhwin7_data);

    rd1win6.makeMove(5, "R");
    rd1win6.makeMove(4, "B");
    rd1win6.makeMove(3, "R");
    rd1win6.makeMove(2, "B");
    rd1win6.makeMove(1, "R");
    rd1win6.makeMove(2, "B");
    rd1win6.makeMove(1, "R");
    rd1win6.makeMove(3, "B");
    rd1win6.makeMove(0, "R");
    rd1win6.makeMove(4, "B");
    rd1win6.makeMove(5, "R");
    rd1win6.makeMove(5, "B");
    rd1win6.makeMove(2, "R");
    rd1win6.makeMove(3, "B");
    rd1win6.makeMove(4, "R");
    rd1win6.makeMove(4, "B");
    rd1win6.makeMove(5, "R");
    rd1win6.makeMove(0, "B");
    rd1win6.makeMove(5, "R");
    rd1win6.makeMove(0, "B");
    rd1win6.makeMove(5, "R");
    rd1win6.makeMove(0, "B");
    rd1win6.makeMove(4, "R");
    rd1win6.makeMove(2, "B");
    rd1win6.makeMove(3, "R");
    var rd1win6_data = {
	board: rd1win6,
	str: "_ _ _ _ _ _ \n|_|_|_|_|_|R|\n|_|_|_|_|R|R|\n|B|_|B|R|B|R|\n|B|_|R|B|R|B|\n|B|R|B|B|B|R|\n|R|R|B|R|B|R|\n"
    };
    board_data.push(rd1win6_data);

    rd2win5.makeMove(4, "R");
    rd2win5.makeMove(0, "B");
    rd2win5.makeMove(0, "R");
    rd2win5.makeMove(3, "B");
    rd2win5.makeMove(3, "R");
    rd2win5.makeMove(0, "B");
    rd2win5.makeMove(0, "R");
    rd2win5.makeMove(1, "B");
    rd2win5.makeMove(0, "R");
    rd2win5.makeMove(1, "B");
    rd2win5.makeMove(2, "R");
    rd2win5.makeMove(2, "B");
    rd2win5.makeMove(2, "R");
    rd2win5.makeMove(1, "B");
    rd2win5.makeMove(1, "R");
    var rd2win5_data = {
	board: rd2win5,
	str: "_ _ _ _ _ _ \n|_|_|_|_|_|_|\n|R|_|_|_|_|_|\n|R|R|_|_|_|_|\n|B|B|R|_|_|_|\n|R|B|B|R|_|_|\n|B|B|R|B|R|_|\n"
    };
    board_data.push(rd2win5_data);

    board_data.push(rvwin4_data);
    board_data.push(rhwin4_data);
    board_data.push(rd1win4_data);
    board_data.push(rd2win4_data);
    board_data.push(tie_data);
    board_data.push(rhwin7_data);
    board_data.push(rd1win6_data);
    board_data.push(rd2win5_data);

    return board_data;
}

/** rvwin4: red vertical win with 4 in a row
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
/** rd2win4 
 *          _ _ _ _ _ _
 *         |_|_|_|_|_|_|
 *         |_|_|_|_|_|_|
 *         |_|R|_|_|_|_|
 *         |_|B|R|_|_|_|
 *         |_|B|B|R|_|_|
 *         |_|R|B|B|R|R|
 */
/** tie
 *          _ _ _ _ _ _
 *         |R|B|R|B|R|B|
 *         |R|B|R|B|R|B|
 *         |R|B|R|B|R|B|
 *         |B|R|B|R|B|R|
 *         |B|R|B|R|B|R|
 *         |B|R|B|R|B|R|
 */
/** rhwin7
 *          _ _ _ _ _ _ _
 *         |_|_|_|_|_|_|_|
 *         |_|_|_|_|_|_|_|
 *         |_|_|_|_|_|_|_|
 *         |_|_|_|_|_|_|_|
 *         |_|_|_|_|_|_|_|
 *         |B|B|B|_|B|B|B|
 *         |R|R|R|R|R|R|R|
 */
/** rd1win6
 *          _ _ _ _ _ _
 *         |_|_|_|_|_|R|
 *         |_|_|_|_|R|R|
 *         |B|_|B|R|B|R|
 *         |B|_|R|B|R|B|
 *         |B|R|B|B|B|R|
 *         |R|R|B|R|B|R|
 */
/** rd2win5
 *          _ _ _ _ _ _
 *         |_|_|_|_|_|_|
 *         |R|_|_|_|_|_|
 *         |R|R|_|_|_|_|
 *         |B|B|R|_|_|_|
 *         |R|B|B|R|_|_|
 *         |B|B|R|B|R|_|
 */
