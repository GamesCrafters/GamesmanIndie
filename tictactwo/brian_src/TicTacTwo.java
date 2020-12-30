package brian_src;

import java.util.ArrayList;
import java.util.Collections;

public class TicTacTwo extends TicTacToe{

    private final int[] SIX_POWERS = {1, 6, 36, 216, 1296, 7776, 46656, 279936, 1679616};
    private final int BOARD_FACTOR = 10077696;

    /** TTT board, then 9 -> whose turn (0, 1), 10 -> X double-move used, 11 -> Y double-move used*/

    @Override
    protected int[] unpackPosition(int position) {
        int[] board = new int[12];
        int board_pos = position % BOARD_FACTOR;
        int other_data = position / BOARD_FACTOR;
        for (int i = 0; i < 9; i++) {
            board[i] = board_pos % 6;
            board_pos /= 6;
        }
        for (int i = 0; i < 3; i++) {
            board[9+i] = other_data % 2;
            other_data /= 2;
        }
        return board;
    }

    @Override
    protected int packPosition(int[] board) {
        int sum = 0;
        for (int i = 0; i < 9; i++) {
            sum += SIX_POWERS[i] * board[i];
        }
        if (board.length > 9) { //necessary for symmetry check
            sum += BOARD_FACTOR * (board[9] + 2*board[10] + 4*board[11]);
        }
        return sum;
    }

    // Mostly so the inheritance works
    @Override
    protected int whoseTurn(int[] board){
        return board[9] + 1;
    }

    protected boolean hasDoubleMove(int[] board) {
        return board[10 + board[9]] == 0;
    }

    /**
    Notation for board: 0 -> empty; 1-> X dominates; 2 -> Y dominates; 3 -> X; 4 -> Y; 5 -> XY
     Notation for moves: Single digit 0~8 is a single move, Double digit is (tens - 1), then (ones)
     */

    @Override
    public int doMove(int position, int move) {
        int[] board = unpackPosition(position);
        if (move <= 9) {
            // Single move: as in TTT
            if (doMoveHelper(board, move) == -1) {
                return -1;
            }
        } else {
            // Double move
            if (!hasDoubleMove(board)) {
                return -1;
            }
            board[10 + board[9]]++;
            if (doMoveHelper(board, move / 10 - 1) == -1) {
                return -1;
            }
            // Win check (disabled)
            //if (super.isWin(board) == 0) {
                if (doMoveHelper(board, move % 10) == -1) {
                    return -1;
                }
            //}
        }
        //Swap move
        board[9] = 1 - board[9];
        return packPosition(board);
    }

    /** Handles a "single move", as it were.*/
    private int doMoveHelper(int[] board, int move) {
        switch(board[9]) {
            case 0:
                // X moves
                switch(board[move]) {
                    case 3:
                    case 5:
                        board[move] = 1;
                        break;
                    case 0:
                        board[move] = 3;
                        break;
                    case 4:
                        board[move] = 5;
                        break;
                    default:
                        return -1;
                }
                break;
            case 1:
                // O moves
                switch(board[move]) {
                    case 4:
                    case 5:
                        board[move] = 2;
                        break;
                    case 0:
                        board[move] = 4;
                        break;
                    case 3:
                        board[move] = 5;
                        break;
                    default:
                        return -1;
                }
        }
        return 0;
    }

    @Override
    protected ArrayList<Integer> generateMovesHelper(int[] board) {
        ArrayList<Integer> moveList = new ArrayList<>();
        ArrayList<Integer> doubleInSame = new ArrayList<>();
        for (int i = 0; i < 9; i++) {
            if (board[i] != 1 && board[i] != 2) {
                moveList.add(i);
                if (board[i] != 5 && board[i] != whoseTurn(board) + 2) {
                    doubleInSame.add(i);
                }
            }
        }
        // Double moves
        if (hasDoubleMove(board)) {
            ArrayList<Integer> primaryMoveList = new ArrayList<>(moveList);
            for (Integer i : primaryMoveList) {
                for (Integer j : primaryMoveList) {
                    if (i < j) {
                        moveList.add(10 + 10*i + j);
                    }
                }
            }
            for (Integer i : doubleInSame) {
                moveList.add(10 + 11*i);
            }
        }
        return moveList;
    }

    @Override
    public ArrayList<Integer> getSymmetries(int position) {
        int board_pos = position % BOARD_FACTOR;
        int other_data = position / BOARD_FACTOR;
        ArrayList<Integer> simpleSymmetries = super.getSymmetries(board_pos);
        for (int i = 0; i < simpleSymmetries.size(); i++) {
            simpleSymmetries.set(i, simpleSymmetries.get(i) + other_data * BOARD_FACTOR);
        }
        return simpleSymmetries;
    }

    public static void main(String[] args) {
        TicTacTwo ttt = new TicTacTwo();
        int[] pos = {0, 1, 2, 3, 4, 5, 0, 1, 5, 0, 1, 1};
        ArrayList<Integer> sym = ttt.getSymmetries(ttt.packPosition(pos));
        for (int p : sym) {
            ttt.printPos(p);
        }
    }

    public void printPos(int path){
        for (int j : unpackPosition(path)){
            System.out.print(j + ", ");
        }
        System.out.println("");
    }
}
