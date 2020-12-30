package ttt_janise;

import java.util.ArrayList;
import java.util.Collections;
import java.util.TreeSet;

public class TicTacToe extends Game {

    public TicTacToe() {
        start = 0;
        name = "Tic Tac Toe";
    }

    public int doMove(int val, int move) {
        int[] board = getBoard(val);
        int player = toMove(board);
        board[move] = player;
        return getVal(board);
    }

    public int[] generateMoves(int val) {
        int[] board = getBoard(val);
        ArrayList<Integer> open = new ArrayList<>();
        for (int i = 0; i < board.length; i++) {
            if (board[i] == 0) {
                open.add(i);
            }
        }
        int[] a = new int[open.size()];
        for (int i = 0; i < open.size(); i++) {
            a[i] = open.get(i);
        }
        return a;
    }

    public String primitiveValue(int val) {
        if (generateMoves(val).length == 0) {
            return "tie";
        }

        int[] board = getBoard(val);
        int a = board[0], b = board[1], c = board[2];
        int d = board[3], e = board[4], f = board[5];
        int g = board[6], h = board[7], i = board[8];
        boolean hasWinner = a != 0 && ((a == b && a == c)
                || (a == d && a == g) || (a == e && a == i));
        hasWinner = hasWinner || (b != 0 && (b == e && b == h))
                || (c != 0 && ((c == f && c == i) || (c == e && c == g)))
                || (d != 0 && (d == e && d == f))
                || (g != 0 && (g == h && g == i));

        return hasWinner ? "lose" : "not_primitive";
    }

    public int[] symmetries(int val) {
        int[] board = getBoard(val);
        int a = board[0], b = board[1], c = board[2];
        int d = board[3], e = board[4], f = board[5];
        int g = board[6], h = board[7], i = board[8];

        int[] rot1 = new int[]{g, d, a, h, e, b, i, f, c};  //clockwise 90 deg
        int[] rot2 = new int[]{i, h, g, f, e, d, c, b, a};  //board, reversed
        int[] rot3 = new int[]{c, f, i, b, e, h, a, d, g};  //rot1, reversed
        int[] flip0 = new int[]{c, b, a, f, e, d, i, h, g}; //flip over vertical line
        int[] flip1 = new int[]{a, d, g, b, e, h, c, f, i}; //flip, then rotate 90 deg
        int[] flip2 = new int[]{g, h, i, d, e, f, a, b, c}; //flip0, reversed
        int[] flip3 = new int[]{i, f, c, h, e, b, g, d, a}; //flip1, reversed

        TreeSet<Integer> set = new TreeSet<>();
        Collections.addAll(set, val, getVal(rot1), getVal(rot2), getVal(rot3),
                getVal(flip0), getVal(flip1), getVal(flip2), getVal(flip3));

        int[] ret = new int[set.size()];
        int j = 0;
        for (int x : set) {
            ret[j++] = x;
        }

        return ret;
    }

    private int toMove(int[] board) {
        int ones = 0;
        int twos = 0;
        for (int sq : board) {
            if (sq == 1) {
                ones++;
            } else if (sq == 2) {
                twos++;
            }
        }
        return ones > twos ? 2 : 1;
    }

    private static int[] getBoard(int val) {
        int[] b = new int[9];
        for (int i = 0; i < 9; i++) {
            b[i] = (int) ((val / Math.pow(3, i)) % 3); //msb last
        }
        return b;
    }

    private static int getVal(int[] board) {
        int val = 0;
        for (int i = 0; i < board.length; i++) {
            val += board[i] * (Math.pow(3, i)); //msb last
        }
        return val;
    }

    public static void main(String[] args) {
        Game g = new TicTacToe();
        solve(g, false);
        solve(g, true);
    }
}
