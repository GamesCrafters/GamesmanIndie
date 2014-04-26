//TODO: replace color1, color2 w/ actual colors
function Board(x, y) {
    this._board = new Array(x);
    this._width = x;
    this._height = y;
    this._valid_moves = [];
    for(var i = 0; i < this._width; i++) {
	this._board.push([]);
	this._valid_moves.push(i);
    }
    this._connections = {
	color1: { h: {}, v: {}, d: {} },
	color2: { h: {}, v: {}, d: {} }
    };
    this._win = { color1: false, color2: false };
    var pos;
    for(var i = 0; i < this._width; i++) {
	for(var j = 0; j < this._height; j++) {
	    pos = [i, j];
	    connections[color1].h[pos] = 0;
	    connections[color1].v[pos] = 0;
	    connections[color1].d[pos] = 0;
	    connections[color2].h[pos] = 0;
	    connections[color2].v[pos] = 0;
	    connections[color2].d[pos] = 0;
	}
    }
    this._move_history = [];
    this._getOtherColor = function(color) {
	return color == color1 ? color2 : color1;
    };
    this._addConnections = function(pos, color) {
	var connections = this._connections[color];
    };
    this._removeConnections = function(pos, color) {};
}

Board.prototype.currentColor = function() {
    return this._current_color;
}

Board.prototype.makeMove = function(column, color) {
    var pos = [column, _board[column].length];
    this._board[column].push(column);
    if(this._board[column].length === this._height) {
	_valid_moves.splice(column, 1);
    }
    this._move_history.push({color: color, column: column});
    this._win[color] = this._addConnections(pos, color);
};
Board.prototype.undoLastMove = function() {
    var last_move = _move_history.pop();
    var board = this._board[last_move.column];
    var pos = [last_move.column, board.length];
    if(board.length == this._height) {
	this._valid_moves.push(last_move.column);
	this._valid_moves.sort();
    }
    board.pop();
    this._win[this.currentColor()] = 
        this._removeConnections(pos, last_move.color);
};

Board.prototype.isWin(color) = function() {
    return this._win[this.currentColor()];
};
Board.prototype.isLoss(color) = function() {
    return this.isWin(this._getOtherColor(color));
};
Board.prototype.isTie(color) = function() {
    return !this.isWin(color) && !this.isLoss(color) &&
           this._valid_moves.length == 0;
};
Board.prototype.isDraw = Board.prototype.isTie;
Board.prototype.validMoves = function() {
    return this._valid_moves;
};
Board.prototype.toString = function() {
    var str = "";
    var board = this._board;
    for(var i = 0; i < this._width; i++) {
	str += " _";
    }
    str += " \n";
    for(var j = this._height-1; j >= 0; j--) {
	for(var i = 0; i < this._width; i++) {
	    if (board[i][j] === color1) {
		str += "|R";
	    } else if(board[i][j] === color2) {
		str += "|B";
	    } else {
		str += "|_";
	    }
	}
	str += "|\n";
    }
};

/***********************************UNIT TESTS*********************************/

/** rvwin 
 *          _ _ _ _ _ _ 
 *         |_|_|_|_|_|_|
 *         |_|_|_|_|_|_|
 *         |_|_|_|R|_|_|
 *         |_|_|_|R|_|_|
 *         |_|_|B|R|B|_|
 *         |_|R|B|R|B|_|
 */
/** rhwin 
 *          _ _ _ _ _ _
 *         |_|_|_|_|_|_|
 *         |_|_|_|_|_|_|
 *         |_|_|_|_|_|_|
 *         |B|_|_|_|_|_|
 *         |B|_|R|R|R|R|
 *         |B|R|B|R|B|B|
 */
/** rdwin 
 *          _ _ _ _ _ _
 *         |_|_|_|_|_|_|
 *         |_|_|_|_|_|_|
 *         |_|_|_|_|R|_|
 *         |_|_|_|R|B|_|
 *         |_|_|R|B|B|_|
 *         |_|R|B|B|R|R|
 */
function runBoardTests() {
    var passed = 0;
    var results = loadAndRunTests();
    for(var i = 0; i < results.length; i++) {
	if(results[i].result != results[i].expected) {
	    console.log(results[i].name + " failed.");
	    console.log("Expected: " + results[i].expected);
	    console.log("Got: " + results[i].answer);
	    console.log("Board: " + results[i].board_str);
	} else {
	    console.log(results[i].name + " passed.");
	    passed++;
	}
    }
    console.log(passed + "/" + tests.length + " passed.");
}

function loadAndRunTests() {
    var data = loadTestData();
    var results = [];
    var result;
    for(var i = 0; i < data.length; i++) {
	result = {
	    name: data.names[i],
	    expected: data.expected[i],
	    board_str: data.board_strs[i]
	};
	result.answer = data.funcs[i].apply(null, data.args[i]);
	results.push(result);
    }
}

function loadTestData() {
    return {
	names: [
	    "rvwin_init",
	    "rhwin_init",
	    "rdwin_init",
	    "rvwin",
	    "rhwin",
	    "rdwin"
	],
	expected: [
	    true,
	    true,
	    true
	],
	board_strs: [
	],
	func: [
	],
	args: [
	]
    };
};
