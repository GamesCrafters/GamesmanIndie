package brian_src;

import java.util.ArrayList;
import java.util.HashSet;

public class TicTacToe implements IntGame {

    // A bunch of saved values to avoid repetitive calculations
    private final int[] THREE_POWERS = {1, 3, 9, 27, 81, 243, 729, 2187, 6561};
    protected final int[][] WIN_POS = {{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}};

    /** These two methods decode an integer into a length-9 array of 0's, 1's and 2's
     *  and re-encode it.
     *  Imagine the array reading from top-left to bottom-right, English text style.
     */

    protected int[] unpackPosition(int position) {
        int[] board = new int[9];
        for (int i = 0; i < 9; i++) {
            board[i] = position % 3;
            position /= 3;
        }
        return board;
    }

    protected int packPosition(int[] board) {
        int sum = 0;
        for (int i = 0; i < board.length; i++) {
            sum += THREE_POWERS[i] * board[i];
        }
        return sum;
    }

    /**
     * This helper method determines the player - 1 or 2 - whose turn it is.
     * It returns -1 if the position is invalid.
     */
    protected int whoseTurn(int[] board) {
        int numOne = 0;
        int numTwo = 0;
        for (int square : board) {
            if (square == 1) {
                numOne++;
            } else if (square == 2) {
                numTwo++;
            }
        }
        if (numOne == numTwo) {
            return 1;
        } else if (numOne == numTwo + 1) {
            return 2;
        }
        return -1;
    }

    /**
     * This helper method determines if the argument player (1 or 2) is winning.
     * It returns the number of the winning player, or 0 if neither player has won,
     * or -1 if both players have "won" (i.e. the position is invalid).
     */
    protected int isWin(int[] board) {
        int winningPlayer = 0;
        for (int[] winType: WIN_POS) {
            if (board[winType[0]] == 1 && board[winType[1]] == 1 && board[winType[2]] == 1) {
                if (winningPlayer == 2) {
                    return -1;
                }
                winningPlayer = 1;
            }
            if (board[winType[0]] == 2 && board[winType[1]] == 2 && board[winType[2]] == 2) {
                if (winningPlayer == 1) {
                    return -1;
                }
                winningPlayer = 2;
            }
        }
        return winningPlayer;
    }

    public int startPosition() {
        return 0;
    }

    public int doMove(int position, int move) {
        int[] board = unpackPosition(position);
        if (board[move] != 0) {
            return -1;
        }
        int turn = whoseTurn(board);
        if (turn == -1) {
            return -1;
        }
        board[move] = turn;
        return packPosition(board);
    }

    public ArrayList<Integer> generateMoves(int position) {
        int[] board = unpackPosition(position);
        return generateMovesHelper(board);
    }

    protected ArrayList<Integer> generateMovesHelper(int[] board) {
        ArrayList<Integer> moveList = new ArrayList<>();
        for (int i = 0; i < 9; i++) {
            if (board[i] == 0) {
                moveList.add(i);
            }
        }
        return moveList;
    }

    public PositionValue primitiveValue(int position) {
        int[] board = unpackPosition(position);
        int playerTurn = whoseTurn(board);
        if (playerTurn == -1) {
            return PositionValue.ERROR;
        }
        int winner = isWin(board);
        if (winner == -1) {
            return PositionValue.ERROR;
        }
        if (playerTurn + winner == 3) { //one is 1, the other is 2
            return PositionValue.LOSE;
        } else if (winner != 0) {
            return PositionValue.ERROR;
        } else if (generateMovesHelper(board).size() == 0) {
            return PositionValue.TIE;
        }
        return PositionValue.NOT_PRIMITIVE;
    }

    public ArrayList<Integer> getSymmetries(int position) {
        int[] board = unpackPosition(position);
        int[] reflectBoard = {board[0], board[3], board[6], board[1], board[4], board[7], board[2], board[5], board[8]};
        HashSet<Integer> symmetries = new HashSet<>();
        symmetries.add(packPosition(reflectBoard));
        for (int i = 0; i < 3; i++) {
            board = rotate(board);
            reflectBoard = rotate(reflectBoard);
            symmetries.add(packPosition(board));
            symmetries.add(packPosition(reflectBoard));
        }
        ArrayList<Integer> ret = new ArrayList<>();
        ret.addAll(symmetries);
        return ret;
    }

    private int[] rotate(int[] in) {
        int[] out = {in[2], in[5], in[8], in[1], in[4], in[7], in[0], in[3], in[6]};
        return out;
    }
}
