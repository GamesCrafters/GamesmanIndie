<script>

/* Functions in board.js that are useful:
	currentColor -- returns current players color
	makeMove(column, color) -- makes a move, adds connections to the board
	undoLastMove -- self explanatory
	isWin(color) -- is move a win
	isLose(color) -- is move a loss
	isTie(color) -- is move a tie
	toString -- gives back string rep. of board pieces.

 		*          _ _ _ _ _ _ 
 		*         |_|_|_|_|_|_|
 		*         |_|_|_|_|_|_|
 		*         |_|_|_|R|_|_|
 		*         |_|_|_|R|_|_|
 		*         |_|_|B|R|B|_|
 		*         |_|R|B|R|B|_|

*/
var TreeNode = function (data) {
    this.parent = data.parent || null;
    this.children = data.children || [];
};
 
TreeNode.prototype.isLeaf = function () {
    return this.children.length == 0;
};
 
TreeNode.prototype.isRoot = function () {
    return this.parent == null;
};

//	IMPORTANT:
//
//***** Library used for DFS/BFS: http://underscorejs.org/ (the _.each() is for the library) ******
//
function visitDfs(node, func) {
    if (func) {
        func(node);
    }
 
    _.each(node.children, function (child) {
        visitDfs(child, func);
    });
}

/* PRUNE Function()
	
   The prune() function will prune out nodes that are single children to their parents 
   in order to collapse the tree into a simpler structure. This will eliminate groupings 
   of nodes that aren’t really grouping anything because their branching factor is 1

	USE: This code works by doing a DFS and calling a function on each node.  
	     That function examines the node to see if it has exactly one child and that the one child node is not a leaf (we don’t want to prune out leaves or roots).  
	     If it is, the child node is extracted out and assigned to the node’s parent’s children and then the child’s parent is reassigned to the node’s parent.  
	     This effectively eliminates (prunes) the node out of the tree collapsing it into a simpler structure.

*/

function prune(root) {
    visitDfs(root, function (node) {
        if (node.isRoot()) {
            return; // do not process roots
        }
        if (node.children.length == 1 && !node.children[0].isLeaf()) {
            var child = node.children[0],
                index = _.indexOf(node.parent.children, node);
            node.parent.children[index] = child;
            child.parent = node.parent;
        }
    });
}

function visitBfs(node, func) {
    var q = [node];
    while (q.length > 0) {
        node = q.shift();
        if (func) {
            func(node);
        }
 
        _.each(node.children, function (child) {
            q.push(child);
        });
    }
}


function chooseMove(Board b) {
	// AI Function to pick the next move. Expectimax.

    validMoves = []; //List of current valid board moves.
    bestMove = null; //Best Move to be returned
    maxVal = -1; //Max value in dict
    moveDict = {}; // {Move: Value}
    validMoves = b.validMoves();

    for(var i = 0; i < validMoves.length; i++){
        //Make move with current valid move
        //Save It's heuristic return value
        //Undo the move
        //Continue appending values and moves for each ValidMove.
        currentMove = validMoves[i];
        move = b.makeMove(currentMove);
        moveDict[currentMove] = b.eval(move);
        b.undoLastMove();
    }

    // Dict --> { Move: Value }
    // Find maximum value, return that key. 
    for (var values in moveDict) {
        var localMax = moveDict[values];
        if (localMax > maxVal) {
            maxVal = localMax;
            bestMove = values;
        }
    }
    //Returns Highest Key, aka Best Move.
    return bestMove;
}




</script>
