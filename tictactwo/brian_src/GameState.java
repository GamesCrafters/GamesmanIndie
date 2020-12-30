package brian_src;

public class GameState {

    private PositionValue pv;
    private int remoteness;

    public GameState(PositionValue pv, int remoteness) {
        this.pv = pv;
        this.remoteness = remoteness;
    }

    public PositionValue positionValue() {
        return pv;
    }

    public int remoteness() {
        return remoteness;
    }
}
