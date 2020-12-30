package brian_src;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.TreeMap;

public class Solver {

    private IntGame game;
    private HashMap<Integer, GameState> statemap;
    private boolean removeSymmetries;
    private String gameName;

    public Solver(IntGame game) {
        this.game = game;
        statemap = new HashMap<>();
        removeSymmetries = false;
        gameName = "Default Name";
    }

    public Solver(IntGame game, boolean remove) {
        this.game = game;
        statemap = new HashMap<>();
        removeSymmetries = remove;
        gameName = "Default Name";
    }

    public Solver (IntGame game, String name) {
        this.game = game;
        statemap = new HashMap<>();
        removeSymmetries = false;
        gameName = name;
    }

    public Solver(IntGame game, boolean remove, String name) {
        this.game = game;
        statemap = new HashMap<>();
        removeSymmetries = remove;
        gameName = name;
    }

    public GameState solve(int position) {
        if (statemap.containsKey(position)) {
            return statemap.get(position);
        }
        if (removeSymmetries) {
            ArrayList<Integer> symmetries = game.getSymmetries(position);
            for (Integer symmetry : symmetries) {
                if (statemap.containsKey(symmetry)) {
                    return statemap.get(symmetry);
                }
            }
        }
        try {
            PositionValue pVal = game.primitiveValue(position);
            GameState gs;
            switch (pVal) {
                case ERROR:
                    return new GameState(PositionValue.ERROR, -1);
                case WIN:
                case LOSE:
                case TIE:
                    gs = new GameState(pVal, 0);
                    statemap.put(position, gs);
                    return gs;
                case NOT_PRIMITIVE:
                default:
                    ArrayList<Integer> moves = game.generateMoves(position);
                    HashMap<PositionValue, Integer> states = new HashMap<>();
                    for (Integer move : moves) {
                        gs = solve(game.doMove(position, move));
                        switch (gs.positionValue()) {
                            case LOSE:
                            case TIE:
                                if (states.containsKey(gs.positionValue())) {
                                    states.put(gs.positionValue(), Math.min(gs.remoteness(), states.get(gs.positionValue())));
                                } else {
                                    states.put(gs.positionValue(), gs.remoteness());
                                }
                                break;
                            case WIN:
                                if (states.containsKey(PositionValue.WIN)) {
                                    states.put(PositionValue.WIN, Math.max(gs.remoteness(), states.get(PositionValue.WIN)));
                                } else {
                                    states.put(PositionValue.WIN, gs.remoteness());
                                }
                                break;
                        }
                    }
                    if (states.containsKey(PositionValue.LOSE)) {
                        gs = new GameState(PositionValue.WIN, states.get(PositionValue.LOSE) + 1);
                    } else if (states.containsKey(PositionValue.TIE)) {
                        gs = new GameState(PositionValue.TIE, states.get(PositionValue.TIE) + 1);
                    } else {
                        gs = new GameState(PositionValue.LOSE, states.get(PositionValue.WIN) + 1);
                    }
                    statemap.put(position, gs);
                    //System.out.print("State: ");
                    //((brian_src.TicTacTwo)game).printPos(position);
                    //System.out.println("Remoteness: " + gs.remoteness());
                    return gs;
            }
        } catch (StackOverflowError err) {
            GameState gs = new GameState(PositionValue.DRAW, Integer.MAX_VALUE);
            statemap.put(position, gs);
            return gs;
        }
    }

    public void detailedAnalysis() {
        // Solve
        solve(game.startPosition());
        TicTacTwo temp = new TicTacTwo();
        TreeMap<Integer, Integer[]> results = new TreeMap<>(); // needs to be sorted
        for (GameState gs : statemap.values()) {
            Integer[] stateArray = {0, 0, 0};
            if (results.containsKey(gs.remoteness())) {
                stateArray = results.get(gs.remoteness());
            }
            switch (gs.positionValue()) {
                case WIN:
                    stateArray[0]++;
                    break;
                case LOSE:
                    stateArray[1]++;
                    break;
                case TIE:
                    stateArray[2]++;
                    break;
            }
            results.put(gs.remoteness(), stateArray);
        }
        // Print
        System.out.print(gameName + " analysis ");
        if (removeSymmetries) {
            System.out.println("(symmetries removed):");
        } else {
            System.out.println("(symmetries not removed):");
        }
        System.out.println("Remote  Win      Lose     Tie      Total");
        System.out.println("----------------------------------------");
        int winTotal = 0, loseTotal = 0, tieTotal = 0, total = 0;
        for (Integer i : results.descendingKeySet()) {
            Integer[] arr = results.get(i);
            int sum = arr[0] + arr[1] + arr[2];
            System.out.printf("%-3d     %-7d  %-7d  %-7d  %-7d\n",
                    i, arr[0], arr[1], arr[2], sum);
            winTotal += arr[0];
            loseTotal += arr[1];
            tieTotal += arr[2];
            total += sum;
        }
        System.out.println("------------------------------------------");
        System.out.printf("Total   %-7d  %-7d  %-7d  %-7d\n",
                winTotal, loseTotal, tieTotal, total);
    }

    public static void main(String[] args) {
       /* G10_to_0_by_1_or_2 g = new G10_to_0_by_1_or_2();
        brian_src.Solver s = new brian_src.Solver(g, "10 to 0 by 1 or 2");
        s.detailedAnalysis();
        System.out.println("\n");
        brian_src.TicTacToe ttt = new brian_src.TicTacToe();
        s = new brian_src.Solver(ttt, "Tic Tac Toe");
        s.detailedAnalysis();
        System.out.println("\n");
        s = new brian_src.Solver(ttt, true, "Tic Tac Toe");
        s.detailedAnalysis();*/
        TicTacTwo tttwo = new TicTacTwo();
        Solver s = new Solver(tttwo, false, "Tic Tac Two");
        s.detailedAnalysis();

    }

    /*ArrayList<Integer> list = new ArrayList<>();
        for (Integer hash : statemap.keySet()) {
            GameState gs = statemap.get(hash);
            if (gs.remoteness() == 0 && gs.positionValue() == PositionValue.LOSE) {
                list.add(hash);
            }
        }
        System.out.println("Start of print");
        java.util.Collections.sort(list);
        for (Integer hash: list){
            temp.printPos(hash);
            // Need to print to file
        }*/
}
