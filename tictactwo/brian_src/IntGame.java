package brian_src;

import java.util.ArrayList;

public interface IntGame {
    // A game whose position, as well as their moves, can be implemented as integers
    int startPosition();
    int doMove(int position, int move);
    ArrayList<Integer> generateMoves(int position);
    PositionValue primitiveValue(int position);
    ArrayList<Integer> getSymmetries(int position);
}
