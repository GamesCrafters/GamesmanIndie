package ttt_janise;

import java.util.TreeMap;

public abstract class Game {

    int start;
    String name;

    public static void solve(Game g, boolean symmetries) {
        System.out.printf("%s analysis (symmetries is %s)\n\n", g.name,
                symmetries ? "on" : "off");

        Solver s = new Solver(g);
        TreeMap<Integer, int[]> res = new TreeMap<>();

        int[] totals = new int[]{0, 0, 0, 0};

        s.solve(g.start, symmetries);
        TreeMap<Integer, Solver.State> positions = s.memo;
        for (int b : positions.descendingKeySet()) {
            Solver.State x = positions.get(b);
            if (!res.containsKey(x.remote)) {
                res.put(x.remote, new int[]{0, 0, 0});
            }
            int j = x.win ? 0 : (x.lose ? 1 : 2);
            res.get(x.remote)[j] += 1;
            totals[j]++;
            totals[3]++;
        }

        System.out.println("Remote   Win    Lose    Tie     Total");
        System.out.println("-------------------------------------");

        for (int i : res.descendingKeySet()) {
            int[] x = res.get(i);
            System.out.printf("%-4d     %-4d   %-4d    %-4d    %-4d\n",
                    i, x[0], x[1], x[2], x[0] + x[1] + x[2]);
        }
        System.out.println("-------------------------------------");
        System.out.printf("Total    %-4d   %-4d    %-4d    %-4d\n\n",
                totals[0], totals[1], totals[2], totals[3]);
    }

    public abstract int doMove(int board, int move);

    public abstract int[] generateMoves(int board);

    public abstract String primitiveValue(int board);

    public abstract int[] symmetries(int board);
}
