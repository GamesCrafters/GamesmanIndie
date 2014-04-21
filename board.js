function Board(x, y) {
    var board = new Array(x);
    var y_indices = new Array(x);
    var move_history = {
	color1: [], //replace w/ actual colors
	color2: []
    };
    var valid_moves = [];
    var connections = {
	color1: {},
	color2: {}
    };
    var width = x;
    var height = y;
    for(var i = 0; i < width; i++) {
	board[i] = new Array(height);
	y_indices[i] = 0;
	valid_moves.push(i);
    }
    var current_color = color1;
    var switchCurrentColor = function() {
	current_color = otherColor();
    };
    var getOtherColor = function(color) {
	return color == color1 ? color2 : color1;
    };
    var updateConnections = function(pos, mode) {};
}

Board.prototype.currentColor = function() {
    return current_color;
}

Board.prototype.makeMove = function(column, color) {
    var pos = [column, y_indices[column]];
    board[column][y_indices[column]] = color;
    move_history[color].push(column);
    y_indices[column]++;
    switchCurrentColor();
    updateConnections(pos, ADD);
};
Board.prototype.undoLastMove = function() {
    var last_move = move_history[this.currentColor()].pop();
    var pos = [last_move, y_indices[last_move]];
    y_indices[last_move]--;
    board[last_move][y_indices[last_move]] = EMPTY;
    switchCurrentColor();
    updateConnections(pos, REMOVE);
};

Board.prototype.isWin(color) = function() {
};
Board.prototype.isLoss(color) = function() {
    return isWin(getOtherColor(color));
};
Board.prototype.isTie(color) = function() {
    return !isWin(color) && !isLoss(color);
};
Board.prototype.isDraw = Board.prototype.isTie;
Board.prototype.validMoves = function() {
    return valid_moves;
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
    var answers = loadAndRunTests();
    for(var i = 0; i < answers.length; i++) {
	if(answers[i].result != answers[i].expected) {
	    console.log(answers[i].name + " failed.");
	    console.log("Expected: " + answers[i].expected);
	    console.log("Got: " + answers[i].result);
	    console.log("Board: " + answers[i].board);
	} else {
	    console.log(answers[i].name + " passed.");
	    passed++;
	}
    }
    console.log(passed + "/" + tests.length + " passed.");
}

function loadAndRunTests() {
}
